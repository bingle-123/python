# JSON

概念：一种保存数据的格式

作用：可以保存本地的json文件，页可以将json串进行传输，通常将json称为轻量级的传输方式

json文件组成

{}     代表对象(字典)

[]     代表列表

:      代表键值对

,     分隔两个部分

```

import json

jsonStr = '{"name":"sunck凯", "age":18, "hobby":["money","power","english"], "parames":{"a":1,"b":2}}'
```

## 将json格式的字符串转为python数据类型的对象
```python
jsonData = json.loads(jsonStr)

print(jsonData)

print(type(jsonData))

print(jsonData["hobby"])
```

## 将python数据类型的对象转为json格式的字符串

```
jsonData2 = {"name":"sunck凯", "age":18, "hobby":["money","power","english"], "parames":{"a":1,"b":2}}

jsonStr2 = json.dumps(jsonData2)

print(jsonStr2)

print(type(jsonStr2))
```


## 读取本地的json文件

```
path1 = r"C:\Users\xlg\Desktop\Python-1704\day18\Json\caidanJson.json"

with open(path1, "rb") as f:

data = json.load(f)
print(data)
# 字典类型
print(type(data))
```

## 写本地json

```
path2 = ` r"C:\Users\xlg\Desktop\Python-1704\day18\Json\test.json" `

jsonData3 = {"name":"sunck凯", "age":18, "hobby":["money","power","english"], "parames":{"a":1,"b":2}}

with open(path2, "w") as f:

json.dump(jsonData3, f)
```

