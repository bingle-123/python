# Redis设计与实现

# 字符串对象sds.h

redis中所有的字符串都是以SDS对象保存,总共有sdshdr5,sdshdr8,sdshdr16,sdshdr32,sdshdr64这5种,sdshdr5没有用

字符串使用C字符串格式,最后一位是'\0'
```c
// 4中len和alloc类型分别为
// uint8_t
// uint16_t
// uint32_t
// uint64_t
{
    uint64_t len; /* 已经使用的长度,不包含'\0' */
    uint64_t alloc; /* 总共大小,不包含头和'\0'*/
    unsigned char flags; /* 前3位表示类型,后5位未使用 */
    char buf[];//字符串最后一位是'\0'
}
```
查看sds字符串直接`printf("%s",s->buf)`

如果要修改sds,那么sds会首先检查空间大小,如果超过实际空间大小,那么会调整空间大小,同时会改变sds的类型flag,

sds申请空间时,会根据字符串长度len预分配一些空间,
`mystring = sdsnewlen("abc",3); ----> sdsnewlen(const void *init, size_t initlen);int hdrlen = sdsHdrSize(type);sh = s_malloc(hdrlen+initlen+1);`

如果某个操作缩短了sds字符串长度,内存是没有进行回收的

## 二进制安全

C字符串中是不能包含`'\0'`的,否则'\0'后面的字符会被忽略.redis以二进制格式保存字符串,当保存字符串时不是以'\0'来判断要保存的字符串结束了,而是根据len参数来决定保存的字节数.所以保存任意格式的二进制数据.

但是每次存储时,都会多申请一个字节用于存放最后一位'\0'

# 链表 adlist.h

```c
//链表节点
typedef struct listNode {
    struct listNode *prev;
    struct listNode *next;
    void *value;
} listNode;

//链表遍历器
typedef struct listIter {
    listNode *next;
    int direction;
} listIter;

typedef struct list {
    listNode *head;//链表头
    listNode *tail;//链表尾
    void *(*dup)(void *ptr);//节点复制函数
    void (*free)(void *ptr);//节点释放函数
    int (*match)(void *ptr, void *key);//节点对比函数
    unsigned long len;//链表长度
} list;
```

# 字典 dict.h

```c

typedef struct dictEntry {
    void *key;//建
    //值
    union {
        void *val;//对象
        uint64_t u64;
        int64_t s64;
        double d;
    } v;
    // 指向下一个hash表节点,形成链表,用于解决冲突
    struct dictEntry *next;
} dictEntry;

typedef struct dictType {
    // 计算hash的函数
    uint64_t (*hashFunction)(const void *key);
    // 复制键的函数
    void *(*keyDup)(void *privdata, const void *key);
    // 复制值的函数
    void *(*valDup)(void *privdata, const void *obj);
    // 对比键的函数
    int (*keyCompare)(void *privdata, const void *key1, const void *key2);
    // 销毁键的函数
    void (*keyDestructor)(void *privdata, void *key);
    // 销毁值得函数
    void (*valDestructor)(void *privdata, void *obj);
} dictType;

/* This is our hash table structure. Every dictionary has two of this as we
 * implement incremental rehashing, for the old to the new table. */
//hash表
typedef struct dictht {
    dictEntry **table;//hash表数组
    unsigned long size;//hash表大小
    unsigned long sizemask;//==size-1
    unsigned long used;//hash已有节点大小
} dictht;

typedef struct dict {
    // 类型
    dictType *type;
    // 私有数据,保存传递给特定函数的可选参数
    void *privdata;
    // hash表
    dictht ht[2];
    long rehashidx; /* rehashing not in progress if rehashidx == -1 */
    unsigned long iterators; /* number of iterators currently running */
} dict;
```
一般情况下字典只是用ht[0],ht[1]只有在对h[0]进行rehash时使用

rehash用于扩大来减少冲突

# 有序集合

# 整数集合

# 对象 server.h

redis使用对象来表示数据库中的键和值,每次都会创键两个对象,一个对象用作键值对的键,一个用于值.  
type: `OBJ_STRING 0 OBJ_LIST 1 OBJ_SET 2 OBJ_ZSET 3 OBJ_HASH 4`  
encoding: 
- OBJ_ENCODING_RAW 0     /* Raw representation */
- OBJ_ENCODING_INT 1     /* Encoded as integer */
- OBJ_ENCODING_HT 2      /* Encoded as hash table */
- OBJ_ENCODING_ZIPMAP 3  /* Encoded as zipmap */
- OBJ_ENCODING_LINKEDLIST 4 /* No longer used: old list encoding. */
- OBJ_ENCODING_ZIPLIST 5 /* Encoded as ziplist */
- OBJ_ENCODING_INTSET 6  /* Encoded as intset */
- OBJ_ENCODING_SKIPLIST 7  /* Encoded as skiplist */
- OBJ_ENCODING_EMBSTR 8  /* Embedded sds string encoding */
- OBJ_ENCODING_QUICKLIST 9 /* Encoded as linked list of ziplists */
```
typedef struct redisObject {
    unsigned type:4;//类型:
    unsigned encoding:4;//保存的值,使用了底层哪一个对象类型
    unsigned lru:LRU_BITS; /* LRU time (relative to global lru_clock) or
                            * LFU data (least significant 8 bits frequency
                            * and most significant 16 bits access time). */
    int refcount;//引用计数
    void *ptr;//指向值
} robj;
```

# 数据库

redis数据库

```
typedef struct redisDb {
    dict *dict;                 /* 保存键值对 The keyspace for this DB */
    dict *expires;              /* 键的过期时间 Timeout of keys with a timeout set */
    dict *blocking_keys;        /* Keys with clients waiting for data (BLPOP)*/
    dict *ready_keys;           /* Blocked keys that received a PUSH */
    dict *watched_keys;         /* WATCHED keys for MULTI/EXEC CAS */
    int id;                     /* Database ID */
    long long avg_ttl;          /* Average TTL, just for stats */
} redisDb;
```

## 键过期

使用惰性删除和定期删除策略

redis服务器周期性的至今cron时就会调用定期删除(activeExpireCycle)

## ADB
每次启动都会载入ADB文件

## AOF

每次启动就会执行呢AOF中的指令

## 数据库通知

客户端订阅数据库中键的变化

