"""Headless playtest: run a step file against pokeblue.gbc in PyBoy, saving screenshots.

Usage: .venv/bin/python playtest/playtest.py steps/FILE.txt [--state IN.state] [--save OUT.state]

Step file, one per line (# comments):
    a / b / start / select / up / down / left / right [N]   press, then wait N frames (default 20)
    mash BUTTON COUNT [N]                                   press COUNT times, N frames apart
    until BUTTON TEXT...                                    press (40 frames apart, max 200) until TEXT is on screen
    untilram LABEL HEX BUTTON...                            cycle the buttons (max 300) until the byte at LABEL is HEX
    wait N                                                  idle N frames
    shot NAME                                               screenshot to playtest/out/NAME.png
    ram LABEL [COUNT]                                       print COUNT bytes at a pokeblue.sym label
    text                                                    print the on-screen text
    poke LABEL HEX...                                       write bytes starting at a pokeblue.sym label
"""
import sys
from pathlib import Path

from pyboy import PyBoy

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "playtest" / "out"


def load_symbols():
    syms = {}
    for line in (ROOT / "pokeblue.sym").read_text().splitlines():
        if line and not line.startswith(";"):
            addr, name = line.split()
            if ":" not in addr:  # exported constants, not addresses
                continue
            syms[name] = int(addr.split(":")[1], 16)
    return syms


def charmap(code):
    if 0x80 <= code <= 0x99:
        return chr(ord("A") + code - 0x80)
    if 0xA0 <= code <= 0xB9:
        return chr(ord("a") + code - 0xA0)
    if 0xF6 <= code <= 0xFF:
        return chr(ord("0") + code - 0xF6)
    return {0x7F: " ", 0xBA: "é", 0xE7: "!", 0xE6: "?", 0xE8: ".", 0xF4: ",", 0xED: ">"}.get(code, " ")


def screen_text(pb, syms):
    """The 20x18 background tile map, decoded, one string per row."""
    base = syms["wTileMap"]
    return [ "".join(charmap(pb.memory[base + y * 20 + x]) for x in range(20)) for y in range(18)]


def main():
    args = sys.argv[1:]
    steps = Path(args[0])
    if not steps.is_absolute():
        steps = ROOT / "playtest" / steps
    state_in = args[args.index("--state") + 1] if "--state" in args else None
    state_out = args[args.index("--save") + 1] if "--save" in args else None

    OUT.mkdir(parents=True, exist_ok=True)
    syms = load_symbols()
    pb = PyBoy(str(ROOT / "pokeblue.gbc"), window="null", sound_emulated=False)
    pb.set_emulation_speed(0)
    if state_in:
        with open(state_in, "rb") as f:
            pb.load_state(f)

    def press(button, wait):
        hold = 16 if button in ("up", "down", "left", "right") else 4  # 16 frames = one step
        pb.button(button, hold)
        pb.tick(hold + wait)

    for raw in steps.read_text().splitlines():
        line = raw.split("#")[0].split()
        if not line:
            continue
        cmd, rest = line[0], line[1:]
        if cmd in ("a", "b", "start", "select", "up", "down", "left", "right"):
            press(cmd, int(rest[0]) if rest else 20)
        elif cmd == "mash":
            for _ in range(int(rest[1])):
                press(rest[0], int(rest[2]) if len(rest) > 2 else 20)
        elif cmd == "until":
            want = " ".join(rest[1:])
            for _ in range(200):
                if any(want in row for row in screen_text(pb, syms)):
                    break
                press(rest[0], 40)
            else:
                raise SystemExit(f"never saw {want!r}")
        elif cmd == "poke":
            for i, byte in enumerate(rest[1:]):
                pb.memory[syms[rest[0]] + i] = int(byte, 16)
        elif cmd == "untilram":
            addr, want, buttons = syms[rest[0]], int(rest[1], 16), rest[2:]
            for i in range(300):
                if pb.memory[addr] == want:
                    break
                press(buttons[i % len(buttons)], 10)
            else:
                raise SystemExit(f"{rest[0]} never became {rest[1]}")
        elif cmd == "text":
            print("\n".join(r.rstrip() for r in screen_text(pb, syms) if r.strip()))
        elif cmd == "wait":
            pb.tick(int(rest[0]))
        elif cmd == "shot":
            pb.screen.image.convert("RGB").save(OUT / f"{rest[0]}.png")
            print("shot", rest[0])
        elif cmd == "ram":
            addr, n = syms[rest[0]], int(rest[1]) if len(rest) > 1 else 1
            print(rest[0], " ".join(f"{pb.memory[addr + i]:02x}" for i in range(n)))
        else:
            raise SystemExit(f"unknown step: {raw}")

    if state_out:
        with open(state_out, "wb") as f:
            pb.save_state(f)
    pb.stop(save=False)


if __name__ == "__main__":
    main()
