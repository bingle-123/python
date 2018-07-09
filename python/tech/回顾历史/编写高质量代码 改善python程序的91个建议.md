# 编写高质量代码 改善python程序的91个建议

本书从8个方面总结高质量python代码所需要掌握的只是、经验和技巧

- 容易被忽视的重要概念和常识，如代码的布局和编写函数的原则等
- 编写python程序惯用的方法，如利用assert语句去发现问题、使用enumerate()或缺序列迭代的索引和值等
- 语法中的关键条款，如有截止地使用from...import、异常处理的几点基本原则
- 常见库的使用，如按需选择sort()或者sorted()、使用Queue使得多线程编程更安全等
- python设计模式的使用，如发布订阅模式实现松耦合、用状态模式美化代码等
- python的内部机制，如名字查找机制、描述符机制等
- 开发工具的使用，如pip、各种代码测试工具的使用等
- python代码的性能优化分析、优化的原则、工具、技巧，以及常见性能问题的解决等

## 引论

- 1：理解pythonic概念
- 2：编写pythonic代码
- 3：理解python与c语言的不同之处
- 4：在代码中适当的加注释
- 5：通过适当的空行使得代码布局更优雅、合理
- 6：编写函数的4个原则
- 7：将常量集中到一个文件

## 编程惯用法


## 基础语法

## 库

## 设计模式

## 内部机制

## 使用工具辅助项目开发

## 性能剖析与优化

## 1. 理解pythonic概念
- Beautiful is better than ugly.
- Explicit is better than implicit.
- Simple is better than complex.
- Complex is better than complicated.
- Flat is better than nested.
- Sparse is better than dense.
- Readability counts.
- Special cases aren't special enough to break the rules.
- Although practicality beats purity.
- Errors should never pass silently.
- Unless explicitly silenced.
- In the face of ambiguity, refuse the temptation to guess.
- There should be one-- and preferably only one --obvious way to do it.
- Although that way may not be obvious at first unless you're Dutch.
- Now is better than never.
- Although never is often better than *right* now.
- If the implementation is hard to explain, it's a bad idea.
- If the implementation is easy to explain, it may be a good idea.
- Namespaces are one honking great idea -- let's do more of those!

### 代码风格
充分表现python自身特色

```python
# 交换两个变量
a, b = b, a

# 灵活使用迭代器；例如安全的关闭文件
with open(file_name) as f:
    do_sth_with(f)
```
### 标准库
对于字符串格式化通常这样写：`print 'hello %s'%('tom',)`，这里的`%s`非常影响可读性，参数多了之后很难分清每个占位符

`print 'hello %(name)s '%{'name':'tom'}`比较清晰一点

`print '{great} from {language} .'.format(great = 'hello world', language = 'python')`

## 2. 编写pythonic代码

遵循[PEP8](https://my.oschina.net/u/1433482/blog/464444?p=1)

## 3. 理解python与c语言的不同之处

三元操作符：`x if y else z`

## 6. 编写函数的4个原则

1. 函数设计应尽量小
2. 函数名能正确反映其大体功能，参数个数不易太多
3. 参数应该向下兼容
4. 一个函数制作一件事

## 8. 利用assert语句来发现问题
