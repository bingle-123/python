 # Python PEP8官方文档规范

内容

- [介绍](https://legacy.python.org/dev/peps/pep-0008/#introduction)
- [愚蠢的一致性是小思想的大人物](https://legacy.python.org/dev/peps/pep-0008/#a-foolish-consistency-is-the-hobgoblin-of-little-minds)
- 代码布局
  - [缩进](https://legacy.python.org/dev/peps/pep-0008/#indentation)
  - [标签或空格？](https://legacy.python.org/dev/peps/pep-0008/#tabs-or-spaces)
  - [最大线路长度](https://legacy.python.org/dev/peps/pep-0008/#maximum-line-length)
  - [应该在二元运算符之前还是之后断行？](https://legacy.python.org/dev/peps/pep-0008/#should-a-line-break-before-or-after-a-binary-operator)
  - [空白行](https://legacy.python.org/dev/peps/pep-0008/#blank-lines)
  - [源文件编码](https://legacy.python.org/dev/peps/pep-0008/#source-file-encoding)
  - [进口](https://legacy.python.org/dev/peps/pep-0008/#imports)
  - [模块级别的dunder名称](https://legacy.python.org/dev/peps/pep-0008/#module-level-dunder-names)
- [字符串引号](https://legacy.python.org/dev/peps/pep-0008/#string-quotes)
- 表达式和语句中的空格
  - [宠物皮皮鬼](https://legacy.python.org/dev/peps/pep-0008/#pet-peeves)
  - [其他建议](https://legacy.python.org/dev/peps/pep-0008/#other-recommendations)
- 注释
  - [阻止评论](https://legacy.python.org/dev/peps/pep-0008/#block-comments)
  - [内联注释](https://legacy.python.org/dev/peps/pep-0008/#inline-comments)
  - [文档字符串](https://legacy.python.org/dev/peps/pep-0008/#documentation-strings)
- 命名约定
  - [压倒一切的原则](https://legacy.python.org/dev/peps/pep-0008/#overriding-principle)
  - [描述性：命名样式](https://legacy.python.org/dev/peps/pep-0008/#descriptive-naming-styles)
  - 规定性：命名约定
    - [要避免的名字](https://legacy.python.org/dev/peps/pep-0008/#names-to-avoid)
    - [包和模块名称](https://legacy.python.org/dev/peps/pep-0008/#package-and-module-names)
    - [类名称](https://legacy.python.org/dev/peps/pep-0008/#class-names)
    - [例外名称](https://legacy.python.org/dev/peps/pep-0008/#exception-names)
    - [全局变量名称](https://legacy.python.org/dev/peps/pep-0008/#global-variable-names)
    - [功能名称](https://legacy.python.org/dev/peps/pep-0008/#function-names)
    - [函数和方法参数](https://legacy.python.org/dev/peps/pep-0008/#function-and-method-arguments)
    - [方法名称和实例变量](https://legacy.python.org/dev/peps/pep-0008/#method-names-and-instance-variables)
    - [常量](https://legacy.python.org/dev/peps/pep-0008/#constants)
    - [设计继承](https://legacy.python.org/dev/peps/pep-0008/#designing-for-inheritance)
  - [公共和内部接口](https://legacy.python.org/dev/peps/pep-0008/#public-and-internal-interfaces)
- 编程建议
  - [功能注释](https://legacy.python.org/dev/peps/pep-0008/#function-annotations)
- [参考](https://legacy.python.org/dev/peps/pep-0008/#references)
- [版权](https://legacy.python.org/dev/peps/pep-0008/#copyright)

# [介绍](https://legacy.python.org/dev/peps/pep-0008/#id14)

本文档给出了Python代码组成的编码约定，其中包含主要Python发行版中的标准库。请参阅在Python的C实现中为C代码描述样式准则的配套信息PEP [[1\]](https://legacy.python.org/dev/peps/pep-0008/#id8)。

本文档和[PEP 257](https://legacy.python.org/dev/peps/pep-0257)（Docstring公约）改编自Guido最初的Python风格指南文章，并增加了一些Barry风格指南[[2\]](https://legacy.python.org/dev/peps/pep-0008/#id9)。

随着时间的推移，这种风格指南会随着其他惯例的确定而变化，过去的惯例会因语言本身的变化而过时。

许多项目都有自己的编码风格指南。在发生任何冲突时，此类项目特定的指南优先于该项目。

# [愚蠢的一致性是小思想的大人物](https://legacy.python.org/dev/peps/pep-0008/#id15)

Guido的一个关键见解是，代码的读取频率远高于编写代码。此处提供的准则旨在提高代码的可读性，并使其在各种Python代码中保持一致。正如[PEP 20](https://legacy.python.org/dev/peps/pep-0020)所说，“可读性计数”。

风格指南是关于一致性的。与此风格指南的一致性非常重要。项目中的一致性更重要。一个模块或功能内的一致性是最重要的。

但是，知道什么时候不一致 - 有时风格指导建议不适用。如有疑问，请使用您的最佳判断。看看其他例子，并决定什么看起来最好。不要犹豫，问！

特别是：不要为了符合这个PEP而打破向后兼容性！

忽略特定指南的其他一些好理由：

1. 在应用指南时，即使对于习惯阅读遵循此PEP的代码的人来说，代码的可读性也会降低。
2. 为了与周围的代码保持一致（也许是出于历史原因） - 尽管这也是一个清理别人乱七八糟（真正的XP风格）的机会。
3. 因为有关代码早于引入准则，所以没有其他理由要修改该代码。
4. 当代码需要与旧版本的Python不兼容时，该版本不支持样式指南推荐的功能。

# [代码布局](https://legacy.python.org/dev/peps/pep-0008/#id16)

## [缩进](https://legacy.python.org/dev/peps/pep-0008/#id17)

每个缩进级别使用4个空格。

连续行应使用Python的隐式行连接括号，括号和大括号，或使用*悬挂缩进* 来垂直对齐包装元素[[7\]](https://legacy.python.org/dev/peps/pep-0008/#fn-hi)。在使用悬挂式缩进时，应考虑以下内容：第一行应该没有任何争论，应该使用进一步的缩进来将自己明确地区分为延续线。

是：

```
＃与开头分隔符对齐。
foo = long_function_name（var_one，var_two，
                         var_three，var_four）

＃包含更多缩进区别于其他缩进。
def long_function_name（
        var_one，var_two，var_three，
        var_four）：
    打印（var_one）

＃悬挂缩进应该添加一个级别。
foo = long_function_name（
    var_one，var_two，
    var_three，var_four）

```

没有：

```
＃不使用垂直对齐时禁止第一行的参数。
foo = long_function_name（var_one，var_two，
    var_three，var_four）

＃由于缩进无法区分，因此需要进一步缩进。
def long_function_name（
    var_one，var_two，var_three，
    var_four）：
    打印（var_one）

```

四维空间规则对于延续线是可选的。

可选的：

```
＃悬挂缩进*可以缩进至4个以内。
foo = long_function_name（
  var_one，var_two，
  var_three，var_four）

```

当`if`语句的条件部分足够长以至于需要将其写入多行时，值得注意的是，两个字符关键字（即`if`）的组合，再加上一个空格以及一个左括号会创建一个自然的多行有条件的后续行使用4空格缩进。这可能会与嵌套在`if`语句中的缩进代码套件产生视觉冲突，该套件自然会缩进到4个空格。该PEP没有明确地说明如何（或是否）进一步在视觉上将这些条件线与`if-` statement 内的嵌套套件区分开来。在这种情况下可接受的选择包括但不限于：

```
＃没有额外的缩进。
if（this_is_one_thing和
    that_is_another_thing）：
    做一点事（）

＃添加评论，这将在编辑器中提供一些区别
＃支持语法高亮显示。
if（this_is_one_thing和
    that_is_another_thing）：
    ＃既然这两个条件都是真的，我们可以生气。
    做一点事（）

＃在条件延续线上添加一些额外的缩进。
if（this_is_one_thing
        和that_is_another_thing）：
    做一点事（）

```

（另请参阅下面关于是否在二元运算符之前或之后中断的讨论。）

多行构造上的右括号/括号/括号可以在列表的最后一行的第一个非空白字符下排列，如下所示：

```
my_list = [
    1，2，3，
    4，5，6，
    ]
result = some_function_that_takes_arguments（
    'a'，'b'，'c'，
    'd'，'e'，'f'，
    ）

```

或者可能会在启动多行构建的行的第一个字符下排列，如下所示：

```
my_list = [
    1，2，3，
    4，5，6，
]
result = some_function_that_takes_arguments（
    'a'，'b'，'c'，
    'd'，'e'，'f'，
）

```

## [标签或空格？](https://legacy.python.org/dev/peps/pep-0008/#id18)

空格是首选的缩进方法。

选项卡应仅用于与已使用选项卡缩进的代码保持一致。

Python 3不允许混合使用制表符和空格来缩进。

Python 2代码缩进的制表符和空格混合应该转换为仅使用空格。

当使用`-t`选项调用Python 2命令行解释器时，它会发出有关非法混合选项卡和空格的代码的警告。使用`-tt时，`这些警告会出错。这些选项是强烈建议！

## [最大线路长度](https://legacy.python.org/dev/peps/pep-0008/#id19)

将所有行限制为最多79个字符。

对于具有较少结构限制（文档字符串或注释）的长文本块，行长度应限制为72个字符。

限制所需的编辑器窗口宽度可以使多个文件并排打开，并且在使用在相邻列中显示两个版本的代码审阅工具时可以很好地工作。

大多数工具的默认包装破坏了代码的可视化结构，使其更难以理解。选择限制是为了避免在窗口宽度设置为80的编辑器中进行包装，即使该工具在换行时在最后一列中放置了标记符号。一些基于Web的工具可能根本不提供动态换行。

有些团队强烈希望更长的线条长度。对于专门或主要由可以就此问题达成一致的团队维护的代码，可以将名义行长度从80个字符增加到100个字符（有效地将最大长度增加到99个字符），条件是仍然包含注释和文档字符串72个字符。

Python标准库是保守的，需要将行限制为79个字符（并且文档字符串/注释为72）。

包装长行的首选方式是在括号，括号和大括号内使用Python的隐含行连续。通过在括号中包装表达式，可以在多行上分割长行。这些应该优先使用反斜杠来继续行。

有时反斜杠可能仍然适用。例如，long，multiple `with` -statements不能使用隐式延续，因此可以接受反斜杠：

```
打开（'/ path / to / some / file / you / want / to / read'）作为file_1，\
     打开（'/ path / to / some / file / being / written'，'w'）作为file_2：
    file_2.write（file_1.read（））

```

（参见前面关于[多行if语句的](https://legacy.python.org/dev/peps/pep-0008/#multiline-if-statements)讨论，以进一步思考这种`带有` -statements的多行缩进。）

另一个这样的情况是`assert`语句。

确保适当缩进续行。

## [应该在二元运算符之前还是之后断行？](https://legacy.python.org/dev/peps/pep-0008/#id20)

几十年来，推荐的风格是在二元运算符之后打破。但是这会以两种方式伤害可读性：操作员倾向于分散在屏幕上的不同列上，并且每个操作员都从操作数移动到前一行。在这里，眼睛必须做额外的工作来判断哪些项目被添加以及哪些被减去：

```
#No：运营商远离他们的操作数
收入=（gross_wages +
          taxable_interest +
          （股息 -  qualified_dividends） - 
          ira_deduction  - 
          student_loan_interest）

```

为了解决这个可读性问题，数学家和他们的出版商遵循相反的惯例。Donald Knuth在他的“ *计算机与排版”*系列中解释了传统规则：“尽管二进制操作和关系之后段落中的公式总是中断，但显示的公式总是在二进制操作之前中断” [[3\]](https://legacy.python.org/dev/peps/pep-0008/#id10)。

遵循数学传统通常会产生更易读的代码：

```
＃是：容易使操作符与操作数匹配
收入=（gross_wages
          + taxable_interest
          +（股息 -  qualified_dividends）
          -  ira_deduction
          -  student_loan_interest）

```

在Python代码中，只要约定在本地一致，就可以在二元运算符之前或之后中断。建议使用新代码Knuth的风格。

## [空白行](https://legacy.python.org/dev/peps/pep-0008/#id21)

用两个空白行围绕顶层函数和类定义。

一个类中的方法定义被一个空行包围。

可以使用额外的空白行（节省空间）来分隔相关功能组。在一堆相关的单行程序（例如一组虚拟执行程序）之间可能会省略空白行。

在函数中使用空行，谨慎地指示逻辑部分。

Python接受控件-L（即^ L）换页字符作为空格; 许多工具将这些字符视为页面分隔符，因此您可以使用它们来分隔文件相关部分的页面。请注意，有些编辑器和基于Web的代码查看器可能无法将控件-L识别为换页符，并会在其位置显示另一个字形。

## [源文件编码](https://legacy.python.org/dev/peps/pep-0008/#id22)

核心Python发行版中的代码应始终使用UTF-8（或Python 2中的ASCII）。

使用ASCII（在Python 2中）或UTF-8（在Python 3中）的文件不应该有编码声明。

在标准库中，非默认编码应仅用于测试目的，或者当注释或文档字符串需要提及包含非ASCII字符的作者名称时; 否则，使用`\ x`， `\ u`，`\ U`或`\ N`转义是在字符串文字中包含非ASCII数据的首选方法。

对于Python 3.0及更高版本，标准库规定了以下策略（参见[PEP 3131](https://legacy.python.org/dev/peps/pep-3131)）：Python标准库中的所有标识符必须使用仅ASCII标识符，并且应尽可能使用英语单词（在许多情况下，缩写和技术）使用的术语不是英语）。另外，字符串文字和注释也必须使用ASCII。唯一的例外是（a）测试非ASCII功能的测试用例，以及（b）作者姓名。名字不是基于拉丁字母的作者必须提供他们的名字的拉丁音译。

鼓励全球受众的开源项目采用类似的政策。

## [进口](https://legacy.python.org/dev/peps/pep-0008/#id23)

- 进口通常应该分开，例如：

  ```
  是的：导入操作系统
       进口系统

  No：import sys，os

  ```

  可以这样说：

  ```
  来自子进程导入Popen，PIPE

  ```

- 导入总是放在文件的顶部，就在任何模块注释和文档字符串之后，以及模块全局变量和常量之前。

  应按以下顺序对导入进行分组：

  1. 标准库导入
  2. 相关的第三方进口
  3. 本地应用程序/库特定导入

  您应该在每组导入之间添加一个空行。

- 建议使用绝对导入，因为如果导入系统配置不正确（例如，当包中的目录最终出现在`sys.path上时`），它们通常更具可读性并且往往表现得更好（或至少提供更好的错误消息）：

  ```
  导入mypkg.sibling
  来自mypkg import sibling
  来自mypkg.sibling导入示例

  ```

  但是，明确的相对进口是绝对进口的可接受替代方案，特别是在处理复杂的包装布局时，使用绝对进口时会产生不必要的冗长：

  ```
  从。进口兄弟
  来自.sibling导入示例

  ```

  标准库代码应避免复杂的包布局，并始终使用绝对导入。

  隐进口相对应*永远不会*被使用，并在Python 3已被删除。

- 从包含类的模块中导入一个类时，通常可以这样描述：

  ```
  从myclass导入MyClass
  来自foo.bar.yourclass导入YourClass

  ```

  如果此拼写导致本地名称冲突，则拼写它们

  ```
  导入myclass
  import foo.bar.yourclass

  ```

  并使用“myclass.MyClass”和“foo.bar.yourclass.YourClass”。

- 应该避免使用通配符导入（`来自<module> import *`），因为它们不清楚命名空间中存在哪些名称，使读者和许多自动化工具混淆。通配符导入有一个可防御的用例，即将内部接口重新发布为公共API的一部分（例如，使用可选加速器模块中的定义覆盖接口的纯Python实现，以及确切的定义将是被覆盖的事先不知道）。

  以这种方式重新发布名称时，以下有关公共和内部接口的指南仍然适用。

## [模块级别的dunder名称](https://legacy.python.org/dev/peps/pep-0008/#id24)

模块级“dunders”（即名称具有两个前缘和两个纵下划线）如`__all__`，`__author__`，`__version__`等应被放置在模块文档字符串之后，但在任何导入语句*以外* `从__future__`进口。Python要求future-imports必须在除docstrings之外的任何其他代码之前出现在模块中。

例如：

```
“”这是示例模块。

这个模块做的东西。
“””

来自__future__ import barry_as_FLUFL

__all__ = ['a'，'b'，'c']
__version__ ='0.1'
__author__ ='红衣主教Biggles'

进口操作系统
进口系统

```

# [字符串引号](https://legacy.python.org/dev/peps/pep-0008/#id25)

在Python中，单引号字符串和双引号字符串是相同的。该PEP不会对此提出建议。选择规则并坚持下去。但是，当字符串包含单引号或双引号字符时，请使用另一个字符串以避免字符串中出现反斜杠。它提高了可读性。

对于三引号字符串，始终使用双引号字符与[PEP 257中](https://legacy.python.org/dev/peps/pep-0257)的docstring约定一致。

# [表达式和语句中的空格](https://legacy.python.org/dev/peps/pep-0008/#id26)

## [宠物皮皮鬼](https://legacy.python.org/dev/peps/pep-0008/#id27)

在以下情况下避免无关的空白：

- 紧靠括号，括号或括号内。

  ```
  是的：垃圾邮件（火腿[1]，{蛋：2}）
  不：垃圾邮件（火腿[1]，{蛋：2}）

  ```

- 在逗号，分号或冒号之前：

  ```
  是：如果x == 4：打印x，y; x，y = y，x
  否：如果x == 4：打印x，y; x，y = y，x

  ```

- 然而，在一个切片中，冒号的作用就像一个二元运算符，并且两边应该有相同的数量（将其视为最低优先级的运算符）。在扩展切片中，两个冒号必须具有相同量的间距。例外：当省略切片参数时，空格被省略。

  是：

  ```
  火腿[1：9]，火腿[1：9：3]，火腿[：9：3]，火腿[1 :: 3]，火腿[1：9：]
  火腿[lower：upper]，火腿[lower：upper：]，ham [lower :: step]
  ham [lower + offset：upper + offset]
  ham [：upper_fn（x）：step_fn（x）]，ham [:: step_fn（x）]
  ham [lower + offset：upper + offset]

  ```

  没有：

  ```
  ham [lower + offset：upper + offset]
  火腿[1：9]，火腿[1：9]，火腿[1：9：3]
  火腿[lower :: upper]
  火腿[：上]

  ```

- 紧接在开始函数调用参数列表的开括号之前：

  ```
  是的：垃圾邮件（1）
  否：垃圾邮件（1）

  ```

- 紧接在开始索引或切片的左括号之前：

  ```
  是的：dct ['key'] = lst [index]
  否：dct ['key'] = lst [index]

  ```

- 赋值（或其他）运算符周围有多个空格，以使其与另一个运算符对齐。

  是：

  ```
  x = 1
  y = 2
  long_variable = 3

  ```

  没有：

  ```
  x = 1
  y = 2
  long_variable = 3

  ```

## [其他建议](https://legacy.python.org/dev/peps/pep-0008/#id28)

- 避免在任何地方尾随空格。因为它通常是不可见的，所以它可能会令人困惑：例如，反斜杠后跟空格和换行符不算作行继续标记。有些编辑器不保留它，许多项目（如CPython本身）都有预先提交的拒绝它的钩子。

- 始终围绕这些二元运算符，两边都有一个空格：赋值（`=`），扩充赋值（`+ =`，`- =` 等），比较（`==`，`<`，`>`，`！=`，`<>`，`<=`， `> =`，`in`，`not in`，`is`，`not not`），布尔（`和`， `或者`，`不是`）。

- 如果使用具有不同优先级的运算符，请考虑在具有最低优先级的运算符周围添加空格。用你自己的判断; 但是，永远不要使用多个空格，并且在二元运算符的两边始终具有相同数量的空白。

  是：

  ```
  我=我+ 1
  提交+ = 1
  x = x * 2  -  1
  hypot2 = x * x + y * y
  c =（a + b）*（ab）

  ```

  没有：

  ```
  I = I + 1
  提交+ = 1
  x = x * 2  -  1
  hypot2 = x * x + y * y
  c =（a + b）*（a  -  b）

  ```

- 当用于指示关键字参数或默认参数值时，请勿在`=`符号周围使用空格。

  是：

  ```
  def complex（real，imag = 0.0）：
      返回魔法（r =真实，i =成像）

  ```

  没有：

  ```
  def complex（real，imag = 0.0）：
      返回魔法（r =真实，i =成像）

  ```

- 功能说明应使用冒号的一般规则，总是有周围的空间`- >`箭头（如果存在）。（有关[功能注释](https://legacy.python.org/dev/peps/pep-0008/#function-annotations)的更多信息，请参见 下面的函数注释。）

  是：

  ```
  def munge（输入：AnyStr）：...
  def munge（） - > AnyStr：...

  ```

  没有：

  ```
  def munge（输入：AnyStr）：...
  def munge（） - > PosInt：...

  ```

- 将参数注释与默认值组合时，请在`=`符号周围使用空格（但仅适用于同时具有注释和默认值的参数）。

  是：

  ```
  def munge（sep：AnyStr = None）：...
  def munge（输入：AnyStr，sep：AnyStr = None，limit = 1000）：...

  ```

  没有：

  ```
  def munge（输入：AnyStr =无）：...
  def munge（输入：AnyStr，limit = 1000）：...

  ```

- 通常不鼓励使用复合语句（同一行上的多个语句）。

  是：

  ```
  如果foo =='blah'：
      do_blah_thing（）
  do_one（）
  do_two（）
  do_three（）

  ```

  而不是：

  ```
  如果foo =='blah'：do_blah_thing（）
  do_one（）; do_two（）; do_three（）

  ```

- 虽然有时可以将if / for / while与小体放在同一行上，但是不要对多子句语句执行此操作。还要避免折叠如此长的线条！

  而不是：

  ```
  如果foo =='blah'：do_blah_thing（）
  for l in lst：total + = x
  而t <10：t =延迟（）

  ```

  当然不：

  ```
  如果foo =='blah'：do_blah_thing（）
  else：do_non_blah_thing（）

  尝试：某事（）
  终于：清理（）

  do_one（）; do_two（）; do_three（长，争论，
                               列表，像，这个）

  if foo =='blah'：one（）; 二（）; 三（）

  ```

# [注释](https://legacy.python.org/dev/peps/pep-0008/#id29)

与代码相矛盾的评论比没有评论更糟糕。始终优先考虑在代码更改时保持评论的最新状态！

评论应该是完整的句子。如果评论是短语或句子，则其第一个单词应该大写，除非它是以小写字母开头的标识符（永远不会改变标识符的情况！）。

如果评论很短，则可以省略最后的句点。块注释通常由完整句子构成的一个或多个段落组成，每个句子应以句点结束。

在句子结束期后你应该使用两个空格。

在写英文时，请遵循Strunk和White。

来自非英语国家的Python编码人员：请用英文写下您的意见，除非您确信代码不会被不会说您的语言的人阅读。

## [阻止评论](https://legacy.python.org/dev/peps/pep-0008/#id30)

块注释通常适用于跟随它们的一些（或所有）代码，并且缩进到与该代码相同的级别。块注释的每一行都以`＃`和单个空格开头（除非它在注释内缩进文本）。

块注释中的段落由包含单个`＃`的行分隔。

## [内联注释](https://legacy.python.org/dev/peps/pep-0008/#id31)

谨慎使用内嵌评论。

内联评论是对语句同一行的评论。内联注释应该与语句中的至少两个空格分隔。他们应该以＃和单个空间开始。

内联评论是不必要的，事实上，如果他们陈述明显的话，就会分心。不要这样做：

```
x = x + 1＃增量x

```

但有时，这很有用：

```
x = x + 1＃补偿边界

```

## [文档字符串](https://legacy.python.org/dev/peps/pep-0008/#id32)

编写良好文档字符串（又称“文档字符串”）的惯例在[PEP 257](https://legacy.python.org/dev/peps/pep-0257)中不朽。

- 为所有公共模块，函数，类和方法编写文档。Docstrings对于非公开方法不是必需的，但您应该有一个评论来描述该方法的功能。此评论应出现在`def`行之后。

- [PEP 257](https://legacy.python.org/dev/peps/pep-0257)描述了良好的文档字符串约定。请注意，最重要的是，结束多行文档字符串的`“”“`应该单独在一行上，例如：

  ```
  “”返回一个foobang

  可选的plotz说要首先对bizbaz进行欺骗。
  “””

  ```

- 对于一个班轮文件，请将结尾`“”“`保留在同一行。

# [命名约定](https://legacy.python.org/dev/peps/pep-0008/#id33)

Python库的命名约定有点乱，所以我们永远不会得到完全一致的结果 - 不过，这里是目前推荐的命名标准。应该为这些标准编写新的模块和包（包括第三方框架），但是现有库具有不同风格时，内部一致性是首选。

## [压倒一切的原则](https://legacy.python.org/dev/peps/pep-0008/#id34)

作为API的公共部分对用户可见的名称应遵循反映使用情况而非实现情况的约定。

## [描述性：命名样式](https://legacy.python.org/dev/peps/pep-0008/#id35)

有很多不同的命名风格。它有助于识别正在使用的命名样式，与它们的用途无关。

以下命名风格通常是可区分的：

- `b`（单个小写字母）

- `B`（单个大写字母）

- `小写`

- `lower_case_with_underscores`

- `大写`

- `UPPER_CASE_WITH_UNDERSCORES`

- `CapitalizedWords`（或CapWords，或者驼峰-如此，因为它信件的颠簸外观而得名[[4\] ](https://legacy.python.org/dev/peps/pep-0008/#id11)）。这有时也被称为StudlyCaps。

  注意：在CapWords中使用缩写时，请将缩写的所有字母大写。因此HTTPServerError优于HttpServerError。

- `mixedCase`（与大写字母不同，由小写字母开始！）

- `Capitalized_Words_With_Underscores`（丑陋！）

还有使用简短唯一前缀将相关名称组合在一起的风格。这在Python中并不常用，但为了完整性而提到它。例如，`os.stat（）`函数返回一个元组，其`元素`传统上具有`st_mode`， `st_size`，`st_mtime`等名称。（这样做是为了强调与POSIX系统调用struct的字段的对应关系，这有助于程序员熟悉它。）

X11库使用前导X来表示其所有公共功能。在Python中，这种样式通常被认为是不必要的，因为属性和方法名称以对象为前缀，函数名称以模块名称为前缀。

此外，还会识别使用前导或尾随下划线的以下特殊形式（这些形式通常可与任何案例约定结合使用）：

- `_single_leading_underscore`：弱“内部使用”指标。例如，`来自M import *`不会导入名称以下划线开头的对象。

- `single_trailing_underscore_`：由约定用于避免与Python关键字冲突，例如

  ```
  Tkinter.Toplevel（master，class _ ='ClassName'）

  ```

- `__double_leading_underscore`：在命名一个class属性时，调用name mangling（在类FooBar中，`__ boo`变成 `_FooBar__boo` ;见下文）。

- `__double_leading_and_trailing_underscore__`：生成在用户控制的命名空间中的“魔术”对象或属性。例如`__init __`，`__ ``import__`或`__file__`。不要发明这样的名字; 仅按记录使用它们。

## [规定性：命名约定](https://legacy.python.org/dev/peps/pep-0008/#id36)

### [要避免的名字](https://legacy.python.org/dev/peps/pep-0008/#id37)

切勿将字符'l'（小写字母el），'O'（大写字母哦）或'I'（大写字母眼睛）用作单个字符变量名称。

在某些字体中，这些字符与数字1和0无法区分。当试图使用'l'时，请使用'L'。

### [包和模块名称](https://legacy.python.org/dev/peps/pep-0008/#id38)

模块应该有简短的全小写名称。如果提高可读性，可以在模块名称中使用下划线。Python包也应该有简短的全小写名称，但不鼓励使用下划线。

当用C或C ++编写的扩展模块具有提供更高级别（例如更多面向对象）的接口的Python模块时，C / C ++模块具有前导下划线（例如`_socket`）。

### [类名称](https://legacy.python.org/dev/peps/pep-0008/#id39)

类名通常应使用CapWords约定。

在接口被记录并主要用作可调用的情况下，可以使用函数的命名约定。

请注意，内置名称有一个单独的约定：大多数内置名称是单个单词（或两个单词一起运行），CapWords约定仅用于异常名称和内置常量。

### [例外名称](https://legacy.python.org/dev/peps/pep-0008/#id40)

因为异常应该是类，所以类命名约定在这里适用。但是，您应该在异常名称上使用后缀“错误”（如果异常实际上是错误）。

### [全局变量名称](https://legacy.python.org/dev/peps/pep-0008/#id41)

（我们希望这些变量只能在一个模块中使用）。约定与函数约定相同。

设计为通过`M import *`使用的模块应该使用`__all__`机制来防止输出全局变量，或者使用旧的约定为这些全局变量添加下划线（您可能希望这样做以表明这些全局变量是“模块非公开的” “）。

### [功能名称](https://legacy.python.org/dev/peps/pep-0008/#id42)

函数名称应该是小写字母，必要时用下划线分隔单词以提高可读性。

只有在已经是主流风格（例如threading.py）的上下文中才允许使用mixedCase，以保持向后兼容性。

### [函数和方法参数](https://legacy.python.org/dev/peps/pep-0008/#id43)

始终使用`self`作为实例方法的第一个参数。

总是使用`cls`作为类方法的第一个参数。

如果函数参数的名称与保留关键字冲突，通常最好追加一个尾部下划线而不是使用缩写或拼写损坏。因此，`class_`比`clss好`。（也许更好的是通过使用同义词来避免这种冲突。）

### [方法名称和实例变量](https://legacy.python.org/dev/peps/pep-0008/#id44)

使用函数命名规则：小写，必要时用下划线分隔，以提高可读性。

仅对非公开方法和实例变量使用一个前导下划线。

为避免名称与子类发生冲突，请使用两个前导下划线来调用Python的名称修改规则。

Python将这些名称与类名称相`冲突`：如果类Foo具有名为`__a`的属性，则`Foo .__ a`将无法访问该属性。（坚持不懈的用户仍然可以通过调用`Foo._Foo__a`获得访问权限。）通常，双重前导下划线应该仅用于避免与设计为子类的类中的属性发生名称冲突。

注意：关于__names的使用存在一些争议（见下文）。

### [常量](https://legacy.python.org/dev/peps/pep-0008/#id45)

常量通常在模块级定义，并用大写字母和下划线分隔单词。例子包括 `MAX_OVERFLOW`和`TOTAL`。

### [设计继承](https://legacy.python.org/dev/peps/pep-0008/#id46)

总是要决定一个类的方法和实例变量（统称为“属性”）是公开的还是非公开的。如有疑问，请选择非公开; 将公开属性设置为非公开更容易。

公共属性是指您希望类的无关客户端使用的属性，您承诺避免向后不兼容的更改。非公开属性是那些不打算供第三方使用的属性; 您不保证非公开属性不会更改，甚至不会被删除。

这里我们不使用术语“private”，因为在Python中没有任何属性是真正的私有的（没有通常不必要的工作量）。

另一类属性是属于“子类API”（通常在其他语言中称为“受保护”）的属性。有些类被设计为从类继承，扩展或修改类的行为方面。在设计这样的类时，请注意明确决定哪些属性是公共的，哪些是子类API的一部分，哪些属性真正只能由基类使用。

考虑到这一点，这是Pythonic指南：

- 公共属性应该没有前导下划线。

- 如果公共属性名称与保留关键字冲突，请在属性名称后附加单个尾随下划线。这比缩写或损坏的拼写更可取。（但是，尽管有这个规则，'cls'是任何已知为类的变量或参数的首选拼写，尤其是类方法的第一个参数。）

  注1：有关类方法，请参阅上面的参数名称建议。

- 对于简单的公共数据属性，最好只公开属性名称，而不使用复杂的访问器/ mutator方法。请记住，如果您发现简单的数据属性需要增加功能行为，Python提供了一条简单的未来增强路径。在这种情况下，使用属性隐藏简单数据属性访问语法背后的功能实现。

  注1：属性仅适用于新式类。

  注2：尝试保持功能行为的副作用免费，尽管缓存等副作用通常很好。

  注3：避免使用属性进行计算量大的操作; 该属性符号使得调用者相信访问是（相对）便宜的。

- 如果你的类想要被子类化，并且你有不想使用子类的属性，可以考虑用双引号强调下划线并且不用尾随下划线。这将调用Python的名称修改算法，其中该类的名称被修改为属性名称。这有助于避免属性名称冲突，如果子类无意中包含具有相同名称的属性。

  注意1：请注意，只有简单的类名称用在mangled名称中，所以如果子类同时选择相同的类名称和属性名称，仍然可以获得名称冲突。

  注意2：名称修改可以使某些用途，例如调试和 `__getattr __（）`，不太方便。但是，名称修改算法已有详细记录，并且易于手动执行。

  注3：不是每个人都喜欢名字混搭。尽量平衡避免意外姓名冲突与高级呼叫者潜在使用的需要。

## [公共和内部接口](https://legacy.python.org/dev/peps/pep-0008/#id47)

任何向后兼容性保证仅适用于公共接口。因此，用户必须能够清楚地区分公共和内部接口。

文档化的接口被认为是公共的，除非文档明确声明它们是临时的或内部接口免于通常的向后兼容性保证。应假定所有未记录的接口都是内部接口。

为了更好地支持自省，模块应该使用`__all__`属性在其公共API中显式声明名称。将`__all__`设置 为空列表表示该模块没有公共API。

即使正确设置`__all__`，内部接口（包，模块，类，函数，属性或其他名称）仍应以前导下划线作为前缀。

如果任何包含名称空间（包，模块或类）的内容被视为内部接口，则该接口也被视为内部接口。

应始终将导入的名称视为实现细节。其他模块不能依赖间接访问这些导入的名称，除非它们是包含模块的API的明确记录的部分，例如`os.path`或从子模块公开功能的包的`__init__`模块。

# [编程建议](https://legacy.python.org/dev/peps/pep-0008/#id48)

- 代码的编写方式不会影响Python的其他实现（PyPy，Jython，IronPython，Cython，Psyco等）。

  例如，不要依赖CPython有效地实现以`a + = b` 或`a = a + b`形式`的`语句的就地字符串连接。即使在CPython中，这种优化也很脆弱（它只适用于某些类型），并且在不使用refcounting的实现中完全不存在。在库的性能敏感部分，应该使用`''.join（）`表单来代替。这将确保串联在各种实现中以线性时间发生。

- 像None这样的单例的比较应该总是使用 `is`或者`不是`，而不是相等的运算符。

  另外，`如果x的`意思`是x不是None`，那么要小心写`x`。例如，当测试一个变量或默认为None的参数是否设置为其他值时。另一个值可能有一个类型（如容器），在布尔上下文中可能为false！

- 使用`不是`操作员而`不是...是`。虽然两个表达式在功能上是相同的，但前者更具可读性和首选性。

  是：

  ```
  如果foo不是无：

  ```

  没有：

  ```
  如果不是foo是None：

  ```

- 当具有丰富实施比较排序操作，最好是实现所有六个操作（`__eq__`，`__ne__`， `__lt__`，`__le__`，`__gt__`，`__ge__`）而不是依靠其他代码，只行使特定的比较。

  为了最大限度地减少所涉及的工作量，`functools.total_ordering（）` 装饰器提供了一个生成缺失比较方法的工具。

  [PEP 207](https://legacy.python.org/dev/peps/pep-0207)指出Python 反射规则*是*由Python承担的。因此，解释器可以用`x <y`，`y> = x` 与`x <= y`交换`y> x`，并且可以交换`x == y`和`x！= y的参数`。的`排序（）`和`MIN（）`操作可保证使用`<`运算符和`MAX（）`函数使用`>` 运算符。但是，最好是执行所有六项操作，以免在其他情况下出现混淆。````````````````````

- 总是使用def语句而不是将lambda表达式直接绑定到标识符的赋值语句。

  是：

  ```
  def f（x）：返回2 * x

  ```

  没有：

  ```
  f = lambda x：2 * x

  ```

  第一种形式意味着生成的函数对象的名称特别是'f'而不是泛型'<lambda>'。这对于一般的回溯和字符串表示更有用。使用赋值语句消除了lambda表达式可以在显式def语句上提供的唯一好处（即它可以嵌入到更大的表达式中）

- 从`Exception`而不是`BaseException`派生异常。`BaseException的`直接继承保留用于捕获它们的异常几乎总是错误的事情。

  基于可能需要*捕获*异常的代码的区别来设计异常层次结构 ，而不是引发异常的位置。旨在回答“出了什么问题？”的问题。以编程方式，而不是仅仅声明“发生了一个问题”（请参阅[PEP 3151](https://legacy.python.org/dev/peps/pep-3151)，了解本课程的示例是为内置异常层次结构学习的）

  类命名约定适用于此处，但如果异常是错误，则应将后缀“Error”添加到异常类中。用于非本地流控制或其他形式的信令的非错误异常不需要特殊后缀。

- 适当地使用异常链接。在Python 3中，“从Y提升X”应该用于指示显式替换而不会丢失原始回溯。

  故意替换内部异常（在Python 2中使用“raise X”或在Python 3.3+中“从无提升X”），确保将相关细节传递给新异常（例如在将KeyError转换为AttributeError时保留属性名称） ，或将原始异常的文本嵌入新的异常消息中）。

- 当在Python 2中引发异常时，使用`raise ValueError（'message'）` 而不是旧的形式`引发ValueError，'message'`。

  后一种形式不是合法的Python 3语法。

  paren-using表单也意味着当异常参数很长或者包含字符串格式时，由于包含圆括号，您不需要使用行连续字符。

- 捕获异常时，请尽可能提及特定异常，而不是使用bare `except`子句。

  例如，使用：

  ```
  尝试：
      import platform_specific_module
  除了ImportError：
      platform_specific_module =无

  ```

  一个裸的`except：`子句将捕获SystemExit和KeyboardInterrupt异常，这使得用Control-C中断程序变得更加困难，并且可以掩盖其他问题。如果要捕获发出程序错误信号的所有异常，请使用 `除Exception :(`裸除了`除了BaseException之外`）。

  一个好的经验法则是将裸“除”子句的使用限制为两种情况：

  1. 如果异常处理程序将打印出来或记录回溯; 至少用户会意识到发生了错误。
  2. 如果代码需要做一些清理工作，但随后让异常向上传播并`加注`。 `尝试...终于` 可以更好地处理这种情况。

- 绑定捕获的名称异常时，更喜欢Python 2.6中添加的显式名称绑定语法：

  ```
  尝试：
      处理数据（）
  除了作为exc的例外：
      引发DataProcessingFailedError（str（exc））

  ```

  这是Python 3中唯一支持的语法，可以避免与旧的基于逗号的语法相关的歧义问题。

- 捕获操作系统错误时，更喜欢Python 3.3中引入的显式异常层次结构，而不是内省`errno` 值。

- 此外，对于所有try / except子句，将`try`子句限制为所需的绝对最小代码量。同样，这可以避免掩盖错误。

  是：

  ```
  尝试：
      value =集合[关键]
  除KeyError外：
      return key_not_found（key）
  其他：
      return handle_value（value）

  ```

  没有：

  ```
  尝试：
      ＃ 太宽泛！
      return handle_value（collection [key]）
  除KeyError外：
      ＃还会捕获handle_value（）引发的KeyError
      return key_not_found（key）

  ```

- 当资源是特定代码段的本地资源时，请使用 `with`语句以确保在使用后立即可靠地清除它。try / finally语句也是可以接受的。

- 上下文管理器应该通过独立的函数或方法来调用，只要它们不是获取和释放资源而是执行其他操作。例如：

  是：

  ```
  与conn.begin_transaction（）：
      do_stuff_in_transaction（康涅狄格州）

  ```

  没有：

  ```
  与conn：
      do_stuff_in_transaction（康涅狄格州）

  ```

  后一个例子没有提供任何信息来表明`__enter__`和`__exit__`方法除了在事务之后关闭连接之外正在做其他事情。在这种情况下，明确是很重要的。

- 在回报陈述中保持一致。函数中的所有返回语句都应该返回一个表达式，或者它们都不应该。如果任何return语句返回一个表达式，那么没有返回值的任何返回语句都应该明确声明这是`返回None`，并且函数末尾应该有一个显式的return语句（如果可以的话）。

  是：

  ```
  def foo（x）：
      如果x> = 0：
          return math.sqrt（x）
      其他：
          返回无

  def bar（x）：
      如果x <0：
          返回无
      return math.sqrt（x）

  ```

  没有：

  ```
  def foo（x）：
      如果x> = 0：
          return math.sqrt（x）

  def bar（x）：
      如果x <0：
          返回
      return math.sqrt（x）

  ```

- 使用字符串方法而不是字符串模块。

  字符串方法总是快得多，并与unicode字符串共享相同的API。如果需要向后兼容早于2.0的Pythons，则覆盖此规则。

- 使用`''.startswith（）`和`''.endswith（）`代替字符串切片来检查前缀或后缀。

  startswith（）和endswith（）更清晰，更不容易出错。例如：

  ```
  是的：如果foo.startswith（'bar'）：
  不：如果foo [：3] =='bar'：

  ```

- 对象类型比较应始终使用isinstance（）而不是直接比较类型。

  ```
  是：如果isinstance（obj，int）：

  否：如果type（obj）是type（1）：

  ```

  检查对象是否为字符串时，请记住它也可能是一个unicode字符串！在Python 2中，str和unicode有一个共同的基类，basetring，所以你可以这样做：

  ```
  if isinstance（obj，basestring）：

  ```

  请注意，在Python 3中，`unicode`和`basestring`不再存在（只有`str`），而bytes对象不再是一种字符串（它是一个整数序列）

- 对于序列，（字符串，列表，元组），请使用空序列为假的事实。

  ```
  是的：如果不是seq：
       如果seq：

  否：如果len（seq）：
      如果不是len（seq）：

  ```

- 不要编写依赖于重要尾随空白的字符串文字。这样的尾随空白在视觉上难以区分，一些编辑（或最近的reindent.py）会修剪它们。

- 不要使用`==`将布尔值与True或False进行比较。

  ```
  是的：如果问候：
  否：如果问候==真：
  更糟糕的是：如果问候是真的：

  ```

## [功能注释](https://legacy.python.org/dev/peps/pep-0008/#id49)

随着[PEP 484](https://legacy.python.org/dev/peps/pep-0484)的接受，功能注释的样式规则正在发生变化。

- 为了向前兼容，Python 3代码中的函数注释应该最好使用[PEP 484](https://legacy.python.org/dev/peps/pep-0484)语法。（上一节中有一些注释的格式化建议。）

- 不再鼓励先前在本PEP中推荐的注释样式的实验。

- 但是，在stdlib之外， 现在鼓励[PEP 484](https://legacy.python.org/dev/peps/pep-0484)规则内的实验。例如，使用[PEP 484](https://legacy.python.org/dev/peps/pep-0484)样式类型注释标记大型第三方库或应用程序，查看添加这些注释的容易程度，并观察它们的存在是否增加了代码的可理解性。

- Python标准库在采用这种注释时应该保守，但是它们的使用允许用于新代码和大型重构。

- 对于想要对函数注释进行不同使用的代码，建议对表单进行注释：

  ```
  #type：忽略

  ```

  靠近文件顶部; 这告诉类型检查器忽略所有注释。（在[PEP 484中](https://legacy.python.org/dev/peps/pep-0484)可以找到更细粒度的禁用类型检查器投诉的方法。）

- 像短绒，类型检查器是可选的，单独的工具。默认情况下，Python解释器不应由于类型检查而发出任何消息，并且不应基于注释更改其行为。

- 不想使用类型检查器的用户可以自由地忽略它们。但是，预计第三方库包的用户可能希望在这些包上运行类型检查器。为此， [PEP 484](https://legacy.python.org/dev/peps/pep-0484)建议使用存根文件：.pyi文件由类型检查程序读取，而不是相应的.py文件。存根文件可以与库一起分发，也可以通过类型化仓库[[5\]](https://legacy.python.org/dev/peps/pep-0008/#id12)单独（与库作者的许可）一起分发。

- 对于需要向后兼容的代码，可以以注释的形式添加功能注释。参见[PEP 484 ](https://legacy.python.org/dev/peps/pep-0484)[[6\]](https://legacy.python.org/dev/peps/pep-0008/#id13)的相关章节 。

脚注

【7】挂入缩进是一种类型设置样式，其中段落中的所有行都缩进，除第一行外。在Python的上下文中，该术语用于描述一种样式，其中，带括号的语句的左括号是该行的最后一个非空格字符，随后的行被缩进，直到右括号。