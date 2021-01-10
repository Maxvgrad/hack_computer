class FileReader:

    def __init__(self, path, parser):
        self.path = path
        self.file = open(path, 'r')
        self.lines = self.file.readlines()
        self.line_pointer = 0
        self.total_lines = len(self.lines)
        self.line = None
        self.cache = None
        self.parser = parser

    def has_next(self):
        if len(self.lines) > 0:
            self.line = self.lines.pop(0)
            self.cache = None
            return True
        return False

    def next(self):
        if self.cache is None:
            self.cache = self.parser.parse(self.line, self.path)
        return self.cache
