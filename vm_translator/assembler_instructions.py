

class AssemblerInstructions:

    ignore = ['D=D']

    def __init__(self) -> None:
        super().__init__()
        self.instructions = list()

    def a_instruction(self, value):
        self.instructions.append('@' + value)
        return self

    def c_instruction(self, instruction):
        self.instructions.append(instruction)
        return self

    def label(self, name):
        self.instructions.append('(' + name + ')')
        return self

    def result(self):
        result = list()
        for item in self.instructions:
            if isinstance(item, list):
                for instr in item:
                    self.append(instr, result)

            self.append(item, result)
        return result

    def append(self, instr, instructions):
        if instr not in self.ignore:
            instructions.append(instr)

