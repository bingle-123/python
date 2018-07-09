Python作业调度工具
```python
import schedule
import time

def job():
print("I'm working...")

schedule.every(10).minutes.do(job)
schedule.every().hour.do(job)
schedule.every().day.at("10:30").do(job)

while True:#类似于守护进程
    schedule.run_pending()
    time.sleep(1)
```
