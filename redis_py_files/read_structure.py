import redis
import time


if __name__ == '__main__':

    r = redis.StrictRedis(host='localhost', port=6379, db=2)

    print('Load keys. \n')

    for key in r.keys('*:104:*'):
        print(key)

    print('\t', 'sets keys:')
    for key in r.keys('*:104:*set'):
        print('\t', '\t', key)

    print('\t', 'hsets:')
    for key in r.keys('*:104:list__*'):
        print('\t', '\t', key)

    print('\t', 'hset keys:')
    for key in r.keys('*:104:hset'):
        unit = r.hscan(key, match='*')
        for h_key in unit[1]:
            print('\t', '\t', h_key)

    print('\n\t', 'hset keys values:')
    k_v = enumerate(r.keys('*:hset'))
    v_indx = 0
    start = time.time()
    for v_indx, v in k_v:
        units = r.hscan(v, match='*')
    end = time.time()
    

    print('\nTime left for get all keys for ALL hset-substructures', end - start, 'sec')
    print('Units count:', v_indx+1)

    # LIST

    print('\n\t', 'list keys values:')
    k_v = enumerate(r.keys('*:list__*'))
    v_indx = 0
    start = time.time()
    for v_indx, v in k_v:
        units = r.lrange(v, 0, -1)
    end = time.time()
    
    print('\nTime left for get values from lists:', end - start, 'sec')
    print('Units count:', v_indx + 1)

    # ZSET

    print('\n\t', 'zset keys values:')
    k_v = enumerate(r.keys('*:zset__*'))
    v_indx = 0
    start = time.time()
    for v_indx, v in k_v:
        units = r.zrange(v, 0, -1)
    end = time.time()
  
    print('\nTime left for get values from zset:', end - start, 'sec')
    print('Units count:', v_indx + 1)
