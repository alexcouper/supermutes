from collections import defaultdict
import inspect

CLASS_REGISTER = defaultdict(dict)


def get_new_obj(obj):
    frm = inspect.stack()[1]
    module = inspect.getmodule(frm[0]).__name__
    register = CLASS_REGISTER[module]
    for old_class, new_class in register.items():
        if isinstance(obj, old_class) and not isinstance(obj, new_class):
            return new_class(obj)
    return obj


def register(module, old_class, new_class):
    CLASS_REGISTER[module][old_class] = new_class


def get_class_registrar(super_name, map_to_class):
    class RegisterClass(type):
        """
        A metaclass used for registering any subclass as the main converter

        If this is used as a metaclass, then upon declaring a class that
        inherits from a class named ``super_name``, ``register`` will
        be called with ``map_to_class`` and the cls currently being declared.
        """
        def __init__(cls, name, bases, attrs):
            try:
                for c in bases:
                    if super_name == c.__name__:
                        register(c.__module__, map_to_class, cls)

            except NameError:
                return
    return RegisterClass
