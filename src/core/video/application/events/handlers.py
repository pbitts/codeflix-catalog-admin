from src.core._shared.application.handler import Handler
from src.core._shared.events.event_dispatcher import EventDispatcher
from src.core.video.application.events.integration_events import AudioVideoMediaUpdatedIntegrationEvent


class PublishAudioVideoMediaUpdatedHandler:
    def __init__(self, event_dispatcher: EventDispatcher):
        self.event_dispatcher = event_dispatcher

    def handle(self, event: AudioVideoMediaUpdatedIntegrationEvent) -> None:
        print(f"Dispatching integration event {event}")
        self.event_dispatcher.dispatch(event)

