from __future__ import annotations

from pathlib import Path

from os_mini_fs import MiniFS, SimulatedCrash


def make_fs(tmp_path: Path) -> MiniFS:
    image = tmp_path / "fs.json"
    MiniFS.mkfs(image, inode_count=8, block_count=16, block_size=8)
    return MiniFS(image)


def test_create_write_read_round_trip(tmp_path: Path) -> None:
    fs = make_fs(tmp_path)
    fs.create("note")
    fs.write("note", "hello-os")
    assert fs.cat("note") == "hello-os"


def test_unlink_frees_inode_and_blocks(tmp_path: Path) -> None:
    fs = make_fs(tmp_path)
    fs.create("note")
    fs.write("note", "abcdefgh1234")
    before = fs.describe()
    fs.unlink("note")
    after = fs.describe()
    assert "used_inodes=2" in before
    assert "used_inodes=1" in after
    assert "used_blocks=0" in after


def test_reopen_persists_files(tmp_path: Path) -> None:
    fs = make_fs(tmp_path)
    fs.create("note")
    fs.write("note", "persist-me")
    reopened = MiniFS(tmp_path / "fs.json")
    assert reopened.cat("note") == "persist-me"


def test_prepared_journal_is_discarded(tmp_path: Path) -> None:
    fs = make_fs(tmp_path)
    fs.create("note")
    fs.write("note", "old")
    try:
        fs.write("note", "newer", crash_stage="after_prepare")
    except SimulatedCrash:
        pass
    stats = fs.recover()
    assert stats["discarded"] == 1
    assert fs.cat("note") == "old"


def test_committed_journal_is_replayed(tmp_path: Path) -> None:
    fs = make_fs(tmp_path)
    fs.create("note")
    fs.write("note", "old")
    try:
        fs.write("note", "newer", crash_stage="after_commit")
    except SimulatedCrash:
        pass
    stats = fs.recover()
    assert stats["replayed"] == 1
    assert fs.cat("note") == "newer"
