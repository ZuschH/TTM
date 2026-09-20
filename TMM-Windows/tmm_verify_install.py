#!/usr/bin/env python3
"""Verify an installed TMM application against its build manifest."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def verify(root: Path, manifest_path: Path) -> None:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8-sig"))
    root = root.resolve()
    for item in manifest["files"]:
        relative = Path(item["path"])
        target = (root / relative).resolve()
        if root not in target.parents:
            raise ValueError(f"manifest path escapes installation root: {relative}")
        if not target.is_file():
            raise FileNotFoundError(f"installed file missing: {relative}")
        if target.stat().st_size != int(item["size"]):
            raise ValueError(f"installed file has wrong size: {relative}")
        digest = hashlib.sha256(target.read_bytes()).hexdigest()
        if digest.lower() != str(item["sha256"]).lower():
            raise ValueError(f"installed file hash mismatch: {relative}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    args = parser.parse_args()
    verify(args.root, args.manifest)
    print("TMM application manifest verified.")


if __name__ == "__main__":
    main()
