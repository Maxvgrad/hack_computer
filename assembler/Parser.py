from assembler import Element
from assembler.Element import AInstruction
from assembler.Element import CInstruction
from assembler.Element import Unsupported
from assembler.Element import Label
from assembler.Element import WhiteSpace


class Parser:

    def __init__(self, path, symbol_table):
        self.symbol_table = symbol_table
        self.file = open(path, 'r')
        self.address = 0
        self.line = None

    def has_next(self):
        line = self.file.readline()
        self.line = line.rstrip('\n').lstrip()
        return bool(line)

    def next(self):
        element = self.parse(self.line)
        if element.is_instruction:
            self.address += 1
        return element

    def parse(self, line) -> Element:
        if is_white_space(line):
            return WhiteSpace(line)
        elif line[0] == '@':
            return create_a_instruction(self.parse_address(line), self.create_comment(line))
        elif is_c_instruction(line):
            return self.create_c_instruction(line)
        elif line[0] == '(':
            return create_label(parse_label(line), self.address)
        else:
            return Unsupported(line)

    def create_c_instruction(self, line):
        dest = None
        jump = None
        instruction = parse_instruction(line)
        if ';' in instruction:
            jump = parse_jump(instruction).rstrip()
            instruction = instruction.split(';')[0]
        if '=' in instruction:
            dest = parse_dest(instruction)
            instruction = instruction.split('=')[1]
        return CInstruction(dest=dest, comp=instruction, jump=jump, comment=self.create_comment(line))

    def parse_address(self, line):
        return line[1:].split()[0]

    def parse_raw_address(self, raw_address):
        decimal_address = raw_address
        if not raw_address.isnumeric():
            variable = raw_address
            if not self.symbol_table.contains(variable):
                self.symbol_table.assign(variable)
            decimal_address = self.symbol_table.get(variable)
        return decimal_address

    def create_comment(self, line):
        return '// ' + line + ' [' + str(self.address) + ']'


def create_a_instruction(address, comment) -> AInstruction:
    return AInstruction(address, comment)


def create_label(label, address):
    return Label(label, address)


def parse_label(line):
    return line.split()[0][1:][:-1]


def parse_dest(line):
    return line.split('=')[0].rstrip()


def parse_jump(line):
    return line.split(';')[1].rstrip()


def parse_instruction(line):
    return line.split('//')[0].rstrip()


def is_c_instruction(line):
    line_without_comment = line.split('//')[0]
    return line_without_comment and '@' not in line_without_comment and '(' not in line_without_comment


def is_white_space(line):
    return len(line) == 0 or line == '\n'
