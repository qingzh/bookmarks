定时任务

* Linux下, 可以使用 crontab:
例如每三个小时定时跑脚本 `some_script.sh`
```bash
$crontab -e 
12 */3 * * * cd $HOME/scripts && sh some_script.sh
```

而在pyhton中我们可以使用 redis + celery

#### 依赖的库
* redis
* celery

#### 准备 worker
1. 任务脚本 tasks.py
```python
from celery import Celery

# redis port: 7979, db: 0
app = Celery('hello', broker='redis://localhost:7979/0')

@app.task
def hellocelery(x):
    return 'hello celery: %s' % x
```
2. 启动 celery
```bash
$celery -A tasks worker --loglevel=debug
```

#### 执行任务
从 celery 的 worker 中选取执行
```bash
$ipython
>>> from tasks import hellocelery
>>> hellocelery.delay('1')
```

#### 定时任务

1. 定时任务配置, 在 tasks.py 中添加如下代码
```python
from datetime import timedelta
from celery.schedules import crontab

app.conf.CELERYBEAT_SCHEDULE = {
    'every-10-seconds': {
        'task': 'tasks.hellocelery',
        # every 10 seconds
        'schedule': timedelta(seconds=10),
        'args': ('10seconds', ),
    },
    'every-minutes': {
        'task': 'tasks.hellocelery',
        # every minutes
        'schedule': crontab(hour='*', minute='*/1'),
        'args': ('minutes', ),
    }
}
```

2. 启动 celery
```bash
$celery -A tasks worker -B --loglevel=debug
```
可以观察到如下日志:
```bash
[2016-03-11 13:48:54,478: INFO/Beat] Scheduler: Sending due task every-10-seconds (tasks.hellocelery)
[2016-03-11 13:48:54,479: DEBUG/Beat] tasks.hellocelery sent. id->952013aa-2f4f-44d6-93b8-5b45109acbb1
[2016-03-11 13:48:54,479: DEBUG/Beat] beat: Waking up in 5.51 seconds.
[2016-03-11 13:48:54,479: INFO/MainProcess] Received task: tasks.hellocelery[952013aa-2f4f-44d6-93b8-5b45109acbb1]
[2016-03-11 13:48:54,479: DEBUG/MainProcess] TaskPool: Apply <function _fast_trace_task at 0x7fce877ef398> (args:('tasks.hellocelery', '952013aa-2f4f-44d6-93b8-5b45109acbb1', ('10seconds',), {}, {'utc': True, u'is_eager': False, 'chord': None, u'group': None, 'args': ('10seconds',), 'retries': 0, u'delivery_info': {u'priority': 0, u'redelivered': None, u'routing_key': u'celery', u'exchange': u'celery'}, 'expires': None, u'hostname': 'celery@rb4a03295.cm8', 'task': 'tasks.hellocelery', 'callbacks': None, u'correlation_id': u'952013aa-2f4f-44d6-93b8-5b45109acbb1', 'errbacks': None, 'timelimit': (None, None), 'taskset': None, 'kwargs': {}, 'eta': None, u'reply_to': u'31c5dfdf-fdf2-38fd-a9f8-8dbc885abe7e', 'id': '952013aa-2f4f-44d6-93b8-5b45109acbb1', u'headers': {}}) kwargs:{})
[2016-03-11 13:48:54,481: DEBUG/MainProcess] Task accepted: tasks.hellocelery[952013aa-2f4f-44d6-93b8-5b45109acbb1] pid:10938
[2016-03-11 13:48:54,482: INFO/MainProcess] Task tasks.hellocelery[952013aa-2f4f-44d6-93b8-5b45109acbb1] succeeded in 0.00149638205767s: 'hello celery: 10seconds'
[2016-03-11 13:49:00,000: INFO/Beat] Scheduler: Sending due task every-minutes (tasks.hellocelery)
[2016-03-11 13:49:00,001: DEBUG/Beat] tasks.hellocelery sent. id->c352ec20-9387-49d5-bcdd-9787ca69002c
[2016-03-11 13:49:00,001: DEBUG/Beat] beat: Waking up in 4.47 seconds.
[2016-03-11 13:49:00,002: INFO/MainProcess] Received task: tasks.hellocelery[c352ec20-9387-49d5-bcdd-9787ca69002c]
[2016-03-11 13:49:00,002: DEBUG/MainProcess] TaskPool: Apply <function _fast_trace_task at 0x7fce877ef398> (args:('tasks.hellocelery', 'c352ec20-9387-49d5-bcdd-9787ca69002c', ('minutes',), {}, {'utc': True, u'is_eager': False, 'chord': None, u'group': None, 'args': ('minutes',), 'retries': 0, u'delivery_info': {u'priority': 0, u'redelivered': None, u'routing_key': u'celery', u'exchange': u'celery'}, 'expires': None, u'hostname': 'celery@rb4a03295.cm8', 'task': 'tasks.hellocelery', 'callbacks': None, u'correlation_id': u'c352ec20-9387-49d5-bcdd-9787ca69002c', 'errbacks': None, 'timelimit': (None, None), 'taskset': None, 'kwargs': {}, 'eta': None, u'reply_to': u'31c5dfdf-fdf2-38fd-a9f8-8dbc885abe7e', 'id': 'c352ec20-9387-49d5-bcdd-9787ca69002c', u'headers': {}}) kwargs:{})
[2016-03-11 13:49:00,003: DEBUG/MainProcess] Task accepted: tasks.hellocelery[c352ec20-9387-49d5-bcdd-9787ca69002c] pid:10953
[2016-03-11 13:49:00,004: INFO/MainProcess] Task tasks.hellocelery[c352ec20-9387-49d5-bcdd-9787ca69002c] succeeded in 0.0014569349587s: 'hello celery: minutes'
```

