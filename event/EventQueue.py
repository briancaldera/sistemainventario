from event.EventSubscriber import EventSubscriber


class EventQueue:

    _instance = None

    @staticmethod
    def get_instance():
        if EventQueue._instance is None:
            EventQueue._instance = EventQueue()

        return EventQueue._instance

    def __init__(self):
        self.subscribers: dict[str: list] = {}

    def subscribe(self, subscriber: EventSubscriber, topic: str):
        if topic not in self.subscribers:
            self.subscribers[topic] = []

        self.subscribers[topic].append(subscriber)

    def publish(self, message, topic: str):
        if topic in self.subscribers:
            for subscriber in self.subscribers[topic]:
                subscriber.receive(message)
