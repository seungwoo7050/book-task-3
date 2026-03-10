from __future__ import annotations

from tests.compose_harness import compose_stack


def main() -> None:
    with compose_stack():
        return


if __name__ == "__main__":
    main()
