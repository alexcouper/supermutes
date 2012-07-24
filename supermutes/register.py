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
