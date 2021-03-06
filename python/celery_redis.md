# Celery и Redis

## Простой пример использования celery

Предположим, у нас есть функция, которая получает список адресов и выполняет запрос для каждого указанного адреса (возможно, мы хотели бы скопировать каталоги нескольких интернет-магазинов, или выполняем сбор данных для машинного обучения, но в данном примере мы используем нейтральные URL).

### Без celery

```python
import requests
import time

def func(urls):
    start = time.time()
    for url in urls:
        resp = requests.get(url)
        print(resp.status_code)

    print("It took", time.time() - start, "seconds")

if __name__ == "__main__":
    func(["http://google.com", "https://facebook.com", "https://twitter.com"])
```

Запускаем:
<pre>
$ python3 celery_example.py
</pre>

Вывод:
<pre>
200
200
200
It took 2.1733005046844482 seconds
</pre>

### Используем celery

Главным компонентом программы с поддержкой celery является воркер - worker.

В примере с регистрацией пользователя на сайте, именно worker выполнял бы работу по отправке электронных писем. В примере с запросом данных, worker будет выполнять запросы по указанным адресам.

Celery worker и ваше приложение (скрипт) - это разные процессы, которые работают независимо друг от друга. Для того, чтоб приложение (скрипт) и celery могли каким-то образом общаться, взаимодействовать друг с другом, удобно использовать очередь сообщений. Приложение оставляет в очереди задачу, celery worker извлекает ее и обрабатывает. В качестве очереди сообщений будем использовать redis.

Перед началом экспериментов убедитесь, что redis установлен и вы можете запустить redis-server. Также убедитесь, что у вас установлен celery.

Измените свой файл *celery_example.py*, чтобы он выглядел так:

```python
import requests
from celery import Celery

app = Celery('celery_example', broker='redis://localhost:6379/0')

@app.task
def fetch_url(url):
    resp = requests.get(url)
    print(resp.status_code)

def func(urls):
    for url in urls:
        fetch_url.delay(url)


if __name__ == "__main__":
    func(["http://google.com", "https://facebook.com", "https://twitter.com"])
```

Создаем экземпляр Celery - app, первый аргумент - имя модуля, второй аргумент - URL брокера сообщений.

Понятия "очередь сообщений" и "брокер сообщений" - часто используются как синонимы. Celery может выполнять несколько процессов параллельно. Мы хотим выполнять запросы по указанным нами адресам параллельно, а не последовательно. Поэтому, нам нужна функция, которая может работать с одним URL, и мы будем запускать эту функцию в 3-х параллельных процессах.

Итак, мы написали задачу celery с именем fetch_url, эта задача может работать с одним URL. Задача celery - это просто функция, с примененным к ней декоратором app.task.

Из нашей старой функции мы вызывали задачу 3 раза последовательно, каждый раз передавая разные адреса.

Когда мы говорим "fetch_url.delay(url)", код сериализуется и помещается в очередь сообщений (в нашем случае - БД redis). Celery worker при запуске будет читать сериализованную задачу из очереди, проводить десериализацию и выполнение.

Для демонстрации работы нашего примера используем два терминала.
1. Запускаем сервер redis, например так:
<pre>
$ service redis start
</pre>
Далее запускаем воркера celery:
<pre>
/usr/local/bin/celery worker -A celery_example -l info -c 3
</pre>
Увидев вывод, вы сможете понять работает celery или при запуске произошла ошибка.

