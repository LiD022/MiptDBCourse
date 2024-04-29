# Знакомство с **Apache Jackrabbit** СУБД

Apache Jackrabbit является реализацией Content Repository for Java Technology API (JCR), которая предоставляет доступ к контенту в виде иерархической структуры узлов и свойств. Для начала разберемся что такое Контентные СУБД.

Модель Content Database - это базы данных, специально оптимизированные для хранения и управления большими объемами неструктурированных данных, таких как текстовые документы, изображения, аудио- и видеофайлы, веб-страницы и другие цифровые активы. 
Контентные СУБД отличаются от традиционных реляционных СУБД тем, что они предоставляют более гибкие схемы данных, поддерживают полнотекстовый поиск, версионирование, управление правами доступа и другие специфические для контента функции. Они также могут масштабироваться горизонтально, что позволяет им эффективно обрабатывать растущие объемы данных.

Разберем подрообнее особенности Apache Jackrabbit и начнем с истории развития данной СУБД.

## История развития СУБД
Проект Jackrabbit был начат 28 августа 2004 года, когда компания *Day Software* начала разработку реализации API хранилища содержимого для Java (JCR). Jackrabbit также был использован как пример реализации JSR-170 и JSR-283 (спецификации Java, которые определяют стандартный API для доступа к репозиториям контента в Java-приложениях). Проект вышел из «инкубатора» Apache 15 марта 2006 года и сейчас является проектом верхнего уровня в Apache Software Foundation. С тех пор Apache Jackrabbit активно развивается и обновляется.

## Инструменты для взаимодействия с СУБД
Для взаимодействия с Apache Jackrabbit можно использовать различные инструменты, такие как:

- *JCR API*: Основной инструмент для взаимодействия с Apache Jackrabbit. Это стандартный Java API, который предоставляет методы для создания, чтения, обновления и удаления контента в репозитории.
- *WebDAV*: Apache Jackrabbit поддерживает протокол WebDAV (Web-based Distributed Authoring and Versioning), что позволяет использовать любой WebDAV-клиент для взаимодействия с репозиторием.
- *RESTful API*: Apache Jackrabbit Oak предоставляет RESTful API, который позволяет получать доступ к контенту репозитория через HTTP-запросы.
- *JCR Shell*: Это командная строка, предоставляемая Apache Jackrabbit. Она позволяет выполнять операции JCR с помощью простых команд.
- *Apache Sling*: Это фреймворк, основанный на Apache Jackrabbit, который предоставляет RESTful интерфейс для доступа к контенту репозитория.
- *Apache Felix JCR Shell*: Это OSGi-совместимая оболочка, которая предоставляет командный интерфейс для взаимодействия с JCR репозиториями.
- *JCR Explorer*: Это веб-приложение, которое предоставляет графический интерфейс для просмотра и управления содержимым JCR репозитория.
- *ModeShape*: Это репозиторий данных, основанный на JCR, который может использоваться для взаимодействия с Apache Jackrabbit.

## Database Engine 
Apache Jackrabbit использует несколько типов баз данных для хранения контента и метаданных. Он поддерживает различные database engines через абстракцию, называемую "Persistence Manager". Некоторые из поддерживаемых баз данных включают:

- *Derby* (встроенная по умолчанию): Apache Jackrabbit поставляется с встроенной базой данных Apache Derby, которая используется по умолчанию.
- *MySQL*: Jackrabbit также поддерживает использование MySQL в качестве внешней базы данных.
- *PostgreSQL*: Поддержка PostgreSQL также доступна для использования с Jackrabbit.
- *Oracle*: Oracle Database может быть использована с Jackrabbit с помощью соответствующего драйвера JDBC.
- *Microsoft SQL Server*: Microsoft SQL Server также может быть использован с Jackrabbit.
- *MongoDB*: Jackrabbit предоставляет поддержку MongoDB через Oak MongoDB Connector.
- *TarMK*: Tar Persistence Manager (TarPM) - это реализация Persistence Manager, которая хранит данные в файлах tar. Этот вариант обеспечивает более высокую производительность и масштабируемость, чем Derby.

