from nose.tools import assert_equals, assert_true

from supermutes.readonly import (
    ReadOnlyClassException, readonly
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

    raised = False
    try:
        d.append("hello")
    except ReadOnlyClassException:
        raised = True
    assert_true(raised)

    raised = False
    try:
        d.insert(3, "hello")
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
        d['list_of_dicts'][0]['g'] = 2
    except ReadOnlyClassException:
        raised = True
    assert_true(raised)
