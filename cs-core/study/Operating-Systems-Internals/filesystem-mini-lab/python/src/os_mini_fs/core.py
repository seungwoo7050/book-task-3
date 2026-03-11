from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class SimulatedCrash(RuntimeError):
    message: str

    def __str__(self) -> str:
        return self.message


class MiniFS:
    def __init__(self, image_path: str | Path):
        self.image_path = Path(image_path)

    @classmethod
    def mkfs(
        cls,
        image_path: str | Path,
        inode_count: int,
        block_count: int,
        block_size: int = 16,
    ) -> "MiniFS":
        image = {
            "superblock": {
                "inode_count": inode_count,
                "block_count": block_count,
                "block_size": block_size,
            },
            "inode_bitmap": [False] * inode_count,
            "block_bitmap": [False] * block_count,
            "inodes": [None] * inode_count,
            "root": {},
            "blocks": [None] * block_count,
            "journal": [],
            "next_txid": 1,
        }
        image["inode_bitmap"][0] = True
        image["inodes"][0] = {"type": "dir", "size": 0, "blocks": []}
        fs = cls(image_path)
        fs._save(image)
        return fs

    def list_files(self) -> list[dict[str, int | str]]:
        image = self._load()
        files: list[dict[str, int | str]] = []
        for name in sorted(image["root"]):
            inode_index = image["root"][name]
            inode = image["inodes"][inode_index]
            files.append({"name": name, "size": inode["size"], "blocks": len(inode["blocks"])})
        return files

    def describe(self) -> str:
        image = self._load()
        listing = ", ".join(
            f"{item['name']}({item['size']}B/{item['blocks']}blk)" for item in self.list_files()
        ) or "(empty)"
        return (
            f"files={listing}\n"
            f"used_inodes={sum(image['inode_bitmap'])} "
            f"used_blocks={sum(image['block_bitmap'])} "
            f"journal_entries={len(image['journal'])}"
        )

    def create(self, name: str, crash_stage: str | None = None) -> None:
        image = self._load()
        if name in image["root"]:
            raise FileExistsError(name)
        txid = self._begin_transaction(image, "create", {"name": name})
        self._maybe_crash(crash_stage, "after_prepare")
        self._commit_transaction(image, txid)
        self._maybe_crash(crash_stage, "after_commit")
        self._apply_and_finalize(image, txid)

    def write(self, name: str, content: str, crash_stage: str | None = None) -> None:
        image = self._load()
        inode = self._lookup_inode(image, name)
        new_blocks = self._allocate_data_blocks(image, content)
        payload = {
            "name": name,
            "new_blocks": new_blocks,
            "new_size": len(content),
            "old_blocks": inode["blocks"],
            "old_size": inode["size"],
        }
        txid = self._begin_transaction(image, "write", payload)
        self._maybe_crash(crash_stage, "after_prepare")
        self._commit_transaction(image, txid)
        self._maybe_crash(crash_stage, "after_commit")
        self._apply_and_finalize(image, txid)

    def cat(self, name: str) -> str:
        image = self._load()
        inode = self._lookup_inode(image, name)
        content = "".join(image["blocks"][block_id] or "" for block_id in inode["blocks"])
        return content[: inode["size"]]

    def unlink(self, name: str, crash_stage: str | None = None) -> None:
        image = self._load()
        self._lookup_inode(image, name)
        txid = self._begin_transaction(image, "unlink", {"name": name})
        self._maybe_crash(crash_stage, "after_prepare")
        self._commit_transaction(image, txid)
        self._maybe_crash(crash_stage, "after_commit")
        self._apply_and_finalize(image, txid)

    def recover(self) -> dict[str, int]:
        image = self._load()
        replayed = 0
        discarded = 0
        for entry in list(image["journal"]):
            if entry["state"] == "prepared":
                discarded += 1
                self._discard_prepared(image, entry)
                image["journal"].remove(entry)
                continue
            replayed += 1
            self._apply_entry(image, entry)
            image["journal"].remove(entry)
        self._save(image)
        return {"replayed": replayed, "discarded": discarded}

    def _begin_transaction(self, image: dict, kind: str, payload: dict) -> int:
        txid = image["next_txid"]
        image["next_txid"] += 1
        image["journal"].append({"txid": txid, "kind": kind, "state": "prepared", "payload": payload})
        self._save(image)
        return txid

    def _commit_transaction(self, image: dict, txid: int) -> None:
        entry = self._find_entry(image, txid)
        entry["state"] = "committed"
        self._save(image)

    def _apply_and_finalize(self, image: dict, txid: int) -> None:
        entry = self._find_entry(image, txid)
        self._apply_entry(image, entry)
        image["journal"].remove(entry)
        self._save(image)

    def _apply_entry(self, image: dict, entry: dict) -> None:
        kind = entry["kind"]
        payload = entry["payload"]
        if kind == "create":
            self._apply_create(image, payload["name"])
        elif kind == "write":
            self._apply_write(image, payload)
        elif kind == "unlink":
            self._apply_unlink(image, payload["name"])
        else:
            raise ValueError(f"unknown journal kind: {kind}")

    def _apply_create(self, image: dict, name: str) -> None:
        if name in image["root"]:
            return
        inode_index = self._allocate_inode(image)
        image["root"][name] = inode_index
        image["inodes"][inode_index] = {"type": "file", "size": 0, "blocks": []}

    def _apply_write(self, image: dict, payload: dict) -> None:
        inode = self._lookup_inode(image, payload["name"])
        old_blocks = list(inode["blocks"])
        inode["blocks"] = list(payload["new_blocks"])
        inode["size"] = payload["new_size"]
        self._free_blocks(image, old_blocks)

    def _apply_unlink(self, image: dict, name: str) -> None:
        if name not in image["root"]:
            return
        inode_index = image["root"].pop(name)
        inode = image["inodes"][inode_index]
        self._free_blocks(image, inode["blocks"])
        image["inode_bitmap"][inode_index] = False
        image["inodes"][inode_index] = None

    def _discard_prepared(self, image: dict, entry: dict) -> None:
        if entry["kind"] == "write":
            self._free_blocks(image, entry["payload"]["new_blocks"])

    def _allocate_inode(self, image: dict) -> int:
        for index in range(1, len(image["inode_bitmap"])):
            if not image["inode_bitmap"][index]:
                image["inode_bitmap"][index] = True
                return index
        raise RuntimeError("no free inode")

    def _allocate_data_blocks(self, image: dict, content: str) -> list[int]:
        block_size = image["superblock"]["block_size"]
        chunks = [content[index : index + block_size] for index in range(0, len(content), block_size)] or [""]
        free = [index for index, used in enumerate(image["block_bitmap"]) if not used]
        if len(free) < len(chunks):
            raise RuntimeError("no free block")
        block_ids = free[: len(chunks)]
        for block_id, chunk in zip(block_ids, chunks):
            image["block_bitmap"][block_id] = True
            image["blocks"][block_id] = chunk
        self._save(image)
        return block_ids

    def _free_blocks(self, image: dict, block_ids: list[int]) -> None:
        for block_id in block_ids:
            if 0 <= block_id < len(image["block_bitmap"]):
                image["block_bitmap"][block_id] = False
                image["blocks"][block_id] = None

    def _lookup_inode(self, image: dict, name: str) -> dict:
        if name not in image["root"]:
            raise FileNotFoundError(name)
        inode_index = image["root"][name]
        inode = image["inodes"][inode_index]
        if inode is None:
            raise RuntimeError(f"missing inode for {name}")
        return inode

    def _find_entry(self, image: dict, txid: int) -> dict:
        for entry in image["journal"]:
            if entry["txid"] == txid:
                return entry
        raise RuntimeError(f"missing txid {txid}")

    def _load(self) -> dict:
        return json.loads(self.image_path.read_text())

    def _save(self, image: dict) -> None:
        self.image_path.write_text(json.dumps(image, indent=2))

    @staticmethod
    def _maybe_crash(crash_stage: str | None, stage: str) -> None:
        if crash_stage == stage:
            raise SimulatedCrash(f"simulated crash at {stage}")
