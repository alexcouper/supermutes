import inspect

from supermutes.register import register


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


class RegisterMetaClass(type):
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
            for base in bases:
                if issubclass(base, SuperMutable):
                    supermute = get_supermute_ancestor(cls)
                    map_to_class = get_mutable_type(supermute)
                    register(supermute.__module__, map_to_class, cls)
                    return
        except NameError:
            pass
        return


RegisterClass = RegisterMetaClass('RegisterClass', (object, ), {})
# In python3 we would need to use
# class SuperMutable(object, metaclass=RegisterMetaClass)
# and in python2.6 we would need to use the var
# __metaclass__
# Declaring RegisterClass in this way makes the code work on both 3.2 and 2.6


class SuperMutable(RegisterClass):

    def mutate(self, value):
        raise NotImplementedError("Mutate() must be implemented on"
                                  " SuperMutable objects")

    def __setitem__(self, key, value):
        super(SuperMutable, self).__setitem__(key, self.mutate(value))
