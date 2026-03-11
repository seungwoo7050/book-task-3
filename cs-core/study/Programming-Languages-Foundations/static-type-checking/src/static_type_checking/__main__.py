from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import StaticTypeCheckingError, check_source, format_type


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check the shared PL foundations language before runtime.")
    parser.add_argument("--program", type=Path, help="path to a .plf source file")
    parser.add_argument("--demo", help="demo name or 'all'")
    args = parser.parse_args(argv)

    try:
        if args.program is not None:
            source = args.program.read_text(encoding="utf-8")
            _print_summary(args.program.name, source)
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
            _print_summary(name, demos[name])
        return 0
    except StaticTypeCheckingError as error:
        print(error, file=sys.stderr)
        return 1


def _print_summary(name: str, source: str) -> None:
    type_expr = check_source(source)
    print(f"== {name} ==")
    print("-- source --")
    print(source.strip())
    print("-- type --")
    print(format_type(type_expr))


def _load_demo_sources() -> dict[str, str]:
    root = Path(__file__).resolve().parents[2]
    examples_dir = root / "examples"
    return {path.stem: path.read_text(encoding="utf-8") for path in sorted(examples_dir.glob("*.plf"))}


if __name__ == "__main__":
    raise SystemExit(main())
