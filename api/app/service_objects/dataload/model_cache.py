class ModelCache():
    def __init__(self):
        self.cache = {}

    def lookup(self, type, key):
        if type in self.cache.keys():
            if key in self.cache[type].keys():
                return self.cache[type][key]

        return None

    def insert(self, type, key, value):
        if type in self.cache.keys():
            self.cache[type][key] = value
        else:
            self.cache[type] = {
                key: value
            }

        return self.cache[type][key]

    def lookup_or_insert(self, type, key, value):
        existing = self.lookup(type, key)
        if existing:
            return existing

        return self.insert(type, key, value)

    def keygen(self, params):
        params = map(lambda p: str(p), params)

        return '->'.join(params)