## Как устроен язык запросов
Язык запросов в Apache Jackrabbit основан на SQL и называется JCR-SQL2. Он позволяет выполнять запросы к репозиторию на основе SQL-подобного синтаксиса. JCR-SQL2 поддерживает фильтрацию, сортировку, объединение и другие операции с данными. Рассмотрим несколько команд на языке Java:

*Подключение к репозиторию*
```
Repository repository = JcrUtils.getRepository();
Session session = repository.login(new SimpleCredentials("admin", "admin".toCharArray()));

```

*Создание узла*
```
Node rootNode = session.getRootNode();
Node myNode = rootNode.addNode("myNode", "nt:unstructured");
myNode.setProperty("title", "My Node");
session.save();

```

*Выполнение запроса на получение всех узлов, которые имеют свойство "title"*
```
String query = "SELECT * FROM [nt:base] WHERE ISDESCENDANTNODE([/]) AND [jcr:title] IS NOT NULL";
QueryManager queryManager = session.getWorkspace().getQueryManager();
Query queryObject = queryManager.createQuery(query, Query.SQL2);
QueryResult result = queryObject.execute();
NodeIterator nodes = result.getNodes();
while (nodes.hasNext()) {
    Node node = nodes.nextNode();
    System.out.println(node.getName() + ": " + node.getProperty("title").getString());
}
```

*Вывод консоли:*
```
myNode: My Node
```

## Распределение файлов БД по разным носителям
По умолчанию, Jackrabbit хранит все данные в одном репозитории на одном носителе. Однако существует несколько способов настроить Jackrabbit для распределения файлов базы данных по разным носителям. Один из популярных реализаций является использование *DataStore* - это компонент Jackrabbit, который используется для хранения бинарных данных.

Для настройки этих опций, нужно изменить файл конфигурации Jackrabbit repository.xml:

```
<DataStore class="org.apache.jackrabbit.core.data.FileDataStore">
  <param name="path" value="$~/istomin_db_hw/hw4/repository/datastore"/>
  <param name="minRecordLength" value="100"/>
</DataStore>

```

## Язык программирования Apache Jackrabbit
Apache Jackrabbit написан преимущественно на языке программирования Java. Это реализация спецификации Content Repository for Java Technology API (JCR), которая предоставляет доступ к контенту в независимом от хранилища формате. Java был выбран из-за его широкого использования в предприятийных приложениях и его способности обеспечивать переносимость между платформами.

## Типы индексов
Apache Jackrabbit поддерживает несколько типов индексов для улучшения производительности запросов. Вот некоторые из них:

- *Property Index*: Индекс свойств используется для индексирования значений свойств узлов. Он улучшает производительность при выполнении запросов, которые фильтруют результаты по значениям свойств.

- *Node Type Index*: Индекс типа узла используется для индексирования узлов на основе их основного типа узла. Это улучшает производительность при выполнении запросов, которые фильтруют результаты по основному типу узла.

- *Path Index*: Индекс пути используется для индексирования узлов на основе их абсолютного пути. Это улучшает производительность при выполнении запросов, которые фильтруют результаты по абсолютному пути узла.

```
// Создание индекса свойств
Node indexNode = rootNode.addNode("myPropertyIndex", "nt:unstructured");
indexNode.setProperty("jcr:primaryType", "rep:PropertyIndex");
indexNode.setProperty("jcr:indexedTypes", "nt:base");
indexNode.setProperty("rep:propertyName", "myProperty");
session.save();

// Создание тестовых узлов
Node testNode1 = rootNode.addNode("testNode1", "nt:unstructured");
testNode1.setProperty("myProperty", "value1");
Node testNode2 = rootNode.addNode("testNode2", "nt:unstructured");
testNode2.setProperty("myProperty", "value2");
session.save();

// Выполнение запроса с использованием индекса
QueryManager queryManager = session.getWorkspace().getQueryManager();
Query query = queryManager.createQuery("SELECT * FROM nt:base WHERE myProperty = 'value1'", Query.SQL);
QueryResult result = query.execute();
NodeIterator nodes = result.getNodes();
while (nodes.hasNext()) {
    Node node = nodes.nextNode();
    System.out.println("Found node: " + node.getPath());
}
```
*Вывод консоли:*
```
Found node: /testNode1
```

