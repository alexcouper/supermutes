from collections import OrderedDict


class OrderedDefaultDict(OrderedDict):

    def __init__(self, default_callable=None, *a, **kw):
        if (default_callable is not None and not callable(default_callable)):
            raise TypeError('First argument must be callable')
        OrderedDict.__init__(self, *a, **kw)
        self.default_callable = default_callable

    def __getitem__(self, key):
        try:
            return OrderedDict.__getitem__(self, key)
        except KeyError:
            return self.__missing__(key)

    def __missing__(self, key):
        if self.default_callable is None:
            raise KeyError(key)
        self[key] = value = self.default_callable()
        return value

    def copy(self):
        return type(self)(self.default_callable, self)


    def __repr__(self):
        return 'OrderedDefaultDict(%s, %s)' % (self.default_callable,
                                        OrderedDict.__repr__(self))
