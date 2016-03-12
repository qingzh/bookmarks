#! -*- coding:utf8 -*-

"""
Prerequisite:
* redis
* celery
"""

from celery import Celery


app = Celery('hello', broker='redis://localhost:7979/0')

# name: zq.hello; app.tasks['zq.hello']
#@app.task(name="zq.hello")
#
# name: tasks.hellocelery; app.tasks['tasks.hellocelery']
#@app.task
#
# name: hello; app.tasks['hello']
#@app.task(name="hello")
#


@app.task
def hellocelery(x):
    return 'hello celery: %s' % x

app.config_from_object('celeryconfig')

