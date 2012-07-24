from copy import deepcopy
from nose.tools import assert_equals, assert_true, assert_false

from supermutes.readonly import (
    ReadOnlyClassException, readonly, ReadOnlyList, reset_mapping
    )


def test_blocks_write_to_dict():
    d = readonly({'a': 2})
    raised = False
    try:
        d['b'] = 3
    except ReadOnlyClassException:
        raised = True
    assert_true(raised)


def test_blocks_write_to_sub_dict():
    d = readonly({'a': {'sub_dict': 3}})
    raised = False
    try:
        d['a']['sub_dict_2'] = 3
    except ReadOnlyClassException:
        raised = True
    assert_true(raised)


def test_blocks_write_to_list():
    d = readonly([1, 2, 3, 4, 5])
    raised = False
    try:
        d[2] = "hello"
    except ReadOnlyClassException:
        raised = True
    assert_true(raised)

    try:
        del d[2]
    except ReadOnlyClassException:
        raised = True
    assert_true(raised)

    try:
        del d[0:1]
    except ReadOnlyClassException:
        raised = True
    assert_true(raised)

    try:
        d[0:1] = [1, 2]
    except ReadOnlyClassException:
        raised = True
    assert_true(raised)

    for method, args in [
                        (d.append, ("hello",)),
                        (d.insert, (3, "hello")),
                        (d.pop, ()),
                        (d.reverse, ()),
                        (d.sort, ()),
                        (d.extend, ([1, 2, 3]))
                        ]:
        raised = False
        try:
            method(*args)
        except ReadOnlyClassException:
            raised = True
        assert_true(raised)


def test_blocks_write_to_sub_list():
    d = readonly([[1, 2, 3, 4, 5]])
    raised = False
    try:
        d[0][2] = "hello"
    except ReadOnlyClassException:
        raised = True
    assert_true(raised)


def test_can_read_everything():
    d = readonly({'s': [1, 2, 3, 4, 5], 'a': 2})
    assert_equals(2, d['a'])
    assert_equals(3, d['s'][2])


def test_blocks_write_during_iterate_through_list():
    d = readonly([{'s': [1, 2, 3, 4, 5], 'a': 2}])
    for item in d:
        raised = False
        try:
            item['new'] = False
        except ReadOnlyClassException:
            raised = True
        assert_true(raised)


def test_writes_during_iterate_through_dict_dont_matter():
    d = readonly([{'s': [1, 2, 3, 4, 5], 'a': [2]}])

    for key, value in d[0].items():
        before = deepcopy(value)
        value.append(3)
        assert_equals(before, d[0][key])
    #TODO: make this work.


def test_blocks_writes_on_mix_of_dicts_and_lists():
    d = readonly({
        'list_of_dicts': [
            {'key': 'val'},
        ],
        'dict_of_lists': {
            "a": ["something", "here"],
        }
    })
    raised = False
    try:
        d['dict_of_lists']['a'].append(3)
    except ReadOnlyClassException:
        raised = True
    assert_true(raised)

    raised = False
    try:
        d['list_of_dicts'][0].append(3)
    except ReadOnlyClassException:
        raised = True
    assert_true(raised)

    raised = False
    try:
        print(type(['list_of_dicts'][0]))
        d['list_of_dicts'][0]['g'] = 2
    except ReadOnlyClassException:
        raised = True
    assert_true(raised)


def test_defining_inherited_classes_alters_mapping():
    """
    Test that we can safely define inherited classes and they will be used.
    """
    class MySubClass(ReadOnlyList):
        pass

    rl = readonly([[0]])
    assert_true(isinstance(rl, MySubClass))
    assert_true(isinstance(rl[0], MySubClass))

    reset_mapping()
    # Confirm reset has worked
    rl = readonly([[0]])
    assert_false(isinstance(rl, MySubClass))
    assert_false(isinstance(rl[0], MySubClass))


def test_get_writable_version_of_the_object():
    """
    Test get_writable returns a fully writable version of the mutable.
    """
    d = readonly({
        'list_of_dicts': [
            {'key': 'val'},
        ],
        'dict_of_lists': {
            "a": ["something", "here"],
        }
    })

    # Check that no exceptions are raised:
    w = d.get_writable()
    w['new_key'] = 3
    w['list_of_dicts'].append('another item')
    w['list_of_dicts'][0]['another_key'] = 'another_value'
    w['dict_of_lists']['b'] = []
    w['dict_of_lists']['a'].append('new one')

    # Check that:
    #   a) the original readonly doesn't contain any of these values
    #   b) new ``writable`` objects don't contain any of these values

    for o in [d, d.get_writable()]:
        assert_false('new_key' in o)
        assert_false('another item' in o['list_of_dicts'])
        assert_false('another_key' in o['list_of_dicts'][0])
        assert_false('b' in o['dict_of_lists'])
        assert_false('new_one' in o['dict_of_lists']['a'])
