

class Computable:
    def compute(self, assembler_instructions):
        return None


class AssignmentStatement(Computable):
    def __init__(self, dest, value) -> None:
        super().__init__()
        self.dest = dest
        self.value = value

    def compute(self, assembler_instructions):
        v_data = self.value.compute(assembler_instructions)
        assembler_instructions.c_instruction('D=' + v_data)
        d_data = self.dest.compute(assembler_instructions)
        assembler_instructions.c_instruction(d_data + '=D')


class Compute(Computable):
    def __init__(self, left_operand, operator, right_operand) -> None:
        super().__init__()
        self.left_operand = left_operand
        self.operator = operator
        self.right_operand = right_operand
        self.data = 'D'

    def compute(self, assembler_instructions):
        l_data = self.left_operand.compute(assembler_instructions)
        assembler_instructions.c_instruction('D=' + l_data)

        r_data = self.right_operand.compute(assembler_instructions)
        assembler_instructions.c_instruction('D=D' + self.operator + r_data)
        return self.data


class PlusCompute(Compute):
    def __init__(self, left_operand, right_operand) -> None:
        super().__init__(left_operand, '+', right_operand)


class MinusCompute(Compute):
    def __init__(self, left_operand, right_operand) -> None:
        super().__init__(left_operand, '-', right_operand)


class Neg(Computable):

    def __init__(self, computable) -> None:
        super().__init__()
        self.computable = computable

    def compute(self, assembler_instructions):
        data = self.computable.compute(assembler_instructions)
        assembler_instructions.c_instruction(data + '=-' + data)
        return data


class Not(Computable):

    def __init__(self, computable) -> None:
        super().__init__()
        self.computable = computable

    def compute(self, assembler_instructions):
        data = self.computable.compute(assembler_instructions)
        assembler_instructions.c_instruction(data + '=!' + data)
        return data


class Number(Computable):

    def __init__(self, name) -> None:
        super().__init__()
        self.name = name
        self.data = 'A'

    def assign_to_data_register_instructions(self, assembler_instructions):
        assembler_instructions.a_instruction(self.name)
        assembler_instructions.c_instruction('D=A')

    def compute(self, assembler_instructions):
        assembler_instructions.a_instruction(str(self.name))
        return self.data


class Variable(Computable):
    def __init__(self, name) -> None:
        super().__init__()
        self.name = name
        self.data = 'M'

    def compute(self, assembler_instructions):
        assembler_instructions.a_instruction(self.name)
        return self.data


class Pointer(Computable):
    def __init__(self, computable) -> None:
        super().__init__()
        self.computable = computable
        self.data = 'M'

    def compute(self, assembler_instructions):
        data = self.computable.compute(assembler_instructions)
        assembler_instructions.c_instruction('A=' + data)
        return self.data


class Incr(Computable):
    def __init__(self, computable) -> None:
        super().__init__()
        self.computable = computable

    def compute(self, assembler_instructions):
        self.computable.compute(assembler_instructions)
        assembler_instructions.c_instruction('M=M+1')


class Decr(Computable):
    def __init__(self, computable) -> None:
        super().__init__()
        self.computable = computable

    def compute(self, assembler_instructions):
        self.computable.compute(assembler_instructions)
        assembler_instructions.c_instruction('M=M-1')


#TODO: Remove
class LabelCounter:
    value = 1


def increment_and_get():
    tmp = LabelCounter.value
    LabelCounter.value += 1
    return str(tmp)


class Compare(Computable):
    def __init__(self, left, right, jump) -> None:
        self.left = left
        self.right = right
        self.label = 'labelName' + increment_and_get()
        self.result = 'result'
        self.result = 'result'
        self.data = 'M'
        self.jump = jump

    def compute(self, assembler_instructions):

        l_data = self.left.compute(assembler_instructions)
        assembler_instructions.c_instruction('D=' + l_data)

        r_data = self.right.compute(assembler_instructions)
        assembler_instructions.c_instruction('D=D-' + r_data)

        assembler_instructions.a_instruction(self.result)
        assembler_instructions.c_instruction('M=-1') #true

        assembler_instructions.a_instruction(self.label)
        assembler_instructions.c_instruction(self.jump)

        assembler_instructions.a_instruction(self.result)
        assembler_instructions.c_instruction('M=0') #false

        assembler_instructions.label(self.label)
        assembler_instructions.a_instruction(self.result)
        return self.data


class Gt(Compare):
    def __init__(self, left, right) -> None:
        super().__init__(left, right, 'D;JGT')


class Lt(Compare):
    def __init__(self, left, right) -> None:
        super().__init__(left, right, 'D;JLT')


class Eq(Compare):
    def __init__(self, left, right) -> None:
        super().__init__(left, right, 'D;JEQ')

