import asyncio
import logging
from collections import defaultdict
from typing import Any, Callable, Coroutine

from src.events.models import Event

logger = logging.getLogger("events")

Handler = Callable[[Event], Coroutine[Any, Any, None]]


class EventBus:
    def __init__(self) -> None:
        self._subscribers: dict[str, list[Handler]] = defaultdict(list)

    def subscribe(self, event_type: str, handler: Handler) -> None:
        self._subscribers[event_type].append(handler)
        logger.debug("Subscribed to %s: %s", event_type, handler.__name__)

    def unsubscribe(self, event_type: str, handler: Handler) -> None:
        self._subscribers[event_type].remove(handler)

    async def publish(self, event: Event) -> None:
        logger.debug("Publishing: %s", event.type)
        for handler in self._subscribers.get(event.type, []):
            try:
                await handler(event)
            except Exception as e:
                logger.error("Handler %s failed on %s: %s", handler.__name__, event.type, e)

    def subscriber_count(self, event_type: str | None = None) -> int:
        if event_type:
            return len(self._subscribers.get(event_type, []))
        return sum(len(h) for h in self._subscribers.values())


_bus: EventBus | None = None


def get_bus() -> EventBus:
    global _bus
    if _bus is None:
        _bus = EventBus()
    return _bus


def reset_bus() -> None:
    global _bus
    _bus = None
