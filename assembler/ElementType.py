from enum import Enum


class ElementType(Enum):
    C_INSTRUCTION = 'c-instruction'
    A_INSTRUCTION = 'a-instruction'
    LABEL = 'label'
    UNSUPPORTED = 'unsupported'
