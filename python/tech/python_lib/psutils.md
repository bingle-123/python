# psutil

`pip install psutil`

## 按进程名杀死某个进程

```python
import psutil
for proc in psutil.process_iter():
    if proc.name().startswith('notepad'):
        proc.kill()
```



## CPU

