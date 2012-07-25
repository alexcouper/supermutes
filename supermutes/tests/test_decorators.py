from nose.tools import assert_true

from supermutes.readonly import ReadOnlyDict
from supermutes.decorators import return_readonly


@return_readonly
def my_test_func():
    return {'a': 2}


def test_response_readonly():
    foo = my_test_func()
    assert_true(isinstance(foo, ReadOnlyDict))
