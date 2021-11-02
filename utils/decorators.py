def deco1(func):
    def inner(*args, **kwargs):
        print('deco1')
        return func(*args, **kwargs)
    return inner


def deco2(func):
    def inner(*args, **kwargs):
        print('deco2')
        return func(*args, **kwargs)
    return inner