#### Celery配置
1. 编写配置文件 celeryconfig :
```python
# broker设置
BROKER_URL = 'amqp://'
# 存储任务结果                     
CELERY_RESULT_BACKEND = 'amqp://'
# celery任务结果有效期      
CELERY_TASK_RESULT_EXPIRES = 18000          

# 任务序列化格式
CELERY_TASK_SERIALIZER = 'json'
# 结果序列化格式               
CELERY_RESULT_SERIALIZER = 'json'   
# celery接收内容类型, 默认: ['pickle', 'json', 'msgpack', 'yaml']          
CELERY_ACCEPT_CONTENT=['json']

# celery使用的时区         
CELERY_TIMEZONE = 'Asia/Shanghai'
# 启动时区设置                
CELERY_ENABLE_UTC = True

# celery日志存储位置              
CELERYD_LOG_FILE="/var/log/celery/celery.log"  

from kombu.common import Broadcast 
# 任务队列的类型
CELERY_QUEUES = (Broadcast('broadcast_logger'), )
# 任务队列      
CELERY_ROUTES = {                                      
    'log_analysis.run': {'queue': 'api.log'},  
    'logrotate': {'queue': 'broadcast_logger'},  
} 

# celery错误邮件通知配置
CELERY_SEND_TASK_ERROR_EMAILS = True
# celery错误邮件接收地址          
ADMINS = (  
    ("*****", "*****@***.com"),        
)   
# celery错误邮件发件人配置
SERVER_EMAIL = ****@***.com        
EMAIL_HOST = "*.*.*.*"                     
EMAIL_PORT = 25  
EMAIL_HOST_USER = SERVER_EMAIL   

# celery定时任务  
CELERYBEAT_SCHEDULE = {                                
    # 接口中心每小时 *:30
    'api.hour':{'task': 'api.hour', 'schedule': crontab(minute=30), 'args': ()},  
    # 接口中心每日 0:30 分 
    'api.day':{'task': 'api.day', 'schedule': crontab(minute=30, hour=0), 'args': ()},  
}  
```
2. 在 tasks.py 中导入配置文件
```python
app.config_from_object('celeryconfig')
```