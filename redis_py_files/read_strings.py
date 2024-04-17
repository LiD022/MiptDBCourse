import time
import redis

if __name__ == '__main__':
    r = redis.StrictRedis(host='localhost', port=6379, db=1)

    print('Load strings. \n')
    print('Match keys. \n')
    for key in r.keys('*'):
        print(key)

    print('Match data by keys. \n')
    ind = 0
    units = []
    start = time.time()
    for ind, key in enumerate(r.keys('*')):
        unit = r.get(key)
    end = time.time()

    print('Time left', end - start, 'sec')
    print('Units count:', ind + 1)
