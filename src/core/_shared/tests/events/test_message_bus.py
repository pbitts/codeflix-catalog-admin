from dataclasses import dataclass
from unittest.mock import create_autospec

from src.core._shared.application.handler import Handler
from src.core._shared.events.event import Event
from src.core._shared.events.message_bus import MessageBus


@dataclass(frozen=True)
class DummyEvent(Event):
    name: str = "dummy"


class TestMessageBus:
    def test_calls_handler_with_message(self) -> None:
        dummy_handler = create_autospec(Handler)
        message_bus = MessageBus()
        event = DummyEvent()

        message_bus.handlers[type(event)] = [dummy_handler]
        message_bus.handle([event])

        dummy_handler.handle.assert_called_once_with(event)
    
    def test_calls_multiple_handlers_with_message(self) -> None:
        dummy_handler1 = create_autospec(Handler)
        dummy_handler2 = create_autospec(Handler)
        message_bus = MessageBus()
        event = DummyEvent()

        message_bus.handlers[type(event)] = [dummy_handler1, dummy_handler2]
        message_bus.handle([event])

        dummy_handler1.handle.assert_called_once_with(event)
        dummy_handler2.handle.assert_called_once_with(event)