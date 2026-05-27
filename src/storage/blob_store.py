from __future__ import annotations

import hashlib
import logging
import os
from pathlib import Path
from typing import Any

logger = logging.getLogger("blob_store")

BLOB_SUBDIR = "data" / Path("blobs")


class BlobStore:
    def __init__(self, base_path: str | Path | None = None) -> None:
        if base_path is None:
            repo_root = Path(__file__).resolve().parent.parent.parent
            base_path = repo_root / BLOB_SUBDIR
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)
        logger.info("Blob store at %s", self.base_path)

    def _shard_path(self, content_hash: str) -> Path:
        return self.base_path / content_hash[:2] / content_hash

    def store(self, data: bytes) -> str:
        content_hash = hashlib.sha256(data).hexdigest()
        path = self._shard_path(content_hash)
        if path.exists():
            return content_hash
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        return content_hash

    def retrieve(self, content_hash: str) -> bytes | None:
        path = self._shard_path(content_hash)
        if path.exists():
            return path.read_bytes()
        return None

    def exists(self, content_hash: str) -> bool:
        return self._shard_path(content_hash).exists()

    def delete(self, content_hash: str) -> bool:
        path = self._shard_path(content_hash)
        if path.exists():
            path.unlink()
            return True
        return False

    def count(self) -> int:
        count = 0
        for shard_dir in self.base_path.iterdir():
            if shard_dir.is_dir():
                count += len(list(shard_dir.iterdir()))
        return count

    def total_size_bytes(self) -> int:
        total = 0
        for shard_dir in self.base_path.iterdir():
            if shard_dir.is_dir():
                for blob_file in shard_dir.iterdir():
                    total += blob_file.stat().st_size
        return total
