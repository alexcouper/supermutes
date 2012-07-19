"A collection of readonly immutables"
from copy import deepcopy

from supermutes.utils import get_new_obj, get_class_registrar, register

readonly = lambda obj: get_new_obj(obj)


def reset_mapping():
    register(__name__, dict, ReadOnlyDict)
    register(__name__, list, ReadOnlyList)


class ReadOnlyClassException(Exception):
    pass


class ReadOnlyBaseClass():

    def method_not_allowed(self, *args, **kwargs):
        raise ReadOnlyClassException("Cannot write to object.")

    (__setitem__, __setattr__, __delitem__, __setslice__, __delslice__,
     append, insert, pop, popitem, remove, clear, update, extend,
     reverse, sort) = (method_not_allowed,) * 15


class ReadOnlyList(ReadOnlyBaseClass, list):

    __metaclass__ = get_class_registrar("ReadOnlyList", list)

    def __getitem__(self, index):
        return readonly(list.__getitem__(self, index))

    def get_writable(self):
        "Get a fully writable version of this list"
        writable = list([])
        for item in self:
            try:
                item = item.get_writable()
            except AttributeError:
                pass
            writable.append(item)
        return deepcopy(writable)


class ReadOnlyDict(ReadOnlyBaseClass, dict):

    __metaclass__ = get_class_registrar("ReadOnlyDict", dict)

    def __getitem__(self, key):
        return readonly(dict.__getitem__(self, key))

    def get_writable(self):
        "Get a fully writable version of this dictionary"
        writable = dict({})
        for key, item in self.items():
            try:
                item = item.get_writable()
            except AttributeError:
                pass
            writable[key] = item
        return deepcopy(writable)

reset_mapping()
