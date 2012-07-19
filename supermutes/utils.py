def get_new_obj(register, obj):
    for old_class, new_class in register.items():
        if isinstance(obj, old_class) and not isinstance(obj, new_class):
            return new_class(obj)
    return obj


def get_class_registrar(super_name, map_to_class, registration_func):
    class RegisterClass(type):
        """
        A metaclass used for registering any subclass as the main converter

        If this is used as a metaclass, then upon declaring a class that
        inherits from a class named ``super_name``, ``registration_func`` will
        be called with ``map_to_class`` and the cls currently being declared.
        """
        def __init__(cls, name, bases, attrs):
            try:
                base_names = [c.__name__ for c in bases]
                if super_name in base_names:
                    registration_func(map_to_class, cls)
            except NameError:
                return
    return RegisterClass
