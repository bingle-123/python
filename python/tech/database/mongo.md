# mongodb权威指南2

# 基础知识

## 数据类型

JSON: null,bool,number,string,array,object

**null:**

{"x":null} 表示空值或不存在的值

**布尔型:**

{"x":true|false}

**数值:**

浮点数默认是64位浮点型,整数可以是NumberInt或者NumberLong  
{"x":NumberInt("3")}也可以是{"x":NumberLong("3")}

**日期:**

{"x":new Date()} *这里必须使用new,如果不适用new,那么存储的是Date函数*

**数组:**

{"x":[1,2,3]}

**内嵌文档:**

{"x":{"foo":"bar"}}

**对象:**

{"x":ObjectId()}

**二进制:**如果要将非UTF-8字符串保存数据库中,二进制是唯一的方式

**代码:**查询和文档中可以包括任意的JavaScript代码

{"x":function(){/*....*/}}

## `_id`和`ObjectId`

每一个文档都必须有个`_id`键,确保每一个文档在集合中是惟一的

ObjectId是`_id`的默认类型.使用12字节的存储空间,前4个字节是时间戳秒级别,567字节是机器主机名的hash,78是PID,最后3个字节是自动增加的计数器,每个进行,每秒可以有2563个不同ObjectID,进程最多有256

## 脚本

`mongo script1.js script2.js`也可以在命令行中`> load("script1.js")`

命令行可以使用run函数来执行shell 命令:`run("ls" ,"-l" ,"/")`

主目录下的`.mongorc.js`会在每次启动mongo时,自动执行 使用`--norc`来禁止加载mongorc

例如:
```JavaScript
var no =funtion(){
    print("not on my Watch");
}
db.dropDatabase=DB.prototype.dropDatabase=no;//禁止删除数据库
```

**编辑复合变量:** shell不可以编辑之前的行,可以在在shell中设置`> EDITOR="/usr/bin/vim"` 然后`edit varname`就可以编辑了

# 创建,更新,删除

## 插入

`db.foo.insert({}) db.foo.insert([{...},{...},...])`

### 插入校验

如果没有`_id`会自动生层`_id`

每个文档不超过16MB,`Object.bsonsize(doc)`来查看文档大小

## 删除文档

`db.foo.remove(filter)`

清空集合`db.blog.drop()`

## 更新文档

`db.users.update({"name":"joe"},joe)`

### 修改器

`db.users.update({"name":"joe"},{"$inc":{"pageviews":1}})`pageviews+1

$set用来指定一个字段的值,如果字段不存在就添加

`db.users.update({"name":"joe"},{"$set":{"pageviews":1}})`

$unset删除某个键

`db.users.update({"name":"joe"},{"$unset":{"favorite book":1}})`

修改内键文档

`db.users.update({"name":"joe"},{"$set":{"author.name":"joe schmoe"}})`

$inc增加或减少

$push向数组中追加元素,如果没有数组就创建,结合$each可以一次push多个值,结合$slice可以限制数组长度,$sort对数组元素排序

```JavaScript
db.movie.update({"_id":'_IDxxx'},
{
    "$push":{"hourly":{
        "$each":[{"name":"a","rating":4.5},{"name":"b","rating":4}],
        "$slice":-10,//限制长度不超过10
        "$sort":{"rating":-1}//倒序排
        }
    }
})
```

$addToSet确保加入数组中的元素不会重复

$pop从数组中删除元素

`{"$pop":{"key":1}}`删除第一个`{"$pop":{"key":-1}}`倒数第一个

$pull从数组中删除所有匹配的元素

`{"$pull":{"list":"abc"}}`

基于位置修改数组元素的值

`db.blog.update({...},{"$inc":{"comments.0.votes":1}})`

通常必须要知道查询的位置,才能根据位置修改元素的值,`$`用来定义查询文档已经匹配的数组元素

`db.blog.update({'comments.author':"john"},{"$set":{"comments.$.author":"jim"}})`

**速度:**$inc可以就地修改文档,速度很快,但是如果更新值,导致了文档大小的变化,就会慢一些.mongodb中插入文档时在磁盘上是相邻的,如果一个文档大小发生变化了,那么就要把文档移到其他位置,原来的位置就会空

mongo会为每个文档分配精确的空间,不留增长空间

**push会改变文档大小,要移动文档,所以可能会导致性能降低**

### upsert

如果没有找到文档,就直接创建文档`update({..},{...},true)`表示upsert

例如:`update({'rep':25},{'$inc':3},true)`会创建`{'rep':28}`

### save

