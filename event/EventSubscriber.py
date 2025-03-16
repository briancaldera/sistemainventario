from abc import ABC, abstractmethod

class EventSubscriber(ABC):
    @abstractmethod
    def receive(self, message: str):
        pass