import hmac
import time
import random


lower_letters = 'abcdefghijklmnopqrstuvwxyz'
upper_letters = lower_letters.upper()
numbers = '0123456789'


def mk_salt():
    res = str(round(time.time(), 7)) + ''.join(random.choices(lower_letters, k=3))
    res += str(random.randint(100, 999)) + ''.join(random.choices(upper_letters, k=3))
    return res


def mk_pw(pw: str, salt: str):
    """
    make password
    :param pw: password
    :param salt:
    :return:
    """
    return hmac.new(key=salt.encode(), msg=pw.encode(), digestmod='sha256').hexdigest()


if __name__ == '__main__':
    s = mk_salt()
    print(s, type(s))
    p = mk_pw(pw='ietar', salt=s)
    print(p, type(p))
