from flask import request


def get_ip(func):
    def get_ip_info(*args, **kwargs):
        print(request.endpoint)
        print('接受一个request')
        return func(*args, **kwargs)

    return get_ip_info


def clock(func):
    import time

    def clocked(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        print('花费的时间为:{}'.format(end_time - start_time))
        return result

    return clocked
