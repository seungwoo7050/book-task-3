from __future__ import annotations

import tempfile
from pathlib import Path

from os_mini_fs import MiniFS


def main() -> int:
    with tempfile.TemporaryDirectory() as temp_dir:
        image = Path(temp_dir) / "demo-image.json"
        MiniFS.mkfs(image, inode_count=8, block_count=16, block_size=8)
        fs = MiniFS(image)
        fs.create("note")
        fs.write("note", "hello-os")
        print("[after write]")
        print(fs.describe())
        print("[cat note]")
        print(fs.cat("note"))
        try:
            fs.write("note", "new-content", crash_stage="after_commit")
        except Exception as exc:  # Simulated crash by design
            print(f"[simulated crash] {exc}")
        recovered = fs.recover()
        print("[after recover]")
        print(recovered)
        print(fs.describe())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
