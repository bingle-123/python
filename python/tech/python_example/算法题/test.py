```
比较两个字符串中重叠的最长字符串，找到一个就行
```

# 以长度小的的字符串作为子串s1
# 从s1找到连续的长度为n(循环n=len(s1)-=1)的字符串，比较该字符串是否在s2中,
# 如果在s2中立即返回
def filter(s1, s2):
    l_s1 = len(s1)
    start_len = l_s1
    while start_len > 0:
        next_index = 0
        while l_s1-next_index >= start_len:
            if s1[next_index:start_len+next_index] in s2:
                return s1[next_index:start_len+next_index]
            next_index += 1
        start_len -= 1
    return ''


def compare(s1, s2):
    l_s1 = len(s1)
    l_s2 = len(s2)
    if l_s1 <= l_s2:
        return filter(s1, s2)
    else:
        return filter(s1, s2)


x = 'abcdefdbcdefgdd'
y = 'abbcdefgacdasdfjasd;lf'
print(compare(x, y))
