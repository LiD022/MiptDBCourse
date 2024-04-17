## Сохранить большой JSON (~20МБ) в виде разных структур - строка, hset, zset, list

Выбрал как основной датасет - https://www.kaggle.com/datasets/rmisra/news-category-dataset

- [Скрипт на python](https://github.com/LiD022/MiptDBCourse/blob/main/redis_py_files/load_strings.py) для сохранения в формате строки. Время работы:

  [!](https://github.com/LiD022/MiptDBCourse/blob/main/redis_py_files/load_string.png)

- [Скрипт на python](https://github.com/LiD022/MiptDBCourse/blob/main/redis_py_files/read_strings.py) для чтения в формате строки. Время работы:

  

- [Скрипт на python](https://github.com/LiD022/MiptDBCourse/blob/main/redis_py_files/load_structure.py) для сохранения сложных структуры (ключам были даны названия для простоты). Время работы:

  

- [Скрипт на python](https://github.com/LiD022/MiptDBCourse/blob/main/redis_py_files/read_structure.py) для чтения сложной структуры. Время работы:

  

Очевидно, что вставка/выборка данных в виде строк почти всегда быстрее, чем использование специальных структур.

## Настройка redis кластера на 3-х нодах
