# -*- coding: utf-8 -*-
from flask import request, current_app
from flask_restful import abort
import time
import logging

logger = logging.getLogger('ietar_limit')
logger.setLevel(logging.DEBUG)
logger.propagate = False


def get_remote_address():
    """
    :return: the ip address for the current request
     (or 127.0.0.1 if none found)

    """
    return request.remote_addr or '127.0.0.1'


class Limiter1(object):
    # 内存式
    def __init__(self, app=None, debug=False):
        self.table = {}
        self.app = app
        self.debug = debug
        self.to_add = {}
        self.app.after_request(self.add_x_header)

    def add_x_header(self, response):
        # for k, v in self.to_add.items():
        #     response.headers.add(k, v)
        response.headers.update(self.to_add)
        return response

    def renew(self, check_interval):
        if self.debug:
            logger.debug(f'renew() {self.table}')
        for record in self.table.copy():
            all_ts: list = self.table[record]['ts']
            now_ts = time.time()
            for ts in all_ts:
                if now_ts - ts > check_interval:
                    all_ts.remove(ts)
                    self.table[record]['count'] -= 1

    def limit(self, amount: int, many_interval=1, interval='second'):
        """
        只接受1组限速 3次/3分 limit(amount=3, many_interval=3, interval='min')
        :param amount:
        :param many_interval:
        :param interval:
        :return:
        """
        interval_dict = {'second': 1, 'min': 60, 'hour': 3600, 'day': 86400}
        check_interval = many_interval * interval_dict.get(interval.lower(), 0)
        # seconds = amount * interval_dict.get(interval, 0)
        if not check_interval:
            raise ValueError(f'param "interval" not in {interval_dict.keys()} and amount cannot equals 0')

        def inner(func: callable):
            def in_inner(*a, **k):

                key = f'{func.__module__}.{func.__name__}/{amount}/{interval}'
                # print(f'key= {key}')  # __main__.abc/3/min
                v = self.table.get(key)
                if not v:
                    # if key not in self.table:
                    self.table[key] = {'ts': [], 'count': 0, 'max': amount}
                else:
                    self.renew(check_interval)
                v = self.table.get(key)

                if v['count'] == amount:
                    self.to_add.update({
                        'Retry-After': round(v['ts'][0] + check_interval - time.time(), 0)
                    })
                    if __name__ != '__main__':
                        abort(429)
                    return 429

                else:
                    self.table.get(key)['ts'].append(time.time())
                    count = self.table.get(key)['count'] + 1
                    self.table.get(key)['count'] = count

                if self.debug:
                    logging.debug(f'{self.table}')

                temp = {'X-Rate-Limit-Limit': amount,
                        # 'X-Rate-Limit-Reset"': 0,
                        'X-Rate-Limit-Remaining': amount - count
                        }
                self.to_add.update(temp)
                self.to_add.setdefault('X-Rate-Limit-Reset', 0)
                # self.app.after_request(self.add_x_header)

                return func(*a, **k)

            return in_inner

        return inner


if __name__ == '__main__':
    import sys

    DEBUG = True
    LEVEL = logging.DEBUG

    hdl = logging.StreamHandler(sys.stderr)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    hdl.setFormatter(formatter)
    hdl.setLevel(LEVEL)
    logger.addHandler(hdl)

    l1 = Limiter1(debug=DEBUG)


    @l1.limit(amount=10, many_interval=20, interval='second')
    def abc():
        global c
        c += 1
        if DEBUG:
            # logging.debug(f'调用成功{c}次')
            logger.debug(f'调用成功{c}次')
        return 1


    c = 0
    for i in range(80):
        res = abc()
        if res == 429:
            time.sleep(1)
        else:
            pass
