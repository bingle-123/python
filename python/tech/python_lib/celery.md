# 分布式任务队列

Celery的工作单元是消息队列中的消息。celery支持多种broker(例如RabbitMQ，Redis)

# First Steps with Celery
Celery推荐使用rabbitmq作为消息队列

## 将Celery应用到系统中

结构

```
proj/__init__.py
    /celery.py
    /tasks.py
```

proj/celery.py 这个模块创建Celery的实例,在系统中使用Celery只需导入这个实例。有几个参数：

- broker:broker的URL
- backend:用来跟踪任务的状态和结果。默认结果是不可用的。如果不需要结果的话，不传这个参数，也可以在`@task(ignore_result=True)`来禁用结果
- include:当worker启动的时导入的模块列表，这里导入tasks,这样worker就能找到任务。

```python
from __future__ import absolute_import
from celery import Celery

app = Celery('proj',
             broker='amqp://guest:guest@localhost//',
             backend='amqp://',
             include=['proj.tasks'])

# Optional configuration, see the application user guide.
app.conf.update(
    CELERY_TASK_RESULT_EXPIRES=3600,
)

if __name__ == '__main__':
    app.start()
```

proj/tasks.py

```python
from __future__ import absolute_import
from proj.celery import app

@app.task
def add(x, y):
    return x + y

@app.task
def mul(x, y):
    return x * y

@app.task
def xsum(numbers):
    return sum(numbers)
```

启动任务 `celery -A proj worker -l info`

### 后台运行

启动`celery multi start w1 -A proj -l info`

重新启动 `celery multi restart w1 -A proj -l info`

停止 `celery multi stop w1 -A proj -l info`

确保所有任务之心完毕再停止`celery multi stopwait w1 -A proj -l info`

### 调用任务

使用任务的delay方法来执行任务。

```python
from proj.task import add

result = add.delay(2,4)
result.state # SUCCESS
result.result # 6
```

这个方法实际是`apply_async()`的简写，`add.apply_async((2, 2))`,apply_async方法支持跟多的参数，例如给哪一个队列发送，执行次数等 `add.apply_async((2, 2), queue='lopri', countdown=10)`,上面这个任务会发送给`lopri`队列，并且在消息发送完成10秒后执行任务。

如果直接调用任务本身`add(2, 2)`那么他不会发送任何消息。

如果使用了backend那么可以查看任务的结果

```python
res = add.delay(2, 2)
res.get(timeout=1)#4
# 如果没有获取到结果，get会抛出异常，通过propagate=False可以不抛出异常
res.get(propagate=False)

res.failed() #True
res.successful()#False
res.state #'FAILURE'
```

任务有三个状态 PENDING->STARTED->SUCCESS

STARTED这个状态只有当Celery设置了`CELERY_TRACK_STARTED`,或者`@task(track_started=True)`才会有