## Процесс выполнения запросов
1. Создание сеанса. Сеанс предоставляет доступ к содержимому репозитория и управляет жизненным циклом изменений.

2. Получение рабочей области. Рабочая область представляет собой область видимости, в которой можно выполнять операции чтения и записи.

3. Создание QueryManager: QueryManager используется для создания и выполнения запросов.

4. Создание запроса, используя QueryManager. Apache Jackrabbit поддерживает два языка запросов: SQL2 и XPath

5. Выполнение запроса, используя метод execute. Этот метод возвращает результат в виде объекта QueryResult.

6. Обработка результатов, используя объект QueryResult. Этот объект позволяет вам пройти через результаты и получить доступ к отдельным узлам.

7. Завершение сеанса. Это важно, так как сеанс использует ресурсы репозитория.

## План запросов
В Apache Jackrabbit нет прямого понятия "план запросов", как это реализовано в некоторых реляционных базах данных. Тем не менее, Jackrabbit предоставляет механизмы оптимизации выполнения запросов, которые можно настроить и использовать для улучшения производительности.

Один из таких механизмов - это Query Planner (Планировщик запросов). Query Planner отвечает за преобразование запросов, написанных на языке запросов (например, SQL2 или XPath), в последовательность операций, которые выполняются репозиторием Jackrabbit. Существует несколько стратегий планирования запросов, которые можно настроить в зависимости от конкретных требований и структуры данных. Например, можно выбрать стратегию планирования запросов "TraversalQueryPlanner" или "SQLQueryPlanner" в зависимости от того, какой тип запросов планируется использовать. Эти стратегии можно настроить в файле конфигурации репозитория (repository.xml).

## Транзакции
Apache Jackrabbit поддерживает транзакции. В Jackrabbit транзакции используются для выполнения набора операций чтения и записи, которые должны быть выполнены атомарно. Это означает, что либо все операции в транзакции выполняются успешно, либо ни одна из них не выполняется.

Jackrabbit использует модель транзакций JCR (Java Content Repository), которая предоставляет два типа транзакций:

- *Транзакции с одним сеансом*: эти транзакции выполняются в контексте одного сеанса и изолированы от других сеансов. Они поддерживают все уровни изоляции, определенные в спецификации JCR.

- *Транзакции с несколькими сеансами*: эти транзакции выполняются в контексте нескольких сеансов и могут использоваться для выполнения операций, которые требуют взаимодействия между несколькими сеансами. Они поддерживают только уровень изоляции "сериализуемый", являющийся самым строгим уровнем изоляции транзакций в модели транзакций ACID (Atomicity, Consistency, Isolation, Durability). Этот уровень изоляции гарантирует, что каждая транзакция выполняется последовательно, как если бы она была единственной транзакцией, выполняющейся в системе, предотвращая все виды конфликтов между транзакциями, включая грязное чтение, неповторяющееся чтение и фантомное чтение.

## Методы восстановления
-*Backup and Restore*: Этот метод предоставляет возможность создавать резервные копии репозитория и восстанавливать их при необходимости. Можно использовать инструмент backup для создания резервной копии и restore для восстановления. Эти инструменты доступны в пакете org.apache.jackrabbit.core.tools.

-*Persistence Manager*: Persistence Manager (PM) используется для управления хранением данных в репозитории. Jackrabbit предоставляет несколько реализаций PM, таких как TarPM, FileSystemPM и другие. Можно выбрать подходящую реализацию PM в зависимости от ваших требований и настроить ее для восстановления данных из резервной копии.

-*Journal Recovery*: Jackrabbit использует журнал для отслеживания изменений в репозитории. При сбое системы журнал может быть использован для восстановления репозитория до консистентного состояния. Можно настроить Jackrabbit для автоматического восстановления из журнала при запуске или выполнить восстановление вручную с помощью инструмента Recover.

-*Cluster Configuration*: Если использовать Jackrabbit в кластерной конфигурации, то данные будут автоматически реплицироваться между узлами кластера. В случае сбоя одного из узлов, данные могут быть восстановлены из других узлов кластера.

-*Versioning*: Jackrabbit поддерживает версионирование узлов и свойств. Это означает, что Можно сохранять предыдущие версии контента и восстанавливать их при необходимости. Можно использовать API версионирования JCR для управления версиями и восстановления данных.

