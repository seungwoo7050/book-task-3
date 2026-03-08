#!/usr/bin/env python3
"""Restore official CS:APP self-study assets into local study/problem trees.

The restored handouts are kept under each project's ignored `problem/official/`
directory so the repository can keep tracked study-owned material separate from
official course handouts and binaries.
"""

from __future__ import annotations

import argparse
import io
import shutil
import ssl
import tarfile
import urllib.request
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class LabSpec:
    name: str
    url: str
    project_dir: str
    nested_sim_tar: str | None = None


REPO_ROOT = Path(__file__).resolve().parents[2]

LABS: dict[str, LabSpec] = {
    "datalab": LabSpec(
        name="datalab",
        url="http://csapp.cs.cmu.edu/3e/datalab-handout.tar",
        project_dir="study/Foundations-CSAPP/datalab/problem",
    ),
    "bomblab": LabSpec(
        name="bomblab",
        url="http://csapp.cs.cmu.edu/3e/bomb.tar",
        project_dir="study/Foundations-CSAPP/bomblab/problem",
    ),
    "attacklab": LabSpec(
        name="attacklab",
        url="http://csapp.cs.cmu.edu/3e/target1.tar",
        project_dir="study/Foundations-CSAPP/attacklab/problem",
    ),
    "archlab": LabSpec(
        name="archlab",
        url="http://csapp.cs.cmu.edu/3e/archlab-handout.tar",
        project_dir="study/Foundations-CSAPP/archlab/problem",
        nested_sim_tar="archlab-handout/sim.tar",
    ),
}


def safe_extract(tf: tarfile.TarFile, destination: Path) -> None:
    destination = destination.resolve()
    for member in tf.getmembers():
        target = (destination / member.name).resolve()
        if not str(target).startswith(str(destination)):
            raise ValueError(f"refusing to extract outside destination: {member.name}")
    tf.extractall(destination, filter="data")


def fetch_archive(url: str) -> bytes:
    context = ssl._create_unverified_context()
    with urllib.request.urlopen(url, timeout=120, context=context) as response:
        return response.read()


def restore_lab(spec: LabSpec) -> None:
    problem_dir = REPO_ROOT / spec.project_dir
    official_dir = problem_dir / "official"

    if official_dir.exists():
        shutil.rmtree(official_dir)
    official_dir.mkdir(parents=True, exist_ok=True)

    archive_bytes = fetch_archive(spec.url)
    with tarfile.open(fileobj=io.BytesIO(archive_bytes), mode="r:*") as archive:
        safe_extract(archive, official_dir)

    if spec.nested_sim_tar:
        sim_tar = official_dir / spec.nested_sim_tar
        with tarfile.open(sim_tar, mode="r:*") as nested:
            safe_extract(nested, sim_tar.parent)

    print(f"[restored] {spec.name}: {official_dir}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Restore official CS:APP self-study handouts for local verification."
    )
    parser.add_argument(
        "labs",
        nargs="*",
        choices=sorted(LABS),
        help="Lab names to restore. Defaults to all known gap projects.",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Restore all supported labs.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    selected = sorted(LABS) if args.all or not args.labs else args.labs
    for lab in selected:
        restore_lab(LABS[lab])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
