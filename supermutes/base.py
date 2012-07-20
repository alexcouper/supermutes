import inspect

from register import register


def get_supermute_ancestor(cls):
    if SuperMutable in cls.__bases__:
        return cls
    for base in cls.__bases__:
        ancestor = get_supermute_ancestor(base)
        if ancestor:
            return ancestor


def get_mutable_type(cls):
    for mutable in [dict, list, set]:
        if mutable in inspect.getmro(cls):
            return mutable


class RegisterClass(type):
    """
    A metaclass used for registering any subclass as the main converter

    If it is the SuperMutable obj - don't worry too much it'll raise
    a NameError and that'll be all

    If it is an inherited class anywhere down from (and including)
    a supermute, then we need to find which kind of supermute it is so we can
    register against the appropriate module and mutable type.
    """
    def __init__(cls, name, bases, attrs):
        try:
            if issubclass(bases[0], SuperMutable):
                supermute = get_supermute_ancestor(cls)
                map_to_class = get_mutable_type(supermute)
                register(supermute.__module__, map_to_class, cls)

        except NameError:
            pass
        return


class SuperMutable(object):
    __metaclass__ = RegisterClass
