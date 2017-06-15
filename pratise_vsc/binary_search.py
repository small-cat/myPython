# -*- encoding: utf-8 -*-
def binary_search(sequence, start, end, key):
    """
    :param sequence: a sorted sequence
    :param start: start index
    :param end: stop index
    :param key: key find in sequence or not
    :return: index of key in sequence, if not, return -1
    """
    if start > end:
        return -1
    mid = (end + start)//2
    if sequence[mid] == key:
        return mid
    elif sequence[mid] > key:  # on the left of mid
        return binary_search(sequence, start, mid - 1, key)
    elif sequence[mid] < key:  # on the right of mid
        return binary_search(sequence, mid + 1, end, key)


mlist = [1, 5, 2, 9, 10]
print mlist
mlist.sort()
print mlist

#number = int(raw_input("input a number to find: "))
number = 10
idx = binary_search(mlist, 0, 4, number)
if idx == -1:
    print "Can not find %d in sequence" % (number, )
else:
    print "mlsit[%d] = %d" % (idx, number)
