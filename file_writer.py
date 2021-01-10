
class FileWriter:

    def __init__(self, file_path) -> None:
        super().__init__()
        self.file = open(file_path, 'w')
        self.is_first_line = True

    def write(self, line):
        self.file.write(line)

    def write_ln(self, line):
        self.file.write(line)
        self.file.write(new_line())


def new_line():
    return '\n'
