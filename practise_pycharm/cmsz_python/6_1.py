# -*- encoding: utf-8 -*-
def init(data):
    data['first'] = {}
    data['middle'] = {}
    data['last'] = {}


def lookup(data, label, name):
    """look for full names in dicitionary"""
    return data[label].get(name)


def store(data, full_name):
    """
    store people\'s full names
    hello world
    """
    names = full_name.split()
    if len(names) == 2:
        names.insert(1, '')
    labels = ['first', 'middle', 'last']
    for label, name in zip(labels, names):
        people = lookup(data, label, name)
        if people:
            data[label][name].append(full_name)
        else:
            data[label][name] = [full_name]


def store2(data, *full_names):
    """
    :param data: dictionary stored all full names
    :param full_names: people's full names
    :return:
    """
    for fullname in full_names:
        names = fullname.split()
        if len(names) == 2:
            names.insert(1, '')
        labels = ['first', 'middle', 'last']
        for label, name in zip(labels, names):
            people = lookup(data, label, name)
            if people:
                data[label][name].append(fullname)
            else:
                data[label][name] = [fullname]

MyNames = {}
init(MyNames)
store(MyNames, 'Wu Zhenyu Yu')
store(MyNames, 'Magus Lie Hetland')
store(MyNames, 'Mr. Gumby')
store2(MyNames, 'Zhang Fei', 'Tylor Swift')
print lookup(MyNames, 'middle', 'Zhenyu')
print lookup(MyNames, 'middle', '')
print store.__doc__
print store2.__doc__
