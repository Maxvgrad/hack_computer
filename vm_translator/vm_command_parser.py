from vm_translator.command import Pop
from vm_translator.command import Push
from vm_translator.command import Arithmetic
from vm_translator.command import IfGoto
from vm_translator.command import Goto
from vm_translator.command import Label
from vm_translator.command import Unsupported


class VmCommandParser:

    def parse(self, line, path):
        elements = line.split()
        if len(elements) >= 1:
            operator = elements[0]
        else:
            operator = ''

        if operator == 'pop':
            return Pop(elements[1], elements[2], line, path)
        elif operator == 'push':
            return Push(elements[1], elements[2], line, path)
        elif operator in arithmetic_operators:
            return Arithmetic(operator, line)
        elif operator == 'label':
            return Label(line)
        elif operator == 'goto':
            return Goto(line)
        elif operator == 'if-goto':
            return IfGoto(line)
        return Unsupported(line)


arithmetic_operators = [
    'add',
    'sub',
    'neg',
    'eq',
    'gt',
    'lt',
    'and',
    'or',
    'not'
]