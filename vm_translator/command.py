from enum import Enum


class CommandType(Enum):
    C_ARITHMETIC = "C_ARITHMETIC",
    C_PUSH = "C_PUSH",
    C_POP = "C_POP",
    C_LABEL = "C_LABEL",
    C_GOTO = "C_GOTO",
    C_IF = "C_IF",
    C_FUNCTION = "C_FUNCTION",
    C_RETURN = "C_RETURN",
    C_CALL = "C_CALL"


# TODO: What is toString method?
class Command:
    def __init__(self, command_type, line) -> None:
        super().__init__()
        self.command_type = command_type
        self.line = line


class MemoryAccess(Command):

    def __init__(self, command_type, segment, operand, line, path) -> None:
        super().__init__(command_type, line)
        self.segment = segment
        self.operand = operand
        self.file_name = path.split('/')[-1].split('.')[0]

    def is_local(self):
        return self.segment == 'local'

    def is_argument(self):
        return self.segment == 'argument'

    def is_this(self):
        return self.segment == 'this'

    def is_that(self):
        return self.segment == 'that'

    def is_segment_has_pointer(self):
        return self.is_local() or self.is_argument() or self.is_that() or self.is_this()

    def is_constant(self):
        return self.segment == 'constant'

    def is_static(self):
        return self.segment == 'static'

    def is_temp(self):
        return self.segment == 'temp'

    def is_pointer(self):
        return self.segment == 'pointer'


class Push(MemoryAccess):
    def __init__(self, segment, operand, line, path) -> None:
        super().__init__(CommandType.C_PUSH, segment, operand, line, path)


class Pop(MemoryAccess):
    def __init__(self, segment, operand, line, path) -> None:
        super().__init__(CommandType.C_POP, segment, operand, line, path)


class Arithmetic(Command):
    def __init__(self, operator, line) -> None:
        super().__init__(CommandType.C_ARITHMETIC, line)
        self.operator = operator

    def is_add(self):
        return self.operator == 'add'

    def is_sub(self):
        return self.operator == 'sub'

    def is_neg(self):
        return self.operator == 'neg'

    def is_eq(self):
        return self.operator == 'eq'

    def is_gt(self):
        return self.operator == 'gt'

    def is_lt(self):
        return self.operator == 'lt'

    def is_and(self):
        return self.operator == 'and'

    def is_or(self):
        return self.operator == 'or'

    def is_not(self):
        return self.operator == 'not'


class Branching(Command):
    def __init__(self, command_type, line) -> None:
        super().__init__(command_type, line)

    def is_label(self):
        return self.command_type == CommandType.C_LABEL

    def is_goto(self):
        return self.command_type == CommandType.C_GOTO

    def is_if_goto(self):
        return self.command_type == CommandType.C_IF


class IfGoto(Branching):
    def __init__(self, line) -> None:
        super().__init__(CommandType.C_IF, line)


class Goto(Branching):
    def __init__(self, line) -> None:
        super().__init__(CommandType.C_GOTO, line)


class Label(Branching):
    def __init__(self, line) -> None:
        super().__init__(CommandType.C_LABEL, line)


class Unsupported(Command):
    def __init__(self, line) -> None:
        super().__init__(None, line)
