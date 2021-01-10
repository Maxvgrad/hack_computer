from assembler import Translator


#todo: difference between abstract factory and factory method
class TranslatorFactory:

    def __init__(self, translators) -> None:
        self.translators = translators

    def find_translator(self, element_type) -> Translator:
        for translator in self.translators:
            if translator.can_handle(element_type):
                return translator
        return None
