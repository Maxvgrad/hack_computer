from handler import Handler
from vm_translator.command import CommandType
from vm_translator.computable import Computable
from vm_translator.computable import Compute
from vm_translator.computable import AssignmentStatement
from vm_translator.computable import MinusCompute
from vm_translator.computable import PlusCompute
from vm_translator.computable import Pointer
from vm_translator.computable import Neg
from vm_translator.computable import Not
from vm_translator.computable import Variable
from vm_translator.computable import Number
from vm_translator.computable import Incr
from vm_translator.computable import Decr
from vm_translator.computable import Gt
from vm_translator.computable import Lt
from vm_translator.computable import Eq
from vm_translator.assembler_instructions import AssemblerInstructions


stack_pointer_ram_address = '@SP'
stack_pointer_var_name = 'SP'
address_var_name = 'addr'
local_ram_address = '@LCL'
address_ram_address = '@addr'
tmp_base_value = 5


class TempCounter:
    def __init__(self, temp_base) -> None:
        super().__init__()
        self.temp_base = temp_base
        self.reset()

    def next(self):
        temp_val = self.counter
        self.counter = self.counter + 1
        return Variable(str(temp_val))

    def reset(self):
        self.counter = self.temp_base


temp_provider = TempCounter(tmp_base_value)


def get_segment_variable_name(payload):
    if payload.is_local():
        return 'LCL'
    elif payload.is_argument():
        return 'ARG'
    elif payload.is_that() or (payload.is_pointer() and payload.operand == '1'):
        return 'THAT'
    elif payload.is_this() or (payload.is_pointer() and payload.operand == '0'):
        return 'THIS'
    else:
        return None


class DummyTranslator(Handler):
    def __init__(self) -> None:
        super().__init__(None)

    def handle(self, payload):
        return list()

    def can_handle(self, payload_type):
        return payload_type is None


class BaseCommandTranslator(Handler):
    def __init__(self, command_types) -> None:
        super().__init__(command_types)
        self.translator = LogicStatementToAssemblerInstructionTranslator()

    def handle(self, payload):
        statement_provider = self.find_statement_provider(payload)
        statements = statement_provider(payload)
        translator = self.translator
        for stm in statements:
            translator.translate(stm)
        return translator.result()

    def find_statement_provider(self, payload):
        return dummy_statement_provider


class BranchingCommandTranslator(BaseCommandTranslator):
    def __init__(self) -> None:
        super().__init__([CommandType.C_LABEL, CommandType.C_GOTO, CommandType.C_IF])

    def find_statement_provider(self, payload):
        if payload.is_label():
            return #TODO
        elif payload.is_goto():
            return #TODO
        elif payload.is_ifgoto():
            return #TODO


class ArithmeticCommandTranslator(BaseCommandTranslator):

    def __init__(self) -> None:
        super().__init__([CommandType.C_ARITHMETIC])

    def find_statement_provider(self, payload):
        if payload.is_add():
            return add_statement_provider
        elif payload.is_sub():
            return sub_statement_provider
        elif payload.is_neg():
            return neg_statement_provider
        elif payload.is_and():
            return and_statement_provider
        elif payload.is_or():
            return or_statement_provider
        elif payload.is_and():
            return and_statement_provider
        elif payload.is_gt():
            return gt_statement_provider
        elif payload.is_lt():
            return lt_statement_provider
        elif payload.is_eq():
            return eq_statement_provider
        elif payload.is_not():
            return not_statement_provider


def compute_statement_provider(computation_statement_provider):
    def compute_statement_provider_inner(payload):
        # SP--
        stm1 = decr_sp()

        temp1 = temp_provider.next()

        # temp1 = *SP
        stm2 = AssignmentStatement(temp1, Pointer(Variable(stack_pointer_var_name)))

        # SP--
        stm3 = decr_sp()

        computation = computation_statement_provider(payload, temp1)

        # SP++
        stm5 = incr_sp()

        return [stm1, stm2, stm3, computation, stm5]
    return compute_statement_provider_inner


def add_statement_provider(payload):
    def add_statement_provider_inner(payload, temp):
        # *SP = *SP + tmp1
        return AssignmentStatement(Pointer(Variable(stack_pointer_var_name)),
                                   PlusCompute(Pointer(Variable(stack_pointer_var_name)), temp))
    return compute_statement_provider(add_statement_provider_inner)(payload)


