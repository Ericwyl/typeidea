'''
import time

CACHE = {}


#被动缓存
def query(sql):
    try:
        result = CACHE[sql]
    except KeyError:
        time.sleep(1)
        result = 'execute %s' % sql
        CACHE[sql] = result
    return result


#主动缓存
def query(sql):
    result = CACHE.get(sql)
    if not result:
        time.sleep(1)
        result = 'execute %s' % sql
        CACHE[sql] = result
    return result


if __name__ == '__main__':
    start = time.time()
    query('SELECT * FROM blog_post')
    print(time.time() - start)

    start = time.time()
    query('SELECT * FROM blog_post')
    print(time.time()-start)
'''

#缓存装饰器
import functools
import time

CACHE = {}


def cache_it(func):
    @functools.wraps(func)
    def inner(*args, **kwargs):
        key = repr(*args, **kwargs)
        try:
            result = CACHE[key]
        except KeyError:
            result = func(*args, **kwargs)
            CACHE[key] = result
        return result
    return inner

#对于要缓存的函数，加上@cache_it就可以了

@cache_it
def query(sql):
    time.sleep(1)
    result = 'execute %s' % sql
    return result


if __name__ == '__main__':
    start = time.time()
    query('SELECT * FROM blog_post')
    print(time.time()-start)

    start = time.time()
    query('SELECT * FROM blog_post')
    print(time.time()-start)

