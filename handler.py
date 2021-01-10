from vm_translator.command import CommandType


class Handler:

    def __init__(self, payload_types) -> None:
        super().__init__()
        self.payload_types = payload_types

    def can_handle(self, payload_type):
        return payload_type in self.payload_types

    def handle(self, payload):
        return None