def sub_statement_provider(payload):
    def sub_statement_provider_inner(payload, temp):
        # *SP = *SP - tmp1
        return AssignmentStatement(Pointer(Variable(stack_pointer_var_name)),
                                   MinusCompute(Pointer(Variable(stack_pointer_var_name)), temp))
    return compute_statement_provider(sub_statement_provider_inner)(payload)


def neg_statement_provider(payload):
    # SP--
    stm1 = decr_sp()

    # *SP = !*SP
    stm2 = AssignmentStatement(Pointer(Variable(stack_pointer_var_name)), Neg(Pointer(Variable(stack_pointer_var_name))))

    # SP++
    stm3 = incr_sp()
    return [stm1, stm2, stm3]


def not_statement_provider(payload):
    # SP--
    stm1 = decr_sp()

    # *SP = !*SP
    stm2 = AssignmentStatement(Pointer(Variable(stack_pointer_var_name)), Not(Pointer(Variable(stack_pointer_var_name))))

    # SP++
    stm3 = incr_sp()

    return [stm1, stm2, stm3]


def and_statement_provider(payload):
    def and_statement_provider_inner(payload, temp):
        # *SP = *SP & tmp1
        return AssignmentStatement(Pointer(Variable(stack_pointer_var_name)),
                                   Compute(Pointer(Variable(stack_pointer_var_name)), '&', temp))
    return compute_statement_provider(and_statement_provider_inner)(payload)


def or_statement_provider(payload):
    def or_statement_provider_inner(payload, temp):
        # *SP = *SP | tmp1
        return AssignmentStatement(Pointer(Variable(stack_pointer_var_name)),
                                   Compute(Pointer(Variable(stack_pointer_var_name)), '|', temp))
    return compute_statement_provider(or_statement_provider_inner)(payload)


def gt_statement_provider(payload):
    def gt_statement_provider_inner(payload, temp):
        # *SP = *SP > tmp1
        return AssignmentStatement(Pointer(Variable(stack_pointer_var_name)),
                                   Gt(Pointer(Variable(stack_pointer_var_name)), temp))
    return compute_statement_provider(gt_statement_provider_inner)(payload)


def eq_statement_provider(payload):
    def eq_statement_provider_inner(payload, temp):
        # *SP = *SP == tmp1
        return AssignmentStatement(Pointer(Variable(stack_pointer_var_name)),
                                   Eq(Pointer(Variable(stack_pointer_var_name)), temp))
    return compute_statement_provider(eq_statement_provider_inner)(payload)


def lt_statement_provider(payload):
    def lt_statement_provider_inner(payload, temp):
        # *SP = *SP < tmp1
        return AssignmentStatement(Pointer(Variable(stack_pointer_var_name)),
                                   Lt(Pointer(Variable(stack_pointer_var_name)), temp))
    return compute_statement_provider(lt_statement_provider_inner)(payload)


class PushCommandTranslator(BaseCommandTranslator):

    def __init__(self) -> None:
        super().__init__([CommandType.C_PUSH])
        self.translator = LogicStatementToAssemblerInstructionTranslator()

    def find_statement_provider(self, payload):
        if payload.is_segment_has_pointer():
            return push_segment_with_pointer_statement_provider
        elif payload.is_constant():
            return push_constant_segment_statement_provider
        elif payload.is_static():
            return push_static_segment_statement_provider
        elif payload.is_temp():
            return push_temp_segment_statement_provider
        elif payload.is_pointer():
            return push_pointer_segment_statement_provider
        else:
            return super().find_statement_provider(payload)


def push_segment_with_pointer_statement_provider(payload):
    # addr = segment + operand
    stm1 = AssignmentStatement(Variable(address_var_name),
                               PlusCompute(Variable(get_segment_variable_name(payload)),
                                           Number(payload.operand)))
    # *SP = *addr
    stm2 = AssignmentStatement(Pointer(Variable(stack_pointer_var_name)), Pointer(Variable(address_var_name)))
    # SP++
    stm3 = incr_sp()
    return [stm1, stm2, stm3]


