"""
In-Process Event Bus
Free alternative to Amazon EventBridge.
Simple pub/sub pattern for decoupling services.
"""
import asyncio
import logging
from typing import Callable, Dict, List, Any
from collections import defaultdict

logger = logging.getLogger(__name__)


class EventBus:
    """Simple event bus for decoupled service communication."""

    def __init__(self):
        self._handlers: Dict[str, List[Callable]] = defaultdict(list)

    def subscribe(self, event_type: str, handler: Callable):
        """Subscribe a handler to an event type."""
        self._handlers[event_type].append(handler)
        logger.info(f"Handler subscribed to event: {event_type}")

    def unsubscribe(self, event_type: str, handler: Callable):
        """Unsubscribe a handler from an event type."""
        if handler in self._handlers[event_type]:
            self._handlers[event_type].remove(handler)

    async def publish(self, event_type: str, data: Dict[str, Any]):
        """Publish an event to all subscribed handlers."""
        handlers = self._handlers.get(event_type, [])
        logger.info(f"Publishing event: {event_type} to {len(handlers)} handlers")

        for handler in handlers:
            try:
                if asyncio.iscoroutinefunction(handler):
                    await handler(data)
                else:
                    handler(data)
            except Exception as e:
                logger.error(f"Error in event handler for {event_type}: {e}")


# Event type constants (matching design doc)
class Events:
    VOICE_REQUEST = "voice.request"
    FARM_REGISTERED = "farm.registered"
    SATELLITE_DATA_READY = "satellite.data_ready"
    VERIFICATION_REQUESTED = "verification.requested"
    VERIFICATION_COMPLETE = "verification.complete"
    TRAFFIC_LIGHT_GREEN = "traffic_light.green"
    TRAFFIC_LIGHT_YELLOW = "traffic_light.yellow"
    TRAFFIC_LIGHT_RED = "traffic_light.red"
    PAYMENT_APPROVED = "payment.approved"
    PAYMENT_PROCESSED = "payment.processed"
    THRESHOLD_BREACH = "threshold.breach"
    ALERT_GENERATED = "alert.generated"


# Global event bus instance
event_bus = EventBus()
