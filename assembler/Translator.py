from assembler.ElementType import ElementType


#todo: abstract class?
class Translator:

    def __init__(self) -> None:
        super().__init__()

    def can_handle(self, element_type) -> bool:
        False

    def translate(self, element) -> str:
        NotImplementedError()


class CTranslator(Translator):
    comp_table = {
        '0':'0101010',
        '1':'0111111',
        '-1':'01 1 1 0 1 0'.replace(' ', ''),
        'D':'0001100',

        # Same code (SC)
        'A':'0110000',
        'M':'1110000',

        '!D':'00 0 1 1 0 1'.replace(' ', ''),

        # SC
        '!A':'01 1 0 0 0 1'.replace(' ', ''),
        '!M':'11 1 0 0 0 1'.replace(' ', ''),

        '-D':'00 0 1 1 1 1'.replace(' ', ''),

        # SC
        '-A':'01 1 0 0 1 1'.replace(' ', ''),
        '-M':'11 1 0 0 1 1'.replace(' ', ''),

        'D+1':'0 0 1 1 1 1 1'.replace(' ', ''),

        # SC
        'A+1':'0 1 1 0 1 1 1'.replace(' ', ''),
        'M+1':'1 1 1 0 1 1 1'.replace(' ', ''),

        'D-1':'0 0 0 1 1 1 0'.replace(' ', ''),

        # SC
        'A-1':'0 1 1 0 0 1 0'.replace(' ', ''),
        'M-1':'1 1 1 0 0 1 0'.replace(' ', ''),

        # SC
        'D+A': '0 0 0 0 0 1 0'.replace(' ', ''),
        'D+M': '1 0 0 0 0 1 0'.replace(' ', ''),

        # SC
        'D-A': '00 1 0 0 1 1'.replace(' ', ''),
        'D-M': '10 1 0 0 1 1'.replace(' ', ''),

        # SC
        'A-D': '00 0 0 1 1 1'.replace(' ', ''),
        'M-D': '10 0 0 1 1 1'.replace(' ', ''),

        # SC
        'D&A': '0 0 0 0 0 0 0'.replace(' ', ''),
        'D&M': '1 0 0 0 0 0 0'.replace(' ', ''),

        # SC
        'D|A': '0 0 1 0 1 0 1'.replace(' ', ''),
        'D|M': '1 0 1 0 1 0 1'.replace(' ', ''),
    }
    dest_table = {
        None: '000',
        'M': '001',
        'D': '010',
        'MD': '011',
        'A': '100',
        'AM': '101',
        'AD': '110',
        'AMD': '111',
    }
    jump_table = {
        None: '000',
        'JGT': '001',
        'JEQ': '010',
        'JGE': '011',
        'JLT': '100',
        'JNE': '101',
        'JLE': '110',
        'JMP': '111',
    }

    def can_handle(self, element_type) -> bool:
        return ElementType.C_INSTRUCTION == element_type

    def translate(self, element) -> str:
        return '111' + self.comp_table[element.comp] + self.dest_table[element.dest] + self.jump_table[element.jump]


class ATranslator(Translator):

    def can_handle(self, element_type) -> bool:
        return ElementType.A_INSTRUCTION == element_type

    def translate(self, element) -> str:
        return '{0:016b}'.format(int(element.decimal_address))
