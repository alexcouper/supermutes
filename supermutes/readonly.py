"A collection of readonly immutables"


class ReadOnlyClassException(Exception):
    pass


def readonly(obj):
    if isinstance(obj, list) and not isinstance(obj, ReadOnlyList):
        return ReadOnlyList(obj)
    elif isinstance(obj, dict) and not isinstance(obj, ReadOnlyDict):
        return ReadOnlyDict(obj)
    return obj


class ReadOnlyBaseClass():

    def method_not_allowed(self, *args, **kwargs):
        raise ReadOnlyClassException("Cannot write to object.")

    __setitem__ = __setattr__ = append = insert = method_not_allowed


class ReadOnlyList(ReadOnlyBaseClass, list):

    def __getitem__(self, index):
        return readonly(list.__getitem__(self, index))


class ReadOnlyDict(ReadOnlyBaseClass, dict):

    def __getitem__(self, key):
        return readonly(dict.__getitem__(self, key))