2. Во втором терминале запускаем скрипт, который поместит в очередь задачи:
<pre>
$ python3 celery_example.py
</pre>
Выполнение celery_example.py не даст никакого вывода на экран. Вывод, связанный с обработкой наших URL, надо смотреть в первом терминале, где запущен celery, ведь именно он будет выполнять поставленные в очередь задачи. В терминале, где запущен celery, мы увидим нечто вроде этого:
<pre>
...
[2020-03-26 11:34:42,617: INFO/MainProcess] Received task: celery_example.fetch_url
[5bf57e5d-5244-4746-86a2-b2120d36a6c0]..
[2020-03-26 11:34:42,622: INFO/MainProcess] Received task: celery_example.fetch_url
[cf134a7f-e0a7-4f56-83c9-0d46c50cb292]..
[2020-03-26 11:34:42,635: INFO/MainProcess] Received task: celery_example.fetch_url
[9ae9163b-dced-450a-95a6-d1ff45021d69]..
[2020-03-26 11:34:42,840: WARNING/ForkPoolWorker-2] 200
[2020-03-26 11:34:42,841: INFO/ForkPoolWorker-2] Task celery_example.fetch_url
[5bf57e5d-5244-4746-86a2-b2120d36a6c0] succeeded in 0.2179497969991644s: None
[2020-03-26 11:34:43,637: WARNING/ForkPoolWorker-1] 200
[2020-03-26 11:34:43,638: INFO/ForkPoolWorker-1] Task celery_example.fetch_url
[cf134a7f-e0a7-4f56-83c9-0d46c50cb292] succeeded in 1.0151048970001284s: None
[2020-03-26 11:34:43,975: WARNING/ForkPoolWorker-3] 200
[2020-03-26 11:34:43,977: INFO/ForkPoolWorker-3] Task celery_example.fetch_url
[9ae9163b-dced-450a-95a6-d1ff45021d69] succeeded in 1.3335965090009267s: None
...
</pre>
На самом деле, ваш вывод может не соответствовать приведенному в качестве примера, т.к. вывод зависит от версии используемых вами продуктов.

Первое, на что нужно обратить внимание, это то, что весь вывод celery был напечатан гораздо меньше, чем за 2 секунды. Ранее для получения ответа по 3 URL потребовалось около 2 секунд. С celery это заняло в два раза меньше времени, и экономия времени будет тем значимей, чем больше адресов мы опрашиваем.

#### celery worker -A celery_example -l info -c 3

"-c 3" означает указание celery запустить 3 параллельных подпроцесса. Каждый подпроцесс выполняет одну задачу.

"-l info" - уровень логирования, "info" означает, что мы хотим максимально подробный вывод.

"-A celery_example" - говорит, что конфигурация celery, которая включает в себя приложение и задачи, о которых должен знать celery worker, хранится в модуле celery_example.py.

#### Комментарии о работе celery с нашим примером кода

Celery worker одновременно запускает 3 подпроцесса, которые он называет Worker-1, Worker-2 и так далее.

Нет необходимости, чтобы задачи извлекались в том же порядке, в каком они были добавлены в список.

Когда мы запустили python *celery_example.py*, задачи были созданы и помещены в очередь сообщений, которая размещена в БД redis.

Celery постоянно опрашивает очередь redis, и выбирает появляющиеся задачи.

Celery десериализует каждую отдельную задачу и заставляет каждую отдельную задачу выполняться в рамках подпроцесса.

Celery не ждет завершения первого задания/подпроцесса, прежде чем приступить ко второму заданию. Пока первое задание
все еще выполняется, celery worker извлекает второе задание, десериализует его и передает другому подпроцессу.

## Хранение кода и конфигурации Celery в разных файлах

В нашем примере мы работали всего с одной задачей. Но реальный проект может охватывать множество модулей с множеством
разных задач. В этом случае лучше перенести конфигурацию celery в отдельный файл.

Создаем файл *celery_config.py*:

```python
from celery import Celery

app = Celery('celery_config', broker='redis://localhost:6379/0', include=['celery_example'])
```

Изменяем *celery_example.py*:

```python
import requests
from celery_config import app

@app.task
def fetch_url(url):
    resp = requests.get(url)
    print(resp.status_code)

def func(urls):
    for url in urls:
        fetch_url.delay(url)

if __name__ == "__main__":
    func(["http://google.com", "https://facebook.com", "https://twitter.com"])
```

Теперь celery worker будет запускаться командой:
<pre>
$ celery worker -A celery_config -l info -c 3
</pre>

Запустите интерпретатор python и введите код:
<pre>
>>> from celery_example import func
>>> func(['http://dev-lab.info', 'http://ya.ru'])
</pre>

