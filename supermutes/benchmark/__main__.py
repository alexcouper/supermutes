from copy import deepcopy
import time

from supermutes.dot import dotify
from supermutes.readonly import readonly
from supermutes.benchmark import DATA


def time_call(text, func, *args, **kwargs):
    t1 = time.time()
    try:
        r = func(*args, **kwargs)
    except:
        r = None
    t2 = time.time()
    print("{0}: {1}".format(text, t2 - t1))
    return r


def do_write_high(data):
    data['new_item'] = [1, 2, 3]


def do_write_low(data):
    data['item_1']['item_2']['item_4'].append({'item101': 9})


def do_delete_low(data):
    del data['item_1']['item_2']['item_4'][-1]['item101']


def do_delete_high(data):
    del data['new_item']


def do_benchmark(data, func):
    #convert
    converted_data = time_call("convert", func, data)
    #read high level
    time_call('Get item H',
              lambda d: d['item_7'],
              converted_data)
    #read low level
    time_call('Get item L',
              lambda d: d['item_1']['item_2']['item_3']['A'],
              converted_data)

    #write high level
    time_call('Write H', do_write_high, converted_data)
    #write low level
    time_call('Write L', do_write_low, converted_data)
    #delete high
    time_call("Delete H", do_delete_high, converted_data)
    #delete low
    time_call("Delete L", do_delete_low, converted_data)


if __name__ == '__main__':
    data = deepcopy(DATA)
    time_call("dict total", do_benchmark, data, dict)
    print('----')
    time_call("dotify total", do_benchmark, data, dotify)
    print("----")
    data = deepcopy(DATA)
    time_call("readonly total", do_benchmark, data, readonly)
