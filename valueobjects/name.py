from dataclasses import dataclass

@dataclass
class Name:

    def __init__(self, name: str):

        name = name.strip()

        if name == '':
            raise Exception('Nombre no puede estar vacío')

        self.name = name
