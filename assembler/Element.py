from assembler.ElementType import ElementType #todo: how does import work?


class Element:

    def __init__(self, element_type, is_instruction, comment) -> None:
        self.type = element_type
        self.is_instruction = is_instruction
        self.comment = comment


class CInstruction(Element):

    def __init__(self, comp, dest, jump, comment) -> None:
        super().__init__(ElementType.C_INSTRUCTION, True, comment)
        self.comp = comp
        self.dest = dest
        self.jump = jump


class AInstruction(Element):

    def __init__(self, decimal_address, comment) -> None:
        super().__init__(ElementType.A_INSTRUCTION, True, comment)
        self.decimal_address = decimal_address


class Label(Element):

    def __init__(self, label, address) -> None:
        super().__init__(ElementType.LABEL, False, None)
        self.label = label
        self.address = address


class Unsupported(Element):

    def __init__(self, line) -> None:
        super().__init__(ElementType.UNSUPPORTED, False, None)
        self.line = line


class WhiteSpace(Unsupported):

    def __init__(self, line) -> None:
        super().__init__(line)
