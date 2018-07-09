# Django

## Django 启动过程

`./manage.py runserver --runserver --noreload --nothreading`

`django/core/management/__init__.py`-->`execute_from_command_line(argv)`

```python
def execute_from_command_line(argv=None):
    """Run a ManagementUtility."""
    utility = ManagementUtility(argv)
    utility.execute()
```





## Django请求到返回