def push_constant_segment_statement_provider(payload):
    # *SP = i
    stm1 = AssignmentStatement(Pointer(Variable(stack_pointer_var_name)), Number(payload.operand))
    # SP++
    stm2 = incr_sp()
    return [stm1, stm2]


def push_static_segment_statement_provider(payload):
    # *SP = static_label
    stm1 = AssignmentStatement(Pointer(Variable(stack_pointer_var_name)), Variable(create_static_label(payload.file_name, payload.operand)))
    # SP++
    stm2 = incr_sp()
    return [stm1, stm2]


def push_pointer_segment_statement_provider(payload):
    # *SP = static_label
    stm1 = AssignmentStatement(Pointer(Variable(stack_pointer_var_name)), Variable(get_segment_variable_name(payload)))
    # SP++
    stm2 = incr_sp()
    return [stm1, stm2]


def push_temp_segment_statement_provider(payload):
    # addr = temp + operand
    stm1 = AssignmentStatement(Variable(address_var_name), PlusCompute(Number(tmp_base_value),
                                                                       Number(payload.operand)))
    # *SP = *addr
    stm2 = AssignmentStatement(Pointer(Variable(stack_pointer_var_name)), Pointer(Variable(address_var_name)))
    # SP++
    stm3 = incr_sp()
    return [stm1, stm2, stm3]


class PopCommandTranslator(BaseCommandTranslator):

    def __init__(self) -> None:
        super().__init__([CommandType.C_POP])

    def find_statement_provider(self, payload):
        if payload.is_segment_has_pointer():
            return pop_segment_with_pointer_statement_provider
        elif payload.is_static():
            return pop_static_statement_provider
        elif payload.is_temp():
            return pop_temp_segment_statement_provider
        elif payload.is_pointer():
            return pop_pointer_segment_statement_provider
        else:
            return super().find_statement_provider(payload)


def pop_segment_with_pointer_statement_provider(payload):
    # addr = segment + operand
    stm1 = AssignmentStatement(Variable(address_var_name),
                               PlusCompute(Variable(get_segment_variable_name(payload)),
                                           Number(payload.operand)))
    # SP--
    stm2 = decr_sp()
    # *SP = *addr
    stm3 = AssignmentStatement(Pointer(Variable(address_var_name)), Pointer(Variable(stack_pointer_var_name)))
    return [stm1, stm2, stm3]


def pop_static_statement_provider(payload):
    # SP--
    stm1 = decr_sp()
    # static_label = *SP
    stm2 = AssignmentStatement(Variable(create_static_label(payload.file_name, payload.operand)),
                               Pointer(Variable(stack_pointer_var_name)))
    return [stm1, stm2]


def pop_temp_segment_statement_provider(payload):
    return pop_temp_segment_statement_provider_inner(payload.operand)


def pop_temp_segment_statement_provider_inner(relative_address):
    # SP--
    stm1 = decr_sp()
    # addr = temp + operand
    stm2 = AssignmentStatement(Variable(address_var_name), PlusCompute(Number(tmp_base_value),
                                                                       Number(relative_address)))
    # *addr = *SP
    stm3 = AssignmentStatement(Pointer(Variable(address_var_name)), Pointer(Variable(stack_pointer_var_name)))
    return [stm1, stm2, stm3]


def pop_pointer_segment_statement_provider(payload):
    # SP--
    stm1 = decr_sp()
    # static_label = *SP
    stm2 = AssignmentStatement(Variable(get_segment_variable_name(payload)), Pointer(Variable(stack_pointer_var_name)))
    return [stm1, stm2]


def dummy_statement_provider(any):
    return list()


def incr_sp():
    return Incr(Variable(stack_pointer_var_name))


def decr_sp():
    return Decr(Variable(stack_pointer_var_name))


def create_static_label(file_name, operand):
    return file_name + '.' + str(operand)


class LogicStatementToAssemblerInstructionTranslator:

    def __init__(self) -> None:
        super().__init__()
        self.reset()

    def reset(self):
        self.assembler_instructions = AssemblerInstructions()

    def translate(self, statement):
        if isinstance(statement, Computable):
            statement.compute(self.assembler_instructions)
            temp_provider.reset()

    def result(self):
        result = self.assembler_instructions.result()
        self.reset()
        return result

