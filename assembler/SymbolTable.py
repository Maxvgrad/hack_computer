

class SymbolTable:
    table = {} #todo: why i assign by default?
    n = 16 #todo: handle

    def add(self, key, value):
        self.table[key] = value #todo: how to add put k v in dict?

    def contains(self, key):
        return bool(self.table.get(key))

    def assign(self, key):
        self.table[key] = self.get_and_increment()

    def get(self, key):
        return self.table[key]

    def get_and_increment(self):
        tmp = self.n
        self.n += 1
        return tmp
