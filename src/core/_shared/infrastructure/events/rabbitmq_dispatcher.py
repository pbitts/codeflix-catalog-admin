
from src.core._shared.events.event import Event
from src.core._shared.events.event_dispatcher import EventDispatcher


class RabbitMQDispatcher(EventDispatcher):
    def __init__(self, queue="videos.new") -> None:
        self.queue = queue
        
    def dispatch(self, event: Event) -> None:
        print(f"RabbitMQ Dispatching event {event}")