save会直接更新文档,如果文档包含`_id`那么会调用upsert

```
var x=db.foo.findOne()
x.name='aaaa'
db.foo.save(x)
//相当于
db.foo.update({'_id':x._id},x)
```

### 更新多个文档

update默认只更新第一个文档,如果全部更新,那么第四个参数true;`update({...},{...},false,true)`

## 写入安全

应答和非应答,非应答不会给出错误提示,需要通过getLastError来获取错误

# 查询

find或者findOne,使用`$`条件查询实现单位查询,数据集包含查询,不等式查询等,查询会返回数据库游标,游标只会在需要的时候才将需要的文档返回

## find

find的第一个参数默认值是`{}`,匹配所有内容`{}`中内容是and操作

指定返回的键`find({},{"key1":1,"key2":1,"_id":0})`默认`_id`是返回的

## 查询条件

**$lt,$gt,$lte,$gte,$ne**:`find({'age':{"$gte":10,'$lte':20}})`

**$in**

`find({'user_ui':{"$in":[1,3,5,6]}})`

**$or**:`find({'$or':[{'ticket_no':724},{'winnner':true}]})`

**$not**:`find({"id_num":{"$not":{"$mod":[5,1]}}})`



# 索引

唯一索引 `db.users.ensureIndex({"username":1},{"unique":true})`

复合唯一索引 `db.users.ensureIndex({"username":1,"age":1},{"unique":true})`

稀疏索引: **唯一索引会把null看成值,所以无法把多个缺少唯一索引的文档插入集合中,那么要结合稀疏索引**稀疏索引不必是唯一的可以去掉unique `db.ensureIndex({"email":1},{"unique":true,"sparse":true})`

# 特殊的索引和集合

固定集合具有固定大小空间,满时老的会被删除

创建固定集合`db.createCollection("my_collection",{"capped":true,"size":100000})`size字节单位

固定集合按照存储顺序进行排序,也叫自然排序,就是老-->新,可以反向排序`db.my_collection.find().sort({'$natural':-1})`

**循环游标:**类似于`tail -f`,当游标没有数据时,就暂停,当新的数据到来时,继续处理,如果10分钟内没有新的数据,那么游标就关闭.`var cursor=db.my_collection.find().tailable()`


## TTL 索引

类似于缓存系统,给文档设置过期时间,`db.foo.ensureIndex({"lastUpdated":1},{"expireAfterSec":60*60*24})` 单位秒

## 全文本索引

创建任何索引开销都很大,全文索引更大,

在操作频繁的集合上创建全文索引可能导致mongodb过载,所以应该在应用离线状态下创建全文索引,后者在性能没有要求时

因为所有字符串都要被分解,分词,并保存到一些地方,索引全文本索引的集合写入性能可能很差,同时也会降低分片时的数据迁移数据,因为迁移的数据也要重新进行索引

## 优化全文索引

可以结合其他索引来缩小搜索范围,


## 使用GridFS存储文件

性能不如直接从文件系统访问块

如果修改GridFS上的文档,必须将文档先删除,在重新保存

# 聚合


可以使用多个构建创建一个管道,用于对一脸串的文档进行处理:筛选filter,project投射,group分组,sort排序,limit限制,skip跳过.

project中1表示需要投射,0不需要
group {"$group":{"_id":"$author","count":{"$sum":1}}} 按照作者分组,遇到一个就+1
aggregate返回一个文档数组
```js
db.articles.aggregate(
    {"$project":{"author":1}},
    {"$group":{"_id":"$author","count":{"$sum":1}}}},
    {"$sort":{"count":1}},
    {"$limit":5}
    )
```
## 管道

每个操作符都会接受一连串的文档,转换的文档作为结果传递给下一个操作符

$match用于对文档进行筛选

....

## MapReducce 

无法使用聚合框架的查询语句,可以使用mapreduce.它使用JavaScript作为查询语言.但是他非常慢,不应用在实时的数据分析中.

mapreduce可以在多塔服务器之间进行执行,他会将一个大问题拆分为多个小问题,将各个小问题发送到不同的机器上.

# 应用设计

## 优化数据操作

为文档预留足够的增长空间

删除过期文档

# 创建副本集

## 复制

使用复制将副本保存到多台服务器上.主服务器处理客户请求,如果主服务器挂了就选择一个备份服务器作为主服务器

# 副本集的组成

## 同步

mongodb的复制功能使用操作日志oplog实现的,oplog是主节点的local数据库中的一个固定集合,备份节点通过查询这个集合就可以知道需要进行复制的操作


# 分区












