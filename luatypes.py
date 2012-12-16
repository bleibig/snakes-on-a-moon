class LuaTable:
    def __init__(self, array=None, hash=None):
        self.array = array or []
        self.hash = hash or {}
        self.metatable = None

    def __getitem__(self, key):
        if isinstance(key, (int, long, float)) and int(key) == key and key > 0:
            key = int(key)
            return self.array[key-1] if len(self.array) >= key else None
        else:
            return self.hash[key] if key in self.hash else None

    def __setitem__(self, key, value):
        if isinstance(key, (int, long, float)) and int(key) == key and key > 0:
            key = int(key)
            while key > len(self.array):
                self.array.append(None)
            self.array[key-1] = value
        else:
            self.hash[key] = value

    def __str__(self):
        return 'LuaTable #array={} #hash={}'.format(
            len(self.array), len(self.hash))

    def __repr__(self):
        return 'LuaTable(array={}, hash={})'.format(self.array, self.hash)

    def __len__(self):
        return len(self.array)

class LuaValue:
    def __init__(self, value):
        # the internal value
        self.value = value
        # list of (closure, upvalue_index) pairs that reference this
        # value as an upvalue
        self.referencing_closures = []
