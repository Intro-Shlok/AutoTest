from __future__ import annotations

import time
from collections import defaultdict
from typing import Any

TTL_DEFAULT = 3600


class ShortTermMemory:
    def __init__(self, ttl: float = TTL_DEFAULT) -> None:
        self._data: dict[str, Any] = {}
        self._expiry: dict[str, float] = {}
        self._ttl = ttl

    def set(self, key: str, value: Any, ttl: float | None = None) -> None:
        self._data[key] = value
        self._expiry[key] = time.time() + (ttl or self._ttl)

    def get(self, key: str) -> Any | None:
        if key not in self._data:
            return None
        if time.time() > self._expiry.get(key, 0):
            del self._data[key]
            del self._expiry[key]
            return None
        return self._data[key]

    def delete(self, key: str) -> bool:
        if key in self._data:
            del self._data[key]
            del self._expiry[key]
            return True
        return False

    def clear(self) -> None:
        self._data.clear()
        self._expiry.clear()

    def keys(self) -> list[str]:
        now = time.time()
        valid = [k for k in self._data if now <= self._expiry.get(k, 0)]
        return list(valid)

    def snapshot(self) -> dict[str, Any]:
        now = time.time()
        return {k: v for k, v in self._data.items() if now <= self._expiry.get(k, 0)}

    @property
    def size(self) -> int:
        return len(self.keys())

    def prune_expired(self) -> int:
        now = time.time()
        expired = [k for k in self._data if now > self._expiry.get(k, 0)]
        for k in expired:
            del self._data[k]
            del self._expiry[k]
        return len(expired)


class SessionContextRegistry:
    def __init__(self) -> None:
        self._sessions: dict[str, ShortTermMemory] = {}

    def get_session(self, session_id: str) -> ShortTermMemory:
        if session_id not in self._sessions:
            self._sessions[session_id] = ShortTermMemory()
        return self._sessions[session_id]

    def remove_session(self, session_id: str) -> None:
        self._sessions.pop(session_id, None)

    def prune_all(self) -> int:
        total = 0
        for mem in self._sessions.values():
            total += mem.prune_expired()
        return total
