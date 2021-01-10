#!/usr/bin/python

from assembler.SymbolTable import SymbolTable
from assembler.Parser import Parser
from assembler.ElementType import ElementType
from assembler.Element import AInstruction
from assembler.TranslatorFactory import TranslatorFactory
from assembler.Translator import CTranslator
from assembler.Translator import ATranslator
import sys
import os


def main(root, read_path, is_debug):
    table = init_symbol_table()
    parser = Parser(read_path, table)
    translator_factory = TranslatorFactory([CTranslator(), ATranslator()])
    first_pass(parser, table)
    output_file = open(create_output_path(root, strip_extension(get_file_name(read_path))), 'w')
    second_pass(output_file, Parser(read_path, table), translator_factory, table, is_debug)


def second_pass(output_file, parser, translator_factory, table, is_debug):
    while parser.has_next():
        element = parser.next()

        #TODO: refactor
        if element.type == ElementType.A_INSTRUCTION:
            address = element.decimal_address
            if not address.isnumeric():
                variable = address
                if not table.contains(variable):
                    table.assign(variable)
                element = AInstruction(table.get(variable), element.comment)

        translator = translator_factory.find_translator(element.type)
        if translator is not None:
            if element.comment and is_debug:
                output_file.write(element.comment + '\n')

            code = translator.translate(element)
            output_file.write(code + '\n')


def create_output_path(root, file_name):
    return root + '/' + file_name + '.hack'


def get_file_name(file):
    return file.split('/')[-1]


def strip_extension(file_name):
    return file_name.split('.')[0]


def init_symbol_table():
    table = SymbolTable()
    for i in range(0, 16):
        table.add("R" + str(i), str(i))
    table.add("SCREEN", "16384")
    table.add("KBD", "24576")
    table.add("SP", "0")
    table.add("LCL", "1")
    table.add("ARG", "2")
    table.add("THIS", "3")
    table.add("THAT", "4")
    return table


def first_pass(parser, table):
    while parser.has_next():
        element = parser.next()
        element_type = element.type

        if element_type is ElementType.LABEL:
            table.add(element.label, element.address)


root = sys.argv[1]

for dir_name, subdirList, file_list in os.walk(root):
    print('Directory: %s' % dir_name)
    for fname in file_list:
        if fname[-3:] == 'asm':
            print('\t%s' % fname)
            main(root, dir_name + '/' + fname, False)



#todo: parse dir
#main(root, file)
