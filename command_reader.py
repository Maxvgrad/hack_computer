

#TODO How to create an interface?
class CommandReader:

    def __init__(self, reader) -> None:
        super().__init__()
        self.reader = reader

    def has_next(self):
        return self.reader.has_next() and self.reader.next() is not None

    def next(self):
        return self.reader.next()
