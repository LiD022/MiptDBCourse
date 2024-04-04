# HW2

## Установка и настройка MongoDB
Для настройки MongoDB я решил воспользоваться Docker. 
```
sudo docker pull mongo
```
При запуске я подключил специальную директорию ./mongoimport, чтобы напрямую загружать данные в контейнер Docker.
```
sudo docker run -it -v mongodata:/data/db --name mongodb -d mongo
```
## Выбор датасета
Взял всем известный датасет titanic.csv и использовав команду импортировал данные из него
```
root@3ay5e1488a6fz:/# mongoimport -d Titanic -c titanic --type csv --file /data/db/titanic.csv --headerline
2024-04-04T20:27:06.995+0000 connected to: mongodb://localhost/
2024-04-04T20:27:07.020+0000 887 document(s) imported successfully. 0 document(s) failed to import.
```
## Написать несколько запросов на выборку и обновление данных
- Вывести первую запись из датасета
```
Titanic> db.titanic.findOne()
{
  _id: ObjectId('660f0d1b521430a37c125b39'),
  Survived: 0,
  Pclass: 3,
  Name: 'Mr. Owen Harris Braund',
  Sex: 'male',
  Age: 22,
  'Siblings/Spouses Aboard': 1,
  'Parents/Children Aboard': 0,
  Fare: 7.25
}
```
- Зная как выглядят данные, можем добавить новую строку
```
Titanic> db.titanic.updateOne({ _id: ObjectId('660f0d1b521430a37c125b39') }, { $set: { Sex: 'hexadetrine' } } )
{
  acknowledged: true,
  insertedId: null,
  matchedCount: 1,
  modifiedCount: 1,
  upsertedCount: 0
}
Titanic> db.titanic.findOne()
{
  _id: ObjectId('660f0d1b521430a37c125b39'),
  Survived: 0,
  Pclass: 3,
  Name: 'Mr. Owen Harris Braund',
  Sex: 'hexadetrine',
  Age: 22,
  'Siblings/Spouses Aboard': 1,
  'Parents/Children Aboard': 0,
  Fare: 7.25
}
```
## Создать индексы и сравнить производительность
Проверим как он выводит без индекса
```
Titanic> db.titanic.find({Sex:'male'}).explain('executionStats')
{
  explainVersion: '1',
  queryPlanner: {
    namespace: 'Titanic.titanic',
    indexFilterSet: false,
    parsedQuery: { Sex: { '$eq': 'male' } },
    queryHash: '861DC9A7',
    planCacheKey: '861DC9A7',
    maxIndexedOrSolutionsReached: false,
    maxIndexedAndSolutionsReached: false,
    maxScansToExplodeReached: false,
    winningPlan: {
      stage: 'COLLSCAN',
      filter: { Sex: { '$eq': 'male' } },
      direction: 'forward'
    },
    rejectedPlans: []
  },
  executionStats: {
    executionSuccess: true,
    nReturned: 572,
    executionTimeMillis: 0,
    totalKeysExamined: 0,
    totalDocsExamined: 887,
    executionStages: {
      stage: 'COLLSCAN',
      filter: { Sex: { '$eq': 'male' } },
      nReturned: 572,
      executionTimeMillisEstimate: 0,
      works: 888,
      advanced: 572,
      needTime: 315,
      needYield: 0,
      saveState: 0,
      restoreState: 0,
      isEOF: 1,
      direction: 'forward',
      docsExamined: 887
    }
  },
  command: { find: 'titanic', filter: { Sex: 'male' }, '$db': 'Titanic' },
  serverInfo: {
    host: '9bd9e288a8fc',
    port: 27017,
    version: '7.0.8',
    gitVersion: 'c5d33e55ba38d98e2f48765ec4e55338d67a4a64'
  },
  serverParameters: {
    internalQueryFacetBufferSizeBytes: 104857600,
    internalQueryFacetMaxOutputDocSizeBytes: 104857600,
    internalLookupStageIntermediateDocumentMaxSizeBytes: 104857600,
    internalDocumentSourceGroupMaxMemoryBytes: 104857600,
    internalQueryMaxBlockingSortMemoryUsageBytes: 104857600,
    internalQueryProhibitBlockingMergeOnMongoS: 0,
    internalQueryMaxAddToSetBytes: 104857600,
    internalDocumentSourceSetWindowFieldsMaxMemoryBytes: 104857600,
    internalQueryFrameworkControl: 'trySbeRestricted'
  },
  ok: 1
}
```
Теперь добавим индекс 
```
Titanic> db.titanic.createIndex({Sex:'male'})
Sex_male
```
И еще раз посмотрим скорость
```
Titanic> db.titanic.find({Sex:'male'}).explain('executionStats')
{
  explainVersion: '1',
  queryPlanner: {
    namespace: 'Titanic.titanic',
    indexFilterSet: false,
    parsedQuery: { Sex: { '$eq': 'male' } },
    queryHash: '861DC9A7',
    planCacheKey: '861DC9A7',
    maxIndexedOrSolutionsReached: false,
    maxIndexedAndSolutionsReached: false,
    maxScansToExplodeReached: false,
    winningPlan: {
      stage: 'COLLSCAN',
      filter: { Sex: { '$eq': 'male' } },
      direction: 'forward'
    },
    rejectedPlans: []
  },
  executionStats: {
    executionSuccess: true,
    nReturned: 572,
    executionTimeMillis: 0,
    totalKeysExamined: 0,
    totalDocsExamined: 572,
    executionStages: {
      stage: 'COLLSCAN',
      filter: { Sex: { '$eq': 'male' } },
      nReturned: 572,
      executionTimeMillisEstimate: 0,
      works: 888,
      advanced: 572,
      needTime: 315,
      needYield: 0,
      saveState: 0,
      restoreState: 0,
      isEOF: 1,
      direction: 'forward',
      docsExamined: 887
    }
  },
  command: { find: 'titanic', filter: { Sex: 'male' }, '$db': 'Titanic' },
  serverInfo: {
    host: '9bd9e288a8fc',
    port: 27017,
    version: '7.0.8',
    gitVersion: 'c5d33e55ba38d98e2f48765ec4e55338d67a4a64'
  },
  serverParameters: {
    internalQueryFacetBufferSizeBytes: 104857600,
    internalQueryFacetMaxOutputDocSizeBytes: 104857600,
    internalLookupStageIntermediateDocumentMaxSizeBytes: 104857600,
    internalDocumentSourceGroupMaxMemoryBytes: 104857600,
    internalQueryMaxBlockingSortMemoryUsageBytes: 104857600,
    internalQueryProhibitBlockingMergeOnMongoS: 0,
    internalQueryMaxAddToSetBytes: 104857600,
    internalDocumentSourceSetWindowFieldsMaxMemoryBytes: 104857600,
    internalQueryFrameworkControl: 'trySbeRestricted'
  },
  ok: 1
}
```
Было 'totalDocsExamined: 887', стало 'totalDocsExamined: 572'.
