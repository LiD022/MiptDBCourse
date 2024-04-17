import json
import time
import redis

if __name__ == '__main__':

    DEBUG_UPLOAD_LIMIT = 2000
    r = redis.StrictRedis(host='localhost', port=6379, db=2)
    print('Upload json as complex structure.')

    # JSON-ключи, которые будут списками, остальные будут hset

    keys_for_list = 'link', \
                    'category'
    # тут разделитель -
    keys_for_list_2 = 'short_description', \
                      'authors'

    with open('data.json', encoding='cp1251') as input_file:
        test_data = json.load(input_file)
        count = len(test_data)
        index = 0

        start = time.time()

        for index, data in enumerate(test_data):
            if DEBUG_UPLOAD_LIMIT and index >= DEBUG_UPLOAD_LIMIT:
                break

            for key, value in data.items():
                if key in keys_for_list:
                    continue
                if key in keys_for_list_2:
                    continue

                r.hset('object:%s:hset' % data.get("system_object_id"), key.lower(), '%s' % value)

            for key in keys_for_list:

                if not data.get(key):
                    print('PASSED', data.get(key))
                    continue
                for item in data.get(key).split(';'):

                    r.lpush('object:%s:list__%s' % (data.get("system_object_id"), key.lower()), item.strip())
            for key in keys_for_list_2:

                if not data.get(key):
                    print('PASSED', data.get(key))
                    continue
                for item in data.get(key).split(' - '):

                    r.lpush('object:%s:list__%s' % (data.get("system_object_id"), key.lower()), item.strip())

            # для zset путь будет упорядоченное по алфавиту по первым бувам (НЕ лексикографическое) название заголовков

            zset_keys = ('headline',)
            for key in zset_keys:
                if not data.get(key):
                    print('PASSED', data.get(key))
                    continue
                for item in data.get(key).split(' - '):

                    value = item.upper().strip()
                    r.zadd('object:%s:zset__%s' % (data.get("system_object_id"), key.lower()), {value: ord(value[0])})
            #
            r.save()

        end = time.time()
        print('\t', 'Were upload:', index, 'units')
        print('\t', 'Time left:', end - start, 'sec')
