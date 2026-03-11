from __future__ import annotations

import argparse

from .core import MiniFS


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Operate on a toy filesystem image.")
    parser.add_argument("--image", required=True, help="Path to the JSON disk image.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    mkfs = subparsers.add_parser("mkfs", help="Create a new image.")
    mkfs.add_argument("--inodes", type=int, required=True)
    mkfs.add_argument("--blocks", type=int, required=True)
    mkfs.add_argument("--block-size", type=int, default=16)

    subparsers.add_parser("ls", help="List files.")

    create = subparsers.add_parser("create", help="Create an empty file.")
    create.add_argument("name")

    write = subparsers.add_parser("write", help="Write full file contents.")
    write.add_argument("name")
    write.add_argument("content")

    cat = subparsers.add_parser("cat", help="Read a file.")
    cat.add_argument("name")

    unlink = subparsers.add_parser("unlink", help="Delete a file.")
    unlink.add_argument("name")

    subparsers.add_parser("recover", help="Replay or discard journal entries.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "mkfs":
        MiniFS.mkfs(args.image, args.inodes, args.blocks, args.block_size)
        print(f"mkfs image={args.image} inodes={args.inodes} blocks={args.blocks}")
        return 0

    fs = MiniFS(args.image)
    if args.command == "ls":
        listing = fs.list_files()
        if not listing:
            print("(empty)")
            return 0
        for item in listing:
            print(f"{item['name']} size={item['size']} blocks={item['blocks']}")
        return 0
    if args.command == "create":
        fs.create(args.name)
        print(f"created {args.name}")
        return 0
    if args.command == "write":
        fs.write(args.name, args.content)
        print(f"wrote {len(args.content)} bytes to {args.name}")
        return 0
    if args.command == "cat":
        print(fs.cat(args.name))
        return 0
    if args.command == "unlink":
        fs.unlink(args.name)
        print(f"removed {args.name}")
        return 0
    if args.command == "recover":
        stats = fs.recover()
        print(f"replayed={stats['replayed']} discarded={stats['discarded']}")
        return 0
    raise RuntimeError("unreachable")
