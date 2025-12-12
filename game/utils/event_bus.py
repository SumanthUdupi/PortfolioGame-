from typing import Callable, Dict, List, Any

class EventBus:
    """
    A simple Event Bus implementation for the publish-subscribe pattern.
    """
    def __init__(self):
        self._subscribers: Dict[str, List[Callable[[Any], None]]] = {}

    def subscribe(self, event_type: str, callback: Callable[[Any], None]) -> None:
        """
        Subscribe to an event type.
        """
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(callback)

    def unsubscribe(self, event_type: str, callback: Callable[[Any], None]) -> None:
        """
        Unsubscribe from an event type.
        """
        if event_type in self._subscribers:
            if callback in self._subscribers[event_type]:
                self._subscribers[event_type].remove(callback)

    def publish(self, event_type: str, data: Any = None) -> None:
        """
        Publish an event to all subscribers.
        """
        if event_type in self._subscribers:
            for callback in self._subscribers[event_type]:
                callback(data)
