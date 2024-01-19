#!/usr/bin/python3
'''Minimum operations problem.
'''


def minOperations(n):
    '''Least amount of operations to get result
    '''
    if not isinstance(n, int):
        return 0
    ops_count = 0
    clipboard = 0
    done = 1
    # print
    while done < n:
        if clipboard == 0:
            # init
            clipboard = done
            done += clipboard
            ops_count += 2
            # print
        elif n - done > 0 and (n - done) % done == 0:
            clipboard = done
            done += clipboard
            ops_count += 2
            # print
        elif clipboard > 0:
            # paste
            done += clipboard
            ops_count += 1
            # print
    # print
    return ops_count
