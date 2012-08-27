from copy import deepcopy
import time

from supermutes.dot import dotify
from supermutes.readonly import readonly
from supermutes.benchmark import DATA


def time_call(func, *args, **kwargs):
    t1 = time.time()
    r = func(*args, **kwargs)
    t2 = time.time()
    print(t2 - t1)
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
    converted_data = time_call(func, data)
    #read high level
    time_call(lambda d: d['item_7'], converted_data)
    #read low level
    time_call(lambda d: d['item_1']['item_2']['item_3']['A'], converted_data)

    try:
        #write high level
        time_call(do_write_high, converted_data)
        #write low level
        time_call(do_write_low, converted_data)
        #delete high
        time_call(do_delete_high, converted_data)
        #delete low
        time_call(do_delete_low, converted_data)
    except:
        print "skipping write tests"
        pass


if __name__ == '__main__':
    data = deepcopy(DATA)
    time_call(do_benchmark, data, dict)
    print '----'
    time_call(do_benchmark, data, dotify)
    print "----"
    data = deepcopy(DATA)
    time_call(do_benchmark, data, readonly)
