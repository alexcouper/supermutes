from nose.tools import assert_equal

from supermutes.ordered import OrderedDefaultDict

def test_orders_things_in_order_inserted():
    d = OrderedDefaultDict(list)
    d['a'] = 1
    d['b'] = 2
    d[123] = 3
    assert_equal([1, 2, 3], d.values())
    assert_equal(['a', 'b', 123], d.keys())


def test_provides_defaults():
    d = OrderedDefaultDict(int)
    d['a'] += 1
    assert_equal(d['a'], 1)
    assert_equal(d['b'], 0)


def test_is_copyable():
    d = OrderedDefaultDict(int)
    d['a'] += 1
    d['b'] += 100
    assert_equal(d, d.copy())
