## Сохранить большой JSON (~20МБ) в виде разных структур - строка, hset, zset, list

Выбрал как основной датасет - https://www.kaggle.com/datasets/rmisra/news-category-dataset

- [Скрипт на python](https://github.com/LiD022/MiptDBCourse/blob/main/redis_py_files/load_strings.py) для сохранения в формате строки. Время работы:

  ![image](https://github.com/LiD022/MiptDBCourse/blob/main/redis_py_files/load_strings.png)

- [Скрипт на python](https://github.com/LiD022/MiptDBCourse/blob/main/redis_py_files/read_strings.py) для чтения в формате строки. Время работы:

  ![image](https://github.com/LiD022/MiptDBCourse/blob/main/redis_py_files/read_string.png)

- [Скрипт на python](https://github.com/LiD022/MiptDBCourse/blob/main/redis_py_files/load_structure.py) для сохранения сложных структуры (ключам были даны названия для простоты). Время работы:

  ![image](https://github.com/LiD022/MiptDBCourse/blob/main/redis_py_files/load_structure.png)

- [Скрипт на python](https://github.com/LiD022/MiptDBCourse/blob/main/redis_py_files/read_structure.py) для чтения сложной структуры. Время работы:

  ![image](https://github.com/LiD022/MiptDBCourse/blob/main/redis_py_files/read_sructure.png)

Очевидно, что вставка/выборка данных в виде строк почти всегда быстрее, чем использование специальных структур.

## Настройка redis кластера на 3-х нодах
- Создаем кластер с помощью minikube и kubernetes:

```
minikube start --cpus=6 --memory=6000 --nodes=4  --kubernetes-version v1.28.8 
```
- С помощью конфигурации получаем отказоустойчивый кластер:
```
kubectl get po -n redis                                            

NAME           READY   STATUS    RESTARTS   AGE
redis-node-0   3/3     Running   0          54s
redis-node-1   3/3     Running   0          32s
redis-node-2   3/3     Running   0          16s
```
- Тюнинг таймаутов в спецификации RedisCluster в конфигурационном файле:
```
kubectl create configmap redis-config --namespace=default --from-literal=timeout=500
```
