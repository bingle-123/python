# Fabric3(python3)

fabric可以执行py文件中的函数,可以给函数传递参数

在项目根目录下创建一个`fabfile.py`文件或者是`fabfile包`

fab寻找文件的方式:

- 当前目录下是否有`fabfile.py`文件
- 当前目录下是否有fabfile文件夹,并且该文件夹下包含`__init__.py`
- 通过命令行参数`-f f_name.py`指定文件
- `~/.fabricrc` 中添加`fabfile = fab_tasks.py`

`fab func_name`会直接调用找到的fabric文件中的`func_name`函数,传递参数`fab func_name:var1=value1'`

