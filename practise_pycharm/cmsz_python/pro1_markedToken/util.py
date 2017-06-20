# -*- encoding:utf-8 -*-


def lines(mfile):
    """
    iterator
    """
    for line in mfile:
        yield line
    yield '\n'


def blocks(mfile):
    """
    yiled return a generator, not a list
    but we want a list
    """
    block = []
    for line in lines(mfile):
        if line.strip():
            block.append(line)
    if block:
        return block


def strip_enter(block):
    """
    去掉末尾的 \r \n
    """
    if block[-2:] == '\r\n':
        print_block = block[:-2]
    elif block[-2] != '\r' and block[-1] == '\n':
        print_block = block[:-1]
    else:
        print_block = block[0:]

    return print_block


# testing
if __name__ == '__main__':
    with open('file1.md', 'r') as f:
        lst = blocks(f)
        print "lst:", lst
        for block in lst:
            print block