## Шардинг
Шардинг (sharding) в Apache Jackrabbit используется для горизонтального масштабирования и улучшения производительности путем разделения данных на более мелкие, управляемые части, называемые шардами. Есть два основных типа шардинга:

- *Content sharding*: Этот тип шардинга разделяет узлы репозитория на несколько шардов на основе их идентификаторов узлов. Каждый шард содержит определенный диапазон идентификаторов узлов. Это помогает сбалансировать нагрузку между шардами и улучшить производительность.
- *Binary sharding*: Этот тип шардинга разделяет двоичные данные, хранящиеся в репозитории, на несколько шардов. Двоичные данные могут включать в себя изображения, видео, документы и другие файлы. Разделение двоичных данных на шарды помогает уменьшить размер репозитория и улучшить производительность при работе с двоичными данными.

**Принцип работы шардинга в Apache Jackrabbit:**
1. Выбор типа шардинга: В зависимости от требований и характеристик данных выбирается подходящий тип шардинга (content sharding или binary sharding).
2. Конфигурация шардов: Количество шардов и их размеры определяются в конфигурационном файле Apache Jackrabbit. Это позволяет настроить шардинг в соответствии с конкретными требованиями и ограничениями производительности.
3. Распределение данных: При добавлении новых данных в репозиторий Apache Jackrabbit автоматически определяет, в какой шард должны быть помещены эти данные, на основе конфигурации шардинга.
4. Доступ к данным: При обращении к данным Apache Jackrabbit определяет, в каком шарде они находятся, и извлекает их оттуда. Это происходит прозрачно для клиентов, которые взаимодействуют с репозиторием.
5. Масштабирование: При необходимости Apache Jackrabbit позволяет увеличивать или уменьшать количество шардов, а также перераспределять данные между шардами для обеспечения лучшей производительности и балансировки нагрузки.

## Data Mining, Data Warehousing и OLAP
Apache Jackrabbit не является системой аналитики данных и не предоставляет встроенных средств для Data Mining, Data Warehousing и OLAP. Однако можно использовать Apache Jackrabbit в сочетании с другими инструментами для решения этих задач.

- Можно извлекать данные из Apache Jackrabbit с помощью JCR API и использовать сторонние библиотеки для Data Mining, такие как Weka или Apache Mahout, для анализа этих данных.

- Можно использовать Apache Jackrabbit в качестве одного из источников данных для хранилища данных (Data Warehouse). Затем можно использовать инструменты анализа данных, такие как Apache Hive или Apache Pig, для обработки и анализа этих данных.

- OLAP (Online Analytical Processing): Можно использовать Apache Jackrabbit в сочетании с инструментами OLAP, такими как Apache Kylin или Mondrian, для анализа многомерных данных.

## Методы защиты
Apache Jackrabbit поддерживает несколько методов защиты для обеспечения безопасности контента и доступа к нему. Вот некоторые из них:

- Шифрование трафика с использованием протокола HTTPS. Это обеспечивает защищенную передачу данных между клиентом и сервером.

- Аутентификация, включая базовую, аутентификацию на основе форм и аутентификацию по заголовкам.

- Авторизация, основанная на ролях. Можно назначать роли пользователям и группам, а затем назначать этим ролям права доступа к ресурсам.

- Контроль доступа, основанный на политиках доступа (Access Control Policies). Это позволяет администраторам определять, кто и как может взаимодействовать с ресурсами.

- Безопасность на уровне узла, что означает, что вы можете устанавливать права доступа для отдельных узлов в репозитории.

- Защита от несанкционированного доступа, включая фильтры и механизмы блокировки.

## Сообщества, развивающие Apache Jackrabbit
Apache Jackrabbit является открытым исходным кодом проекта, который разрабатывается и поддерживается сообществом Apache. Сообщество Apache Jackrabbit состоит из разработчиков, пользователей и энтузиастов со всего мира, которые вносят свой вклад в разработку и улучшение программного обеспечения.

В проекте Apache Jackrabbit есть несколько ролей, которые могут иметь право на коммит и создание дистрибутива версий:

- Коммиттеры - это разработчики, которые имеют право непосредственно вносить изменения в исходный код проекта. Они также могут создавать дистрибутивы версий и участвовать в принятии решений о развитии проекта. Коммиттеры избираются другими коммиттерами на основе их вклада в проект.

- ПМС (Project Management Committee) - это группа людей, которая отвечает за управление проектом в целом. Они имеют право на коммит и создание дистрибутива версий, а также принимают решения о развитии проекта и направлении его движения. ПМС избирается другими членами ПМС.

- Сотрудники Apache - это люди, которые работают непосредственно в фонде Apache и поддерживают инфраструктуру, необходимую для работы проектов Apache. Они также могут иметь право на коммит и создание дистрибутива версий в некоторых проектах. Некоторые из компаний, которые активно участвуют в развитии Apache Jackrabbit, включают Adobe, BloomReach, Hippo, Red Hat и другие. Э

## Создание собственных данных
```
import javax.jcr.Node;
import javax.jcr.PropertyType;
import javax.jcr.Repository;
import javax.jcr.RepositoryException;
import javax.jcr.Session;
import javax.jcr.SimpleCredentials;
import org.apache.jackrabbit.commons.JcrUtils;

public class JackrabbitTest {

  public static void main(String[] args) throws RepositoryException {
    // создаем репозиторий
    Repository repository = JcrUtils.getRepository();
    Session session = repository.login(new SimpleCredentials("admin", "admin".toCharArray()));

    // создаем узел
    Node rootNode = session.getRootNode();
    Node testNode = rootNode.addNode("testNode", "nt:unstructured");

    // добавляем свойства
    testNode.setProperty("testProperty1", "test value 1");
    testNode.setProperty("testProperty2", 123);
    testNode.setProperty("testProperty3", true);
    testNode.setProperty("testProperty4", new String[] {"value1", "value2", "value3"});

    // добавляем дочерние узлы
    Node childNode1 = testNode.addNode("childNode1", "nt:unstructured");
    childNode1.setProperty("childProperty1", "child value 1");
    Node childNode2 = testNode.addNode("childNode2", "nt:unstructured");
    childNode2.setProperty("childProperty2", "child value 2");

    session.save();

    // читаем узел
    Node readNode = rootNode.getNode("testNode");
    String propertyValue1 = readNode.getProperty("testProperty1").getString();
    long propertyValue2 = readNode.getProperty("testProperty2").getLong();
    boolean propertyValue3 = readNode.getProperty("testProperty3").getBoolean();
    String[] propertyValue4 = readNode.getProperty("testProperty4").getValue(PropertyType.STRING).getValues();
    Node readChildNode1 = readNode.getNode("childNode1");
    String childPropertyValue1 = readChildNode1.getProperty("childProperty1").getString();
    Node readChildNode2 = readNode.getNode("childNode2");
    String childPropertyValue2 = readChildNode2.getProperty("childProperty2").getString();

    System.out.println("Property value 1: " + propertyValue1);
    System.out.println("Property value 2: " + propertyValue2);
    System.out.println("Property value 3: " + propertyValue3);
    System.out.println("Property value 4: " + String.join(", ", propertyValue4));
    System.out.println("Child property value 1: " + childPropertyValue1);
    System.out.println("Child property value 2: " + childPropertyValue2);

    // закрываем сессию
    session.logout();
  }
}
```

*Вывод консоли:*
```
Property value 1: test value 1
Property value 2: 123
Property value 3: true
Property value 4: value1, value2, value3
Child property value 1: child value 1
Child property value 2: child value 2
```

## Демобаза
Apache Jackrabbit Oak GitHub репозиторий содержит несколько примеров демобаз, которые я использовал для изучения языка запросов. Ссылка на репозиторий: https://github.com/apache/jackrabbit-oak

Помимо этого, я просматривал туториалы Apache Jackrabbit Oak Tutorials. Ссылка: https://jackrabbit.apache.org/oak/docs/tutorials.html

Ещё один отличный ресурс это Apache Jackrabbit Wiki - место, где можно найти много информации о СУБД, включая примеры демобаз и языка запросов. Ссылка на Wiki: https://cwiki.apache.org/confluence/display/JCR/Home

## Документация / Как быть в курсе происходящего
https://jackrabbit.apache.org/jcr/index.html
