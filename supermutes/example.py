from supermutes.register import get_new_obj
from supermutes.base import SuperMutable


class OnlyStringOrDict(SuperMutable, dict):

    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)
        for key, value in self.items():
            self[key] = value

    def mutate(self, value):
        return get_new_obj(value)  # get_new_obj uses the module that called
                                   # it to determine which kind of SuperMutable
                                   # is appropriate. This makes subclassing
                                   # of your SuperMutable easy!

    def __setitem__(self, key, value):
        if isinstance(value, basestring) or isinstance(value, dict):
            return super(OnlyStringOrDict, self).__setitem__(key, value)
        raise Exception("OnlyStringOrDict only likes strings or "
                        "dicts: {0}".format(value))

"""
In Use:

from supermutes.example import OnlyStringDict

>>  string_dict = OnlyStringOrDict({'one': 'f', 'two': {'what': '4'}})
>>  string_dict[4] = "This will go in fine"
>>  string_dict
{4: 'This will go in fine', 'two': {'what': '4'}, 'one': 'f'}
>>  string_dict[5] = {'another': "legitimate"}
>>  string_dict
{5: {'another': 'legitimate'}, 4: 'This will go in fine', 'two': {'what': '4'},
 'one': 'f'}
>>  string_dict[5]['fail'] = 10
Exception: OnlyStringOrDict only likes strings or dicts: 10
"""
