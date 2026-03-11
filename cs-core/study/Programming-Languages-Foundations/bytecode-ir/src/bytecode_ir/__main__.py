from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import BytecodeIRError, disassemble_source, run_source


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Compile the shared PL foundations language to bytecode and run it.")
    parser.add_argument("--program", type=Path, help="path to a .plf source file")
    parser.add_argument("--demo", help="demo name or 'all'")
    parser.add_argument("--emit", choices=["run", "disasm"], default="run")
    args = parser.parse_args(argv)

    try:
        if args.program is not None:
            source = args.program.read_text(encoding="utf-8")
            _print_summary(args.program.name, source, args.emit)
            return 0

        demos = _load_demo_sources()
        selected = args.demo or "all"
        if selected == "all":
            names = list(demos)
        else:
            if selected not in demos:
                raise SystemExit(f"unknown demo '{selected}'. available: {', '.join(demos)}")
            names = [selected]

        for index, name in enumerate(names):
            if index:
                print()
            _print_summary(name, demos[name], args.emit)
        return 0
    except BytecodeIRError as error:
        print(error, file=sys.stderr)
        return 1


def _print_summary(name: str, source: str, emit: str) -> None:
    print(f"== {name} ==")
    print("-- source --")
    print(source.strip())
    if emit == "disasm":
        print("-- disasm --")
        print(disassemble_source(source))
        return
    print("-- result --")
    print(run_source(source))


def _load_demo_sources() -> dict[str, str]:
    root = Path(__file__).resolve().parents[2]
    examples_dir = root / "examples"
    return {path.stem: path.read_text(encoding="utf-8") for path in sorted(examples_dir.glob("*.plf"))}


if __name__ == "__main__":
    raise SystemExit(main())
