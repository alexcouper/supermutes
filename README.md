supermutes
==========

This project defines two kinds of mutables.

dot
---

The ``dot`` module contains classes that allow dot-notation to be used for
when accessing a ``list`` or ``dict`` object.

eg::

    >>  from supermutes.dot import dotify
    >>  d = dotify({'a':[1, 2, 3, 4, 5], 'b': {'c': 5}})
    >>  d.a._0
    1
    >>  d.b.c
    5
    >>  d.c = {'f': 9}
    >>  d.c.f
    9

readonly
--------

The ``readonly`` module contains classes that transform ``dict`` and ``list``
objects into ones that cannot have any values changed on them.

eg::

    >>  from supermutes.readonly import readonly
    >>  r = readonly({'a':[1, 2, 3, 4, 5], 'b': {'c': 5}})
    >>  r
    {'a': [1, 2, 3, 4, 5], 'b': {'c': 5}}
    >>  r['a'].append(5)
    supermutes.readonly.ReadOnlyClassException: Cannot write to object.
    >> r['b']['d'] = 6
    supermutes.readonly.ReadOnlyClassException: Cannot write to object.


Creating Sub Classes
--------------------

Upon declaration of a sub class of any of the supermutes, that class will be
set as the defacto class for recursively changing data sets.

To reset the classes back to the original set, use the ``reset_mapping`` method
inside the module

eg::

    >>> from supermutes.dot import DotDict, DotList, reset_mapping
    >>> class MySubClass(DotDict): pass
    >>> d = MySubClass({'a': {'b': {'c': 3}}})
    >>> d.a.b
    {'c': 3}
    >>> d.a.b.__class__
    <class '__main__.MySubClass'>
    >>> f = DotList([1, {}])
    >>> f[1].__class__
    <class '__main__.MySubClass'>
    >>> reset_mapping()
    >>> f = DotList([1, {}])
    >>> f[1].__class__
    <class 'supermutes.dot.DotDict'>



