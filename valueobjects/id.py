from dataclasses import dataclass

@dataclass
class Id:

    def __init__(self, id: int):

        if id < 0:
            raise Exception('ID no puede ser negativo')

        self.id = id
