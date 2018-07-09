# POSTGRESQL

## JSON 数据类型

pg支持两种 JSON和JSONB两种json数据类型,他们基本相同.但是如果要以二进制格式保存json文档,那么jsonb更有效,而且支持索引.

当使用json时,尽量使用UTF8做数据库编码格式.JSON文档存储时是以文档格式保存,并且当把JSON对象保存为JSONB时,JSON的原始数据类型主要为`string Boolean`,number类型会被映射为文本

json 存储的数据几乎和输入数据一样，存储的是未解析的数据，调用函数时使用效率较低; 而 jsonb 存储的是分解的 binary 格式数据，使用时不需要再解析了，因此使用上效率较高; 另一方面 json 在写入时较快，而 jsonb 写入时由于需要转换导致写入较慢

### 修改以及访问JSON类型

把text转为JSON时,text内容不会被修改,JSON类型会抱回空格.数字格式,以及元素的排列顺序.JSONB则不会保护这些信息

```sql
CREATE TABLE test_json(
  doc json
);
CREATE TABLE test_jsonb (
doc jsonb );

INSERT INTO test_json  VALUES ('{"car_id":1,      "model":"BMW"}'::json),
  ('{"name":"some name", "name":"some name"}'::json);
INSERT INTO test_jsonb  VALUES ('{"car_id":1,
"model":"BMW"}'::jsonb),
  ('{"name":"some name", "name":"some name"}'::jsonb);
SELECT * FROM test_json;
                   doc
------------------------------------------
 {"car_id":1,      "model":"BMW"}
 {"name":"some name", "name":"some name"}

SELECT * FROM test_jsonb;
              doc
-------------------------------
 {"model": "BMW", "car_id": 1}
 {"name": "some name"}

```

JSON类型数据中还可以任意的嵌套json数据.
```sql
INSERT INTO test_jsonb VALUES ('{"name":"John", "Address":{"Street":"Some street", "city":"Some city"}, "rank":[5,3,4,5,2,3,4,5]}'::JSONB);
```

- =	    jsonb	两个jsonb是否相等	'[1,2,3]'::jsonb = '[1,2,3]'::jsonb
- @>	jsonb	左边的jsonb是否包含右边的json	'{"a":1, "b":2}'::jsonb @> '{"b":2}'::jsonb
- <@	jsonb	左边的jsonb是否包含在右边的json	'{"b":2}'::jsonb <@ '{"a":1, "b":2}'::jsonb
- ?	     text	json中是否包含右边的key/element	'{"a":1, "b":2}'::jsonb ? 'b'
- ?|	text[]	json的是否包含右边的列表中任意一个key/element '{"a":1, "b":2, "c":3}'::jsonb ?| array['b', 'c']
- ?&	text[]	json是否全部包含右边列表中key/element	'["a", "b"]'::jsonb ?& array['a', 'b']

如果json中潜逃了json,那么可以使用
- `->` `->>` 来一步步往下查询
This returns a JSON field either using the field index or field name
- `#>` `#>>` 按照给定的路径查找

```sql
INSERT INTO test_jsonb VALUES ('{"name":"John", "Address":{"Street":"Some street", "city":{"Street":"Some street", "city":"Some city"}}, "rank":[5,3,4,5,2,3,4,5]}'::JSONB);

SELECT doc->'Address'->'city'->>'city', doc#>>'{Address, city, city}' FROM test_jsonb;
```

条件查询

```sql
SELECT doc->'Address'->'city'->>'city', doc#>>'{Address, city, city}' FROM test_jsonb where doc->'Address'->'city'->>'city'='Some city';
SELECT doc->'Address'->'city'->>'city', doc#>>'{Address, city, Street}' FROM test_jsonb where doc#>>'{Address,city,city}'='Some city';
```

**目前还没有办法单独更新json中的某个字段**


##  [JSON 函数和操作](https://www.postgresql.org/docs/9.5/static/functions-json.html)

# 文档

## 允许远程链接

```bash
# vim /etc/postgresql/9.5/main/postgresql.conf
listen_addresses = '*'

# vim /etc/postgresql/9.5/main/pg_hba.conf
# IPv4 local connections:
host    all             all             192.168.1.1/24          md5
```