Celery немедленно отреагирует:
<pre>
[2020-03-26 13:11:31,449: WARNING/ForkPoolWorker-1] 200
[2020-03-26 13:11:31,450: INFO/ForkPoolWorker-1] Task celery_example.fetch_url[9426f1af-256d-4220-9ff8-38c185d05274]
succeeded in 0.3073845450016961s: None
[2020-03-26 13:11:32,052: WARNING/ForkPoolWorker-3] 200
[2020-03-26 13:11:32,054: INFO/ForkPoolWorker-3] Task celery_example.fetch_url[83a84a46-b776-40c1-8680-e033a5a0eae2]
succeeded in 0.9161740339986864s: None
</pre>

## Добавление еще одной задачи для celery

Вы можете добавить другой модуль и определить задачу в этом модуле.

Создайте модуль *celery_example_2.py* со следующим содержимым:

```python
from celery_config import app

@app.task
def add(a, b):
    return a + b
```

Измените *celery_config.py*, чтобы включить новый модуль *celery_example_2.py*:

```python
from celery import Celery

app = Celery('celery_config', broker='redis://localhost:6379/0', include=['celery_example', 'celery_example_2'])
```

Попробуйте добавить новую задачу в очередь:
<pre>
>>> from celery_example_2 import add
>>> add.delay(4, 5)
AsyncResult: dfe34202-f710-448b-9748-7fc75fb86d8d>
</pre>

Вывод celery worker:
<pre>
[2020-03-26 13:16:10,315: INFO/MainProcess] Received task: celery_example_2.add
[dfe34202-f710-448b-9748-7fc75fb86d8d]..
[2020-03-26 13:16:10,318: INFO/ForkPoolWorker-3] Task celery_example_2.add
[dfe34202-f710-448b-9748-7fc75fb86d8d] succeeded in 0.0006317919978755526s: 9
</pre>

## Использование celery с пакетом

Мы продолжаем работать с *celery_config.py*. Рассмотрим директорию, которая содержит *celery_config.py*
и является корневым каталогом вашего проекта.

Создайте пакет с именем pack на том же уровне, что и *celery_config.py*.

Создайте файл *pack/celery_example_3.py* со следующим содержимым:

```python
import requests
from celery_config import app

@app.task
def fetch_url(url):
    resp = requests.get(url)
    print(resp.status_code)

def func(urls):
    for url in urls:
        fetch_url.delay(url)
```

Измените celery_config.py:
```python
from celery import Celery
app = Celery('celery_config', broker='redis://localhost:6379/0', include=['pack.celery_example_3']
```

Запускаем celery worker:
<pre>
/usr/local/bin/celery worker -A celery_config -l info -c 3
</pre>
Убедитесь, что вы видите в выводе строки:
<pre>
[tasks]
  . pack.celery_example_3.fetch_url
</pre>
Теперь используйте func:
<pre>
>>> from pack.celery_example_3 import func
>>> func(['https://google.com', 'https://facebook.com'])
</pre>

## Redis и celery на отдельных машинах

До сих пор наш скрипт, **celery** и **redis** работали на одной машине. Но это не обязательно.

Задачи **celery** должны выполнять сетевые вызовы. Таким образом, выполнение **celery worker** на компьютере, который оптимизирован
для работы с сетью, ускорит выполнение задач. **Redis** - это база данных в памяти, поэтому, если **redis**.
будет работать на машине, оптимизированной под нужды подобных хранилищ данных - это также хорошо скажется на
эффективности всей системы.

Чтоб начать использовать **redis**, размещенный на отдельной машине, нам надо внести изменения в файл *celery_config.py*,
изменив ip-адрес брокера сообщений:
```python
app = Celery('celery_config', broker='redis://54.69.176.94:6379/0', include=['celery_example_3'])
```

## Celery и веб-приложение/скрипт на отдельных машинах

Как упоминалось ранее, **celery worker** и ваша программа являются отдельными процессами и не зависят друг от друга.
Можно запустить их на разных машинах.

Предположим, у вас есть сервер **54.69.176.94**, на котором вы хотите запустить **celery**, но вы хотите продолжать
запускать скрипт на локальном компьютере.

Скопируйте файлы *celery_config.py* и *celery_example.py* на сервер (54.69.176.94).
Запустите **"celery worker -A celery_config -l info"** на сервере.

Используя локальный компьютер, поместите в очередь задачу. Очередь является общей для всех, и для нашего
локального скрипта, и для **celery worker**, запущенного на удаленном сервере. Worker получит задачу из очереди и выполнит ее.
