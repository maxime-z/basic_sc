def abs(n):
    '''
    Function to get absolute value of n.

    Example:
    >>> abs(-1)
    1
    >>> abs(1)
    1
    >>> abs(0)
    0
    :param n:
    :return:
    '''
    return n if n > 0 else (-n)


if __name__ == '__main__':
    import doctest
    doctest.testmod()