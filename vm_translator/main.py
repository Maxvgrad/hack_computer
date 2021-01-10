from file_reader import FileReader
from file_writer import FileWriter
from vm_translator.vm_command_parser import VmCommandParser
from command_reader import CommandReader
import vm_translator.command_translator
from handler_registry import HandlerRegistry
import sys
import os


def main(read_path, output_path, is_debug):
    validate_read_path(read_path)

    translator_registry = HandlerRegistry([
        vm_translator.command_translator.ArithmeticCommandTranslator(),
        vm_translator.command_translator.PopCommandTranslator(),
        vm_translator.command_translator.PushCommandTranslator(),
        vm_translator.command_translator.DummyTranslator(),
    ])

    parser = CommandReader(FileReader(read_path, VmCommandParser()))
    writer = FileWriter(output_path)
    while parser.has_next():
        command = parser.next()
        translator = translator_registry.find(command.command_type)
        assembler_lines = translator.handle(command)
        if is_debug and len(assembler_lines) > 0:
            writer.write(make_comment(command.line))
        for assembler_line in assembler_lines:
            writer.write_ln(assembler_line)


def validate_read_path(path):
    if path[-2:] != 'vm':
        raise AssertionError()
    return True


def make_comment(line):
    return '// ' + line






# for dir_name, subdirList, file_list in os.walk(root):
#     print('Directory: %s' % dir_name)
#     for fname in file_list:
#         if fname[-3:] == 'asm':
#             print('\t%s' % fname)
#             main(root, dir_name + '/' + fname, False)

root = sys.argv[1]
read = sys.argv[1]

# for dir_name, subdirList, file_list in os.walk(root):
#     print('Directory: %s' % dir_name)
#     for fname in file_list:
#         if fname[-2:] == 'vm':
#             print('\t%s' % fname)
#             read = dir_name + '/' + fname
#             main(read, read.replace('.vm', '.asm'), True)


main(read, read.replace('.vm', '.asm'), True)
