from nose.tools import assert_equals, assert_true, assert_false, assert_raises

from supermutes.dot import DotDict, dotify, reset_mapping


def test_combination_dot():
    """
    Test that we can always have dot behaviour down a stack of objects
    """
    dd = dotify({
        "fred": 1,
        "dict_of_lists": {
            'g': ['2', '3', '4']
        },
        "list_of_dicts": [
            {'id': 2},
        ]
    })

    assert_equals(1, dd.fred)
    assert_equals('4', dd.dict_of_lists.g._2)
    assert_equals(2, dd.list_of_dicts._0.id)

    dd.dict_of_lists.h = 'another'
    assert_equals('another', dd['dict_of_lists']['h'])

    dd.list_of_dicts._0.another_key = "fred"
    assert_equals('fred', dd['list_of_dicts'][0]['another_key'])
    assert_equals(2, dd['list_of_dicts'][0]['id'])


def test_dot_list_access():
    """Test that we can access items in a ``DotList`` using dot notation"""
    dl = dotify(['fred', 'alex', 'bill'])
    assert_equals('fred', dl[0])
    assert_equals('fred', dl._0)
    assert_equals('bill', dl[2])
    assert_equals('bill', dl._2)


def test_dot_list_data_entry():
    """Test that we can add items to a ``DotList`` using dot notation"""
    dl = dotify(['fred', 'alex', 'bill'])
    dl._2 = 'bob'
    assert_equals('bob', dl[2])


def test_raises_if_assign_out_of_range():
    """
    Test that we get an exception when we insert out of range to a ``DotList``.
    """
    dl = dotify(['fred', 'alex', 'bill'])

    raised = False
    try:
        dl._10 = 'fred'
    except IndexError:
        raised = True
    assert_true(raised)


def test_can_still_assign_own_attributes():
    """
    Test that we can still assign our own attributes to a ``DotList``.
    """
    dl = dotify([])
    dl.mine = 12
    dl._hidden = 13
    assert_equals(dl, [])
    assert_equals(dl._hidden, 13)
    assert_equals(dl.mine, 12)


def test_dot_dict_equality():
    """Test the equality behaviour of ``DotDict``."""
    d = dotify({'key_one': '1'})

    # Test equality with dict
    assert_equals(d, {'key_one': '1'})


def test_dot_dict_adding_dictionaries():
    """
    Test the behaviour of adding dictionaries to ``DotDict`` objects.
    """
    d = dotify({'key_one': '1'})
    # Test adding dictionaries
    d.key_two = {'sub_key_1': ['item1', 'item2']}
    assert_equals(d,
                  {
        'key_one': '1',
        'key_two': {
            'sub_key_1': [
                'item1',
                'item2'
            ]
        }
    })


def test_dot_dict_raises_key_error_on_missing_key():
    """
    Test the behaviour of accessing missing keys in ``DotDict`` objects.
    """
    d = dotify({'key_one': '1'})
    raised = False
    try:
        d.key_two
    except KeyError:
        raised = True
    assert_true(raised)


def test_defining_inherited_classes_alters_mapping():
    """
    Test that we can safely define inherited classes and they will be used.
    """
    class MySubClass(DotDict):
        pass

    d = dotify({'a': {'b': {'c': 3}}})
    assert_true(isinstance(d, MySubClass))
    assert_true(isinstance(d['a'], MySubClass))
    assert_true(isinstance(d['a']['b'], MySubClass))

    reset_mapping()
    # Confirm reset has worked
    d = dotify({'a': {'b': {'c': 3}}})
    assert_false(isinstance(d, MySubClass))
    assert_false(isinstance(d['a'], MySubClass))
    assert_false(isinstance(d['a']['b'], MySubClass))


def test_dot_with_space_in_names():
    d = dotify({'key one': 1})
    assert_equals(1, d.key_one)
    assert_equals(1, d['key one'])


def test_dot_with_space_clash():
    assert_raises(ValueError, dotify, {
        'key one': 1,
        'key_one': 2
    })
