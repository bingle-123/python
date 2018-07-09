# swift3 官方beta [2016-08-13](https://swift.org/documentation/#the-swift-programming-language)
反馈:`canhuayin@gmail.com`
> 注意:2.0和3.0语法上有很大差别

# 欢迎来到swift世界
## swift快速入门
通常我们学习第一门语言的时候都会来个‘hello world’。在swift中只需
```swift
print("hello world")
```
如果你写过C或者OC的话，会觉得他们看起来很像。在swift中不需要导入额外的库，如input/output或者string处理函数。这行代码就是程序的入口，swift不需要main()函数，（类似于python）也不需要在末尾添加“;”。  
这个教程会通过大量编程实例，来告诉你关于swift编程的知识。如果不明白的话，不要紧，本书的后面会有非常详细的介绍。  
### 简单值
通过`let`定义常量，`var`定义变量。在编译时不需要知道常量的值，但是你必须在定义时就给他赋值。
```swift
var myVariable = 42
myVariable = 50
let myConstant = 42
```
给变量赋值时，值得类型，必须与变量类型一致。然而你并不需要在定义变量是都制定类型，swift会自动判断值的类型，并推导出变量的类型。例如：`myVariable`是整型，因42就是整型。  
如果值不能确定类型的话，你可以定义变量的类型
```swift
let explicitDouble: Double = 70
```
数值不会被自动的转换为其他类型。如果你需要将一个数值转换为其他类型，你需要生成该类型的对象。
```swift
let label = "The width is"
let width = 94
let widthLabel = label + String(width)
```
swift提供了非常简便的方法来将变量包含到字符串中。你只需要使用`\(变量名)`。
```swift
let apples = 3
let oranges = 5
let appleSummary = "I have \\(apples) apples."
let fruitSummary = "I have \\(apples + oranges) pieces of fruit.”
```
使用`[]`来创建列表和字典，通过下标`index`或者键`key`，访问他们的元素。最后一个元素后面允许跟着一个逗号`,`。
```swift
var shoppingList = ["catfish", "water", "tulips", "blue paint"]
shoppingList[1] = "bottle of water"
var occupations = ["Malcolm": "Captain","Kaylee": "Mechanic",]
occupations["Jayne"] = "Public Relations”
```
创建空的列表或者字典，只需要使用初始化语句即可
```swift
let emptyArray = [String]()
let emptyDictionary = [String:Float]()
```
如果不确定类型的话,可以直接使用`[]`创建空列表,`[:]`创建空字典。例如:**你给一个变量赋值或者给一个函数传递参数**。
```swift
shoppingList = []
occupations = [:]
```
### 控制流
使用`if`和`switch`来创造条件,使用`for-in`,`for`,`while`,`repeat-while`,来创建循环。条件两边的`()`是可选的,`{}`是必选的。
```swift
let individualScores = [75, 43, 103, 87, 12]  
var teamScore = 0
for score in individualScores {
    if score > 50 {
        teamScore += 3
    }else {
        teamScore +=1
    }
}
print(teamScore)
```
在`if`语句中,条件必须是Boolean类型,如果使用`if score {}`会报错,swift不会隐式转换数据的类型。  
你可以使用`if`和`let`一起来处理可能没有值的变量。这些值被当做`optional`,optional类型会在后面详解。optional类型要么包含一个值,要么包含`nil`,`nil`表示没有值。在变量类型后面加上`?`将变量变为optional类型。
```swift
var optionalString: String? = "Hello"
print(optionalString == nil)
var optionalName: String? = "John Appleseed"
var greeting = "Hello!"
if let name = optionalName {
    greeting = "Hello, \(name)"
}
```
如果optional值是`nil`,那么`if`语句的条件将会是`false`。否将会取出optional的值并赋给变量。  
另外一种处理optional值的方式是通过`??`给一个默认值,如果optional没有值的话,将会使用默认值。取出optional的值使用`!`
```swift
let nickName: String? = nil
let fullName: String? = "John Appleseed"
let informalGreeting = "HI \(nickName ?? fullName)"
print(informalGreeting) //HI Optional("John Appleseed")
print(fullName)//Optional("John Appleseed")
print(fullName!)//"John Appleseed"
```
**switch** 支持任意类型的数据和以及多种比较方式。
```swift
let vegetable = "red pepper"
switch vegetable {
    case "celery":
        print("Add some raisins and make ants on a log.")
    case "cucumber","watercress":
        print("That would make a good tea sandwich")
    case let x where x.hasSuffix("pepper")
        print("Is it a spicy \(x)?")
    default:
        print("EverEverything tastes good in soup")
}
```
注意`let`可以用来做模式匹配。每一个case匹配之后都会自动break。
**for-in** 可以通过(key,value)循环一个字典中的元素,字典是无序的(类似于python无序字典),所以他的键值对也是任意顺序。他同样可循环访问一个列表的中的元素。
```swift
let interestingNumbers = [
    "Prime":[2, 3, 4, 5, 6, 7],
    "Fibonacci":[1, 1, 2, 3, 5, 8],
    "Square":[1, 4, 9, 16, 25],
]
var largest = 0
for (kind, numbers) in interestingNumbers {
    for number in numbers {
        if number > largest{
            largest = number
        }
    }
    print(kind,largest)
}
//Prime 7
//Fibonacci 8
//Square 25
```
**while** 可以在条件范围内,循环执行代码。条件可以再代码开头定义,也可以在代码结尾定义。
```swift
var n = 2
while n < 10 {
    n = n * 2
    print(n)
}
var m = 2
repeat {
    m = m * 2
    print(m)
}while m < 10
```
可以通过`..<`来构建一个iterator,类似于python的range()。  
- 0..<4 表示不包含0,1,2,3
- 0...4表示包含0,1,2,3,4
```swift
var total = 0
for i in 0..<4 {
    total += i
}
print(total)//6

total = 0
for i in 0...4 {
    total += i
}
print(total)//10
```
### 函数和闭包
`func`定义一个函数,`->`跟着返回值类型
```swift
func greet(person: String, day: String) -> String{
    return "hello \(person), today is \(day)"
}
greet(person: "Bob", day: "Tuesday")
```
默认情况下,函数使用它们参数的名称作为label,在参数名称前添加label,或者使用`_`表示不使用label。
```swift
func greet(_ person: String, on day: String) -> String{
    return "hello \(person), today is \(day)"
}
greet("Bob", on: "Tuesday")
```
将元祖类型作为返回值类型,可以一次返回多个值,元祖可以通过名称或者元素的位置数值访问其中包含的元素。(tuple.itemname,tuple.1)
```swift
func calculateStatistics(scores: [Int]) -> (min: Int, max: Int, sum: Int) {
    var min = scores[0]
    var max = scores[0]
    var sum = 0

    for score in scores {
        if score > max {
            max = score
        } else if score < min {
            min = score
        }
        sum += score
    }

    return (min, max, sum)
}
let statistics = calculateStatistics(scores: [5, 3, 100, 3, 9])
print(statistics.sum)
print(statistics.2)
```
函数还可以不同数量的参数,将他们收进一个列表中
```swift
func sumOf(numbers: Int...) -> Int {
    var sum = 0
    for number in numbers {
        sum += number
    }
    return sum
}
sumOf()
sumOf(numbers: 42, 597, 12)
```
函数还可作为内置函数,他可以访问外部函数的变量。
```swift
func returnFifteen() -> Int {
    var y = 10
    func add() {
        y += 5
    }
    add()
    return y
}
returnFifteen()
```
函数也是一种类型,也就是函数可以返回一个函数类型。
```swift
func makeIncrementer() -> ((Int) -> Int) {
    func addOne(number: Int) -> Int {
        return 1 + number
    }
    return addOne
}
var increment = makeIncrementer()
increment(7)
```
函数可以将其他函数作为参数
```swift
func hasAnyMatches(list: [Int], condition: (Int) -> Bool) -> Bool {
    for item in list {
        if condition(item) {
            return true
        }
    }
    return false
}
func lessThanTen(number: Int) -> Bool {
    return number < 10
}
var numbers = [20, 19, 7, 12]
hasAnyMatches(list: numbers, condition: lessThanTen)
```
函数实际是一种图书的闭包,他可以在定义之后被其他代码调用。可以用`{}`来构建匿名闭包。使用`in`将函数定义域函数体分离
```swift
numbers.map({
    (number: Int) -> Int in
    let result = 3 * number
    return result
})
```
有很多种方法可以定义更加间接地闭包,例如:如果你只到函数类型(参数类型,返回值),那么可以省略掉参数的类型,以及返回类型
```swift
let mappedNumbers = numbers.map({ number in 3 * number })
print(mappedNumbers)
```
你可以通过参数位置而不是参数名字来引用参数——这个方法在非常短的闭包中非常有用,当一个闭包作为最后一个参数传给一个函数的时候,它可以直接跟在括号后面。当一个闭包是传给函数的唯一参数,你可以完全忽略
括号。
### 对象和类
通过`class`定义一个类,类的属性以及函数定义方式与普通变量以及函数定义一样,只不过他们属于类。
```swift
class Shape {
    var numberOfSides = 0
    func simpleDescription() -> String {
        return "A shape with \(numberOfSides) sides."
    }
}
```
创建类的实例以及访问属性和方法
```swift
var shape = Shape()
shape.numberOfSides = 7
var shapeDescription = shape.simpleDescription()
```
类的构造函数为`init`,self代表实例本身,类中的任何一个属性都必须赋值,如果定义时没有给出值,那么在init中必须给其赋值。
```swift
class NamedShape {
    var numberOfSides: Int = 0
    var name: String
    init(name: String) {
        self.name = name
    }
    func simpleDescription() -> String {
        return "A shape with \(numberOfSides) sides."
    }
}
```
如果你需要在对象实例被删除之前做一些操作,那么可以将这些操作写在`deinit`函数中
子类想要重写父类方法,必须使用`override`,没有override会报错。子类调用父类方法通过`super`对象
```swift
class Square: NamedShape {
    var sideLength: Double
    init(sideLength: Double, name: String) {
        self.sideLength = sideLength
        super.init(name: name)
        numberOfSides = 4
}
    func area() ->  Double {
        return sideLength * sideLength
}
    override func simpleDescription() -> String {
        return "A square with sides of length \(sideLength)."
} }
let test = Square(sideLength: 5.2, name: "my test square")
test.area()
test.simpleDescription()
```
类的属性还可以拥有`set`和`get`方法
```swift
class EquilateralTriangle: NamedShape {
    var sideLength: Double = 0.0
    init(sideLength: Double, name: String) {
        self.sideLength = sideLength
        super.init(name: name)
        numberOfSides = 3
    }
    var perimeter: Double {
        get {
            return 3.0 * sideLength
        }
        set {
            sideLength = newValue / 3.0
        }
    }
    override func simpleDescription() -> String {
        return "An equilateral triagle with sides of length \(sideLength)."
    }
}
var triangle = EquilateralTriangle(sideLength: 3.1, name: "a triangle")
print(triangle.perimeter)
```
在`set`中默认的参数名为`newValue`,也可以自定义一个参数名,`set(newVal){}`,不一定一定要有set,如果没有set的话变量是只读的。  
**注意** `EquilateralTriangle`的构造函数执行了三步:
- 设置sideLength
- 调用父类构造函数
- 修改父类numberOfSides的值

变量观察者(有点意思),变量赋值有两个会触发两个函数`willSet`,`didSet`,变量必须是`var`,默认情况下`willSet`接受`newValue`参数,也可以自定义一个名字`willSet(newVal)`,`didSet`接受一个'oldValue'参数,也可以自定义`didSet(oldVal)`,如果变量类型是以引用类型,例如class,那么该实例的属性值变化并不会出发willSet,因为变量的保存的时实例的地址,只要地址不变,就不会触发。(后面会讲到引用类型和数值类型)
```swift
class TriangleAndSquare {
    var triangle: EquilateralTriangle {
        willSet {
            square.sideLength = newValue.sideLength
        }
    }
    var square: Square {
        willSet {
            triangle.sideLength = newValue.sideLength
        }
    }
    init(size: Double, name: String) {
        square = Square(sideLength: size, name: name)
        triangle = EquilateralTriangle(sideLength: size, name: name)
    }
}
var triangleAndSquare = TriangleAndSquare(size: 10, name: "another test shape")
print(triangleAndSquare.square.sideLength)
print(triangleAndSquare.triangle.sideLength)
triangleAndSquare.square = Square(sideLength: 50, name: "larger square")
print(triangleAndSquare.triangle.sideLength)
```
optional类型在变量定义时加`?`,如果变量的值为nil那么`?`之后代码不会运行
```swift
let optionalSquare: Square? = Square(sideLength: 2.5, name: "optional square")
let sideLength = optionalSquare?.sideLength
```
### 枚举和机构体
使用`enum`来创建一个枚举,枚举也可以有自己的函数,也有构造函数,enum类似于一个已知状态的集合,集合中任意一个元素独立
```swift
enum Rank: Int {
    case Ace = 1
    case Two, Three, Four, Five, Six, Seven, Eight, Nine, Ten
    case Jack, Queen, King
    func simpleDescription() -> String {
        switch self {
        case .Ace:
            return "ace"
        case .Jack:
            return "jack"
        case .Queen:
            return "queen"
        case .King:
            return "king"
        default:
            return String(self.rawValue)
        }
    }
}
let ace = Rank.Ace
let aceRawValue = ace.rawValue
```
枚举元素的原始值默认类型是Int,并且从0开始递增。可以通过`.rawValue`获取原始值。上面我们指定Ace=1,那么初始值会从1开始递增。也可以自定义原始值,并且原始值类型可以是字符串或者小数。  
使用`init?(rawValue:)`创建enum实例,
```swift
if let convertedRank = Rank(rawValue: 3) {
    let threeDescription = convertedRank.simpleDescription()
}
```
枚举的元素值是实际的值,并不是另一种书写方式。通常为了不让原始值没有意义,你不需要自己提供原始值。
```swift
enum Suit {
    case Spades, Hearts, Diamonds, Clubs
    func simpleDescription() -> String {
        switch self {
        case .Spades:
            return "spades"
        case .Hearts:
            return "hearts"
        case .Diamonds:
            return "diamonds"
        case .Clubs:
            return "clubs"
        }
    }
}
let hearts = Suit.Hearts
let heartsDescription = hearts.simpleDescription()
```
**注意** 这里我们定义了常量`let hearts = Suit.Hearts`,他必须通过`Suit.Hearts`。然而在枚举内部的switch中,我们并没有使用`Suit.*`,而是直接使用`.*`,这是合法的,因为我们提前知道`self`就`Suit`。(后面会详细讲解enum的特性,自定义值,取值..)  
使用`struct`来定义结构体,结构体有自己的属性和方法,类似于enum以及class,但是`struct`和'enum'都是值类型,而`class`是引用类型。值类型和引用类型的区别:值类型总是赋值一份新的,引用类型却只是将地址传递过来。值类型互补干扰,而引用类型,任何一个地方改变,会影响到全部引用变量。
```swift
struct Card {
    var rank: Rank
    var suit: Suit
    func simpleDescription() -> String {
        return "The \(rank.simpleDescription()) of \(suit.simpleDescription())"
    }
}
let threeOfSpades = Card(rank: .Three, suit: .Spades)
let threeOfSpadesDescription = threeOfSpades.simpleDescription()
```
### 协议和扩展
protocol是一个对象类型,但是并没存在protocol对象,我们无法实例化他。protocol只是列出一些属性和方法,属性没有值.实际的对象类型将会完整的定义他们。枚举,结构体,类都可以*实现*协议。
```swift
protocol ExampleProtocol {
    var simpleDescription: String { get }
    mutating func adjust()
}
class SimpleClass: ExampleProtocol {
    var simpleDescription: String = "A very simple class."
    var anotherProperty: Int = 69105
    func adjust() {
        simpleDescription += "  Now 100% adjusted."
    }
}
var a = SimpleClass()
a.adjust()
let aDescription = a.simpleDescription
struct SimpleStructure: ExampleProtocol {
    var simpleDescription: String = "A simple structure"
    mutating func adjust() {
        simpleDescription += " (adjusted)"
    }
}
var b = SimpleStructure()
b.adjust()
let bDescription = b.simpleDescription
```
**注意** 在定义protocol是我们使用了`mutating`这个关键字用于`struct`中,表示这个方法会改变属性的值。(后面会详细介绍)
`extension`用于扩展一个类型,例如添加属性,方法。
```swift
extension Int: ExampleProtocol {
    var simpleDescription: String {
        return "The number \(self)"
    }
    mutating func adjust() {
self += 42 }
}
print(7.simpleDescription)
```
### 错误处理
swift中有一`Error`协议,我们可以*adopt*他来自定义错误类型。
```swift
enum PrintError:Error{
    case outOfPaper
    case noToner
    case onFire
}
```
使用`throw`来触发错误,在函数后面跟上`throws`表示这个函数可以抛出错误
```swift
func send(job: Int, toPrinter printerName: String) throws -> String {
    if printerName == "Never Has Toner" {
        throw PrinterError.noToner
    }
    return "Job sent"
}
```
有很多方式来处理异常  
第一种'do-catch',在`do`代码块中,在代码前加上`try`表示这个代码可以跑出错误,在`catch`代码块中,错误会默认以`error`名传递给`catch`,也可以自己给一个名字`catch(myError)`
```swift
do {
    let printerResponse = try send(job: 1040, toPrinter: "Bi Sheng")
    print(printerResponse)
} catch {
    print(error)
}
```
可以使用多个catch来处理不同的错误
```swift
do {
    let printerResponse = try send(job: 1440, toPrinter: "Gutenberg")
    print(printerResponse)
} catch PrinterError.onFire {
    print("I'll just put this over here, with the rest of the fire.")
} catch let printerError as PrinterError {
    print("Printer error: \(printerError).")
} catch {
    print(error)
}
```
第二种使用`try?`来把结果转成`optional`类型。如果函数返回了错误,那么错误信息会被丢弃,并且结果为nil。否则会包含函数返回值。
```swift
let printerSuccess = try? send(job: 1884, toPrinter: "Mergenthaler")
let printerFailure = try? send(job: 1885, toPrinter: "Never Has Toner")
```
使用`defer`来写一段代码,这段代码会在函数,函数所有代码执行完成后执行,即在函数返回之前执行,不论这个函数是是否抛出错误,这段代码都会执行。可以用`defer`来做设置以及清除设置。
```swift
var fridgeIsOpen = false
let fridgeContent = ["milk", "eggs", "leftovers"]

func fridgeContains(_ food: String) -> Bool {
    fridgeIsOpen = true
    defer {
        fridgeIsOpen = false
    }

    let result = fridgeContent.contains(food)
    return result
}
fridgeContains("banana")
print(fridgeIsOpen)
```
### 泛型
使用`<name>`创建,泛型函数或者类型。(泛型到底是个啥,后面讲解)
```swfit
func makeArray<Item>(repeating item: Item, numberOfTimes: Int) -> [Item] {
    var result = [Item]()
    for _ in 0..<numberOfTimes {
        result.append(item)
    }
    return result
}
makeArray(repeating: "knock", numberOfTimes:4)
```
你也可以创建泛型函数,方法,枚举,类,结构体
```swift
// Reimplement the Swift standard library's optional type
enum OptionalValue<Wrapped> {
case None
    case Some(Wrapped)
}
var possibleInteger: OptionalValue<Int> = .None
possibleInteger = .Some(100)
```
在类型后面使用`where`来给出依赖列表
```swift
func anyCommonElements<T: Sequence, U: Sequence where T.Iterator.Element: Equatable, T.Iterator.Element ==             U.Iterator.Element>(_ lhs: T, _ rhs: U) -> Bool {
    for lhsItem in lhs {
        for rhsItem in rhs {
            if lhsItem == rhsItem {
                return true
            }
        }
    }
    return false
}
anyCommonElements([1, 2, 3], [3])
```
# swift详解
## 语法基础(The Basic)
### 变量定义
常量通过`let`定义,变量通过`var`定义,可以一次定义多个变量用`,`隔开。如果你确定变量的值在运行过程中不会改变的话,就用`let`定义它(例如配置信息等)。
> 2.0 中测试出如果变量定义名称相同,会覆盖前面的定义。

```swift
let maximumNumberOfLoginAttempts = 10
var currentLoginAttempt = 0
var x = 0.0, y = 0.0, z = 0.0
```
### 类型声明
你可以在定义变量的时候,指定变量的类型。`var welcome:String="hello"`(定义变量是如果类型不是`optional`必须初始化一个值)。你也可以在一行中同时定义几个相同类型的变量`var red, green, blue: Double?`
### 变量名
你几乎可以使用任何一个你喜欢的字符作为名称
```swift
let π = 3.14159
let 你好 = "你好世界"
let 🐶🐮 = "dogcow"
```
你可以在变量声明之后给其赋予相同类型的任意值,但是常量一旦定义就不可修改其值。**如果定义的常量是个类的实例,那么改变这个实例的属性是可以的,因为他是引用类型。**
### 打印变量
```swift
let name:String="Merlin.G"
let age:Int=20
print("\(name) are \(age) years old")
//Merlin.G are 20 years old
```
### 注释
swift使用`//`和`/**/`来注释代码,swift也不需要`;`结尾,除非你在一行内执行多条命令`let name:String="Merlin.G";let age:Int=20`
### 整型
swift提供了8,16,32,64位类型整数,分别为([U]Int8,[U]Int16,[U]Int32,[U]Int64)。swift中提供了Int和UInt两个类型他们有当前平台长度一直。
### 小数
swift中有两种小数类型`Float`32位,`Double`64位。
### 类型安全与推断
swift是类型安全的,这需要你明确知道,你所操作的对象的类型。比如你的变量是String那么就不可以传Int过去。swift会在编译时就检查这些类型。但是swift也提供了类型推断功能,比如`var unknown_type=32`这里swift会自动推断出unknown_type变量的类型为Int。默认swift把整数推断为Int,小数推断为Double。  
表达式也会自动被推断
```swift
let anotherPi = 3 + 0.14159
// anotherPi 会被推测为 Double 类型
//这里3并没有类型
```
### Numeric Literals
整数有多重写法
- 没有前缀的十进制数
- `0b`开头,二进制
- `0o`开头,8进制
- `0x`开头,16进制

```swift
let decimalInteger = 17
let binaryInteger = 0b10001       // 17 2进制
let octalInteger = 0o21           // 17 8进制
let hexadecimalInteger = 0x11     // 17 16进制
```
小数的写法  
小数可以用十进制和十六进制,小数点两边至少一边有值。指数在十进制中用`e`,十六进制中用`p`。
```swift
let decimalDouble = 12.1875
let exponentDouble = 1.21875e1
let hexadecimalDouble = 0xC.3p0
```
**数值还可以包含额外的格式来增强可读性** 他们可以包含额外的`0`和`_`
```swift
let paddedDouble = 000123.456
let oneMillion = 1_000_000
let justOverOneMillion = 1_000_000.000_000_1
```
### 数值类型转换
如果不是明确性趣优化内存,性能等,不要使用UInt8...这种整数类型,尽量直接使用Int类型。   
不同类型的整数能存储的值有固定范围(`Int8.min`和`Int8.max`)。因为swift是类型安全所以一旦赋值范围不在(min~max)那么就报错。
```swift
let cannotBeNegative: UInt8 = -1
// Uint8 不可以保存负数
let tooBig: Int8 = Int8.max + 1
// 超出Int8的最大范围了
```
两个不同类型的变量,需要进行类型转换后才可以使用。*(当尝试将字符串转为数字式返回的`optional`类型,而这段代码中UInt16(one)返回的却是UInt16,貌似是构造函数搞鬼(-_-)没有细究)*
```swift
let twoThousand: UInt16 = 2_000
let one: UInt8 = 1
let twoThousandAndOne = twoThousand + UInt16(one)
```
### 类型别名
类型别名是个当前类型指定一个可选的名称,这个别名与原类型是同一个东西。使用`typealias`
```swift
typealias AudioSample = UInt16
var maxAmplitudeFound = AudioSample.min
```
### 布尔类型
swift的布尔类型为`Bool`。只有`true`和`false`连个值。
> swift中控制流的条件是Bool类型,而且只能是Bool类型,如果是其他类型,需要转换为Bool类型,否则会报错.例如 if 2 {}就报错

### 元祖
元祖有点python元祖的味道。元祖内的元素类型不需要相同
```swift
let http404Error = (404, "Not Found")
// http404Error is of type (Int, String), and equals (404, "Not Found")
```
将元祖拆分 *(python和es2015更简洁)*
```swift
let (statusCode, statusMessage) = http404Error
print("The status code is \(statusCode)")
// Prints "The status code is 404"
print("The status message is \(statusMessage)")
// Prints "The status message is Not Found
```
也可以用`_`忽略某个位置的值
```swift
let (justTheStatusCode, _) = http404Error
print("The status code is \(justTheStatusCode)")
```
访问元祖的元素,默认是使用下标从0开始`print("The status code is \(http404Error.0)")`  
我们也可以给元素指定名称,这样就可以用名称来访问元素
```swift
let http200Status = (statusCode: 200, description: "OK")
print("The status code is \(http200Status.statusCode)")
print("The status message is \(http200Status.description)")
```
### Optionals
当变量的值有可能不存在是时候,你可能会使用`Optionals`.`optional`有两种情况:要么他有值,然后你可以解析出来,要么就没有值。  
一个例子:你想把一个字符串转换为Int类型,但是这个字符串有可能无法转换为Int比如"hello"。
```swift
let possibleNumber = "123"
let convertedNumber = Int(possibleNumber)
// convertedNumber is inferred to be of type "Int?", or "optional Int”
/*
* 这里的转换会返回一个Int类型还是Int?,结果是:
* possibleNumber: String = "123"
* convertedNumber: Int? = 123
*/
/*********************************************/
let possibleNumber = "hello"
let convertedNumber = Int(possibleNumber)
/*
* 这里的转换会返回一个Int类型还是Int?,结果是:
* possibleNumber: String = "hello"
* convertedNumber: Int? = nil
*/
```
因为这里的构造函数可能失败,所以他返回了一个`Int?`,`?`表示这是个`optional`类型。
### nil
默认optional类型的值为`nil`,表示他不包含值。
```swift
var surveyAnswer: String?
//surveyAnswer: String? = nil
var serverResponseCode: Int? = 404
serverResponseCode = nil
//serverResponseCode: Int? = nil
```
### if和强制解析
可以通过if语句判断变量是否包含值,如果包含的话,在变量后面加上`!`可以取出值。
```swift
if convertedNumber != nil {
    print("convertedNumber has an integer value of \(convertedNumber!).")
}
```
### Optional Binding
可以通过*optional binding* 来判断一个optional是否包含值,如果包含的话,就把它们赋值给,临时的常量或者变量。可以再'if'和`while`语句中使用。
```swift
if let constantName = someOptional {
    statements
}
```
这样的话上面的字符串转Int就可以这么写
```swift
if let actualNumber = Int(possibleNumber) {
    print("\"\(possibleNumber)\" has an integer value of \(actualNumber)")
} else {
    print("\"\(possibleNumber)\" could not be converted to an integer")
}
// Prints ""123" has an integer value of 123"
/*
这里可以这么理解,如果Int(possibleNumber)成功把字符串转成了Int那么把这个值赋给actualNumber*(“It has already been initialized with the value contained within the optional, and so there is no need to use the ! suffix to access its value”是啥意思,为毛已经被初始化)*
*/
```
如果想要在if代码块中修改临时变量,那么需要用`var`定义这个变量。   
你可以在一条if中包含多个条件,他们用`,`分离,只要其中一个为false,整条语句就为false
```swift
if let firstNumber = Int("4"), let secondNumber = Int("42"), firstNumber < secondNumber && secondNumber < 100 {
    print("\(firstNumber) < \(secondNumber) < 100")
}
// Prints "4 < 42 < 100"

if let firstNumber = Int("4") {
    if let secondNumber = Int("42") {
        if firstNumber < secondNumber && secondNumber < 100 {
            print("\(firstNumber) < \(secondNumber) < 100")
        }
    }
}
// Prints "4 < 42 < 100"
```
### Implicitly Unwrapped Optionals(隐式解析)
上面可以看到,可以通过if来判断optional是否有值。但是有的时候程序一旦运行optional总是有值的。这样的话就没有必要每次去判断然后解析optional的值。我们可以使用`var a:String!="hello"`这里用的是`!`。这样定义变量后,当访问变量的时候swift会自动解析出它包含的值。
```swift
let possibleString: String? = "An optional string."
let forcedString: String = possibleString! // requires an exclamation mark

let assumedString: String! = "An implicitly unwrapped optional string."
let implicitString: String = assumedString // no need for an exclamation mark
```
你仍然可以把这个变量当做普通的optional来处理
```swift
if assumedString != nil {
    print(assumedString)
}
if let definiteString = assumedString {
    print(definiteString)
}
// Prints "An implicitly unwrapped optional string."
```
### 错误处理
当一个函数发生错误时,他会抛出异常。他的调用者,可以捕获异常并进行适当的处理,定义函数可以抛出异常需要在定义时加上`throws`,当你调用一个可能抛出异常的函数时,使用`try`。catch可以捕获不同的异常。
```swift
func canThrowAnError() throws {
    // this function may or may not throw an error
}
do {
    try canThrowAnError()
    // no error was thrown
} catch {
    // an error was thrown
}
func makeASandwich() throws {
    // ...
}

do {
    try makeASandwich()
    eatASandwich()
} catch SandwichError.outOfCleanDishes {
    washDishes()
} catch SandwichError.missingIngredients(let ingredients) {
    buyGroceries(ingredients)
}
```
### Assertions(断言)
有时候,在缺少某些必要条件的时候你的代码没办法继续运行。这时候你可以使用断言机制。可以用断言调试代码。当断言条件不满足时抛出异常等。
```swift
let age = -3
assert(age >= 0, "A person's age cannot be less than zero")
// this causes the assertion to trigger, because age is not >= 0”
```
断言也可以不发送消息`assert(age >= 0)` **断言慎用！**。
## 基本运算符(Basic Operators)
算术运算符`= + - * / % ++ -- -= += *= /= %=`  
比较操作符`> < == != <= >=`  
元祖也可以进行比较,只要他们包含相同数量的值,并且值可以进行比较。    
他会从做到右依次比较,每次只比较一个元素,直到他们不相同,否元祖就是相等的。  
```swift
(1, "zebra") < (2, "apple")   // true because 1 is less than 2
(3, "apple") < (3, "bird")    // true because 3 is equal to 3, and "apple" is less than "bird"
(4, "dog") == (4, "dog")      // true because 4 is equal to 4, and "dog" is equal to "dog"
```
三元运算符` question ? answer1 : answer2`
### Nil-Coalescing Operator
`a ?? b`表示:如果a这个optional类型有值的话,就取出来,否则用b作为默认值。他类似这样`a != nil ? a! : b`。这个方式可以做很多有趣的事情,比如尝试获取系统配置,如果没有获取到,就给定义一个默认值。
```swift
let defaultColorName = "red"
var userDefinedColorName: String?   // defaults to nil
var colorNameToUse = userDefinedColorName ?? defaultColorName
// userDefinedColorName is nil, so colorNameToUse is set to the default of "red"

userDefinedColorName = "green"
colorNameToUse = userDefinedColorName ?? defaultColorName
// userDefinedColorName is not nil, so colorNameToUse is set to "green”
```
### Range Operators(区间运算符)
`a...b`包含两边的值 ,`a..<b`不包含右边的值
```swift
for index in 1...5 {
    print("\(index) times 5 is \(index * 5)")
}
// 1 times 5 is 5
// 2 times 5 is 10
// 3 times 5 is 15
// 4 times 5 is 20
// 5 times 5 is 25

let names = ["Anna", "Alex", "Brian", "Jack"]
let count = names.count
for i in 0..<count {
    print("Person \(i + 1) is called \(names[i])")
}
// Person 1 is called Anna
// Person 2 is called Alex
// Person 3 is called Brian
// Person 4 is called Jack
```
### 逻辑运算符
`&&`,`||`,'！',和大多数语言一样是短路运算
## 字符串和字符(Strings and Characters)
String有一系列Character组成,string的内容可以通过多种方式访问。swift中字符串用`""`表示。
### 创建String
可以直接给变量赋值`""`这样就是一个空字符串,也可以`String()`。isEmpty属性表示字符串是否为空,他是Bool类型。
```swift
let s=""
var s=String()
print(s.isEmpty)
```
字符串可以直接用`+`链接,可以通过遍历String的characters属性来处理每一个字符。
```swift
for character in "Dog!🐶".characters {
    print(character)
}
// D
// o
// g
// !
// 🐶
```
字符串也可以通过Character数组来实例化,*String还提供很多方法具体看api*
```swift
let catCharacters: [Character] = ["C", "a", "t", "!", "🐱"]
let catString = String(catCharacters)
print(catString)
// Prints "Cat!🐱”
```
### 访问和修改字符串
我们可以通过函数以及属性来访问修改字符串,也可以使用下标    
#### 字符串索引
swift中每个字符串都有索引类型,他标记每个字符在字符串中的位置。因为不同的字符集使用的存储空间是不一样的,所以不可以使用整数下标。  
`startIndex`属性是字符串的第一位置索引,`endIndex`属性是字符串**最后一个字符的下一个位置**,所以`endIndex`不可以作为有效的索引。如果一个字符串为空那么endIndex=startIndex  
可以通过字符串的`index(before:)`,`index(after:)`方法来访问字符。为了能够多次使用一个索引你可以使用`index(_:offsetBy:)`来设置一个索引
```swift
let greeting = "Guten Tag!"
greeting[greeting.startIndex]
// G
greeting[greeting.index(before: greeting.endIndex)]
// !
greeting[greeting.index(after: greeting.startIndex)]
// u
let index = greeting.index(greeting.startIndex, offsetBy: 7)
greeting[index]
// a
```
如果索引位置超出了字符串,那么会报错
```swift
greeting[greeting.endIndex] // error 上面提到了endIndex不可作为有效的索引
greeting.index(after: endIndex) // error
```
使用characters.indices可以取出字符串中所有的索引
```swift
for index in greeting.characters.indices {
    print("\(greeting[index]) ", terminator: "")
}
// Prints "G u t e n   T a g !"
```
#### 插入和删除
将一个字符插入字符串中使用`insert(_:at:)`,将一个字符串插入另一个字符串中使用`insert(contentsOf:at:)`。**2.0版本有insertContentsOf方法**
```swift
var welcome = "hello"
welcome.insert("!", at: welcome.endIndex)
// welcome now equals "hello!"

welcome.insert(contentsOf:" there".characters, at: welcome.index(before: welcome.endIndex))
// welcome now equals "hello there!"
```
删除一个字符可以使用`remove(at:)`,删除一段字符串使用`removeSubrange(_:)` **2.0有removeRange**
```swift
welcome.remove(at: welcome.index(before: welcome.endIndex))
// welcome now equals "hello there"

let range = welcome.index(welcome.endIndex, offsetBy: -6)..<welcome.endIndex
welcome.removeSubrange(range)
// welcome now equals "hello"
```
#### 判断字符串开头结尾包含的字符串
`hasPrefix(_:)`开头,`hasSuffix(_:)`结尾,他们返回Bool。
> 关于unicode 再说吧

## 集合类型(Collection Types)
swift提供了三种原生Collection类型:数组,集合,字典。数组是有序的,集合和字典无序。  
数组,集合,字典都是可变的。但是如果用`let`声明的话,将不可变,也就是他们的大小,内容都不能改变。  
### 数组
数组有多种创建方法
```swift
var someInts = [Int]()//创建一个空数组
someInts.append(3)//往数组添加值
someInts = []//清空数组

//用默认值初始化数组
var threeDoubles = Array(repeating: 0.0, count: 3)//数组长度为3,每个元素都是0.0
//通过两个数组相加得到另一个数组
var anotherThreeDoubles = Array(repeating: 2.5, count: 3)
var sixDoubles = threeDoubles + anotherThreeDoubles
//直接初始化值
var shoppingList = ["Eggs", "Milk"]//类型推断
var shoppingList: [String] = ["Eggs", "Milk"]
```
#### 访问数组
`count`返回数组长度。`isEmpty`是否为空。`append`添加值。  
- 修改数组元素`“shoppingList[0] = "Six eggs"`
- 替换掉一段元素`shoppingList[4...6] = ["Bananas", "Apples"]`
- 插入到指定位置`shoppingList.insert("Maple Syrup", at: 0)`
- 删除指定位置元素 `let mapleSyrup = shoppingList.remove(at: 0)`
- 删除最后一个元素 `let apples = shoppingList.removeLast()`

#### 循环一个数组
`for-in`可以遍历数组的每一个元素,如果想要同时遍历下标以及值,可以使用`enumerated()`方法
```swift
for item in shoppingList {
    print(item)
}
// Six eggs
// Milk
// Flour
// Baking Powder
// Bananas

for (index, value) in shoppingList.enumerated() {
    print("Item \(index + 1): \(value)")
}
```
### 集合
集合中的元素是无序的,并且元素唯一。集合中元素的类型必须可以计算自身的hash值。Int,String,Double,Bool,Enumerations都是可hash的,所以他们可以作为集合的元素,也可以作为字典的key。集合比较两个元素是否相等使用`a.hashValue == b.hashValue`  
> 也可以自己定义一个类型,来作为集合元素或者字典的key,但是这个类型必须实现 Hashable协议,他需要提供一个Int类型的属性包含hashValue

#### 集合相关操作
```swift
var letters = Set<Character>()//创建空集合
letters.insert("a")//往集合插入数值
letters = []//清空集合
var favoriteGenres: Set = ["Rock", "Classical", "Hip hop"]//集合不可以直接从列表推导过来,所以这里一定要加上Set
var favoriteGenres: Set<String> = ["Rock", "Classical", "Hip hop"]//指定类型初始化
favoriteGenres.contains("Funk")//判断集合是否包含"Funk"
favoriteGenres.remove("Rock")//删除指定元素,失败nil
favoriteGenres.removeAll()//删除所有元素
```
使用`for-in`遍历集合,集合也可以使用`sorted()`来排序
```swift

for genre in favoriteGenres.sorted() {
    print("\(genre)")
}
```
逻辑处理
- `intersection(_:)`//创建新的集合,A,B集合共有的部分
- `symmetricDifference(_:)`//创建新的集合,两个集合union之后去除共有的部分
- `union(_:)`//创建新的集合,A,B集合所有的元素放一起
- `subtracting(_:)`  //创建新的集合,包含在A,不包含在B的元素

包含关系
- `isSubset(of:)`B集合的元素是否都包含在A集合中
- `isSuperset(of:)`A集合是否包含B集合的所有元素
- `isStrictSubset(of:)`A,B两个集合元素都相同,但是A,B是不等的
- `isStrictSuperset(of:)`A,B两个集合元素都相同,但是A,B是不等的
- `isDisjoint(with:)`判断A,B是否有共同的元素
```swift
let oddDigits: Set = [1, 3, 5, 7, 9]
let evenDigits: Set = [0, 2, 4, 6, 8]
let singleDigitPrimeNumbers: Set = [2, 3, 5, 7]

oddDigits.union(evenDigits).sorted()
// [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
oddDigits.intersection(evenDigits).sorted()
// []
oddDigits.subtracting(singleDigitPrimeNumbers).sorted()
// [1, 9]
oddDigits.symmetricDifference(singleDigitPrimeNumbers).sorted()
// [1, 2, 9]

let houseAnimals: Set = ["🐶", "🐱"]
let farmAnimals: Set = ["🐮", "🐔", "🐑", "🐶", "🐱"]
let cityAnimals: Set = ["🐦", "🐭"]

houseAnimals.isSubset(of: farmAnimals)
// true
farmAnimals.isSuperset(of: houseAnimals)
// true
farmAnimals.isDisjoint(with: cityAnimals)
// true”
```
### 字典
字典也是无序的,他一key->value形式,与生活的字典差不多。
#### 字典基本操作
```swift
var namesOfIntegers = [Int: String]()//创建空字典
namesOfIntegers[16] = "sixteen"//如果字典存在key:16那么更行key:16的值,不存在就添加key:16
namesOfIntegers = [:]//清空字典
var airports = ["YYZ": "Toronto Pearson", "DUB": "Dublin"]//创建字典的另一种方式,自动推导类型
var airports: [String: String] = ["YYZ": "Toronto Pearson", "DUB": "Dublin"]//创建字典的另一种方式,声明类型
```
#### 字典访问
字典可以直接用key开或者对应元素的值,字典提供了`updateValue(_:forKey:)`方法,这个方法在调用时:如果可以不存在,则创建,存在则更新。但是这个方法会返回key对应的旧值(如果旧值存在的话),类型为optional,这样我们就可以判断是否是更新操作。当我们去读取字典的元素时,他返回的其实是一个optional类型,如果key对应值存在,返回该值,不存在返回nil。将key对应值赋值为nil,可以删除该元素。
```swift
airports["LHR"] = "London"
airports["LHR"] = "London Heathrow"//这里可以任意修改key对应值

//更新或添加key
if let oldValue = airports.updateValue("Dublin Airport", forKey: "DUB") {
    print("The old value for DUB was \(oldValue).")
}

//读取字典元素
if let airportName = airports["DUB"] {
    print("The name of the airport is \(airportName).")
} else {
    print("That airport is not in the airports dictionary.")
}
// Prints "The name of the airport is Dublin Airport.”

//将key对应值赋值为nil,可以删除key
airports["APL"] = "Apple International
airports["APL"] = nil

//使用removeValue(forKey:)来删除key,如果key存在返回key对应值(optional),不存在返回nil
if let removedValue = airports.removeValue(forKey: "DUB") {
    print("The removed airport's name is \(removedValue).")
} else {
    print("The airports dictionary does not contain a value for DUB.")
}
```
#### 遍历字典
`for-in`遍历字典,通过`keys`和`values`属性可以遍历字典的键和值。字典是无序的但是我们可以调用keys.sorted()或者values.sorted()。
```swift
for (airportCode, airportName) in airports {
    print("\(airportCode): \(airportName)")
}
for airportCode in airports.keys {
    print("Airport code: \(airportCode)")
}
for airportName in airports.values {
    print("Airport name: \(airportName)")
}
```
有时候你可能想把字典的keys或者values转化为数组
```swift
let airportCodes = [String](airports.keys)
// airportCodes is ["YYZ", "LHR"]

let airportNames = [String](airports.values)
// airportNames is ["Toronto Pearson", "London Heathrow"]
```
## 控制流(Control Flow)
swift提供了多种流程控制语法。包括循环`while`,分支`if`,`guard`,`switch`。以及`break`,`continue`  
swift也提供了`for-in`来更加方便的遍历数组,字典,ranges,字符串,以及其他序列对象  
### For-In循环
循环可以用来遍历序列,例如数字区间,数组,字符串
```swift
//刚进入循环是index为rang(1),一次结束后一次变成range(2)..。
//index在每次循环操作时自动创建,并且为常量。所以我们不需要声明index。
for index in 1...5{
    print("\(index) times 5 is \(index * 5)")
}
//如果你不想知道index的值,可以用"_"代替它
let base = 3
let power = 10
var answer = 1
for _ in 1...power {
    answer *= base
}
```
### While循环
while虚幻有两种情况:   
1.先判断条件是否符合   
```swift
while condition{
    statement
}
```
2.代码运行结束后再检测条件是否符合   
```swift
repeat{
    statement
}while condition
```
### if条件
```swift
temperatureInFahrenheit = 90
if temperatureInFahrenheit <= 32 {
    print("It's very cold. Consider wearing a scarf.")
} else if temperatureInFahrenheit >= 86 {
    print("It's really warm. Don't forget to wear sunscreen.")
} else {
    print("It's not that cold. Wear a t-shirt.")
}
// Prints "It's really warm. Don't forget to wear sunscreen."
```
### swift
如果条件判断较多的话用`switch`替代`if`是个不错的选择。swift会包给定的值,与多个模式进行匹配。通常是对一个值和多个与他类型相同的值进行比较。swift提供了更多的功能来实现较为复杂的模式匹配。`default`会在没有任何匹配时执行。每当匹配到一条规则后swift就会`break`出来。每一个case分支必须至少包含一条可执行语句。
```swift
switch some value to consider {
case value 1:
    respond to value 1
case value 2,
     value 3:
    respond to value 2 or 3
default:
    otherwise, do something else
}
```
case可以一次匹配多个模式,需要用`,`将他们隔开。
```swift
let anotherCharacter: Character = "a"
switch anotherCharacter {
case "a", "A":
    print("The letter A")
default:
    print("Not the letter A")
}
```
#### Interval Matching
模式可以是一个区间,判断给定值是否在该模式区间内。下面这个例子用数字区间
```swift
let approximateCount = 62
let countedThings = "moons orbiting Saturn"
var naturalCount: String
switch approximateCount {
case 0:
    naturalCount = "no"
case 1..<5:
    naturalCount = "a few"
case 5..<12:
    naturalCount = "several"
case 12..<100:
    naturalCount = "dozens of"
case 100..<1000:
    naturalCount = "hundreds of"
default:
    naturalCount = "many"
}
print("There are \(naturalCount) \(countedThings).")
// Prints "There are dozens of moons orbiting Saturn."
```
#### Tuple Matching
switch还可以使用元祖来做模式匹配。元祖中的元素既可以是值,也可以是区间,使用`_`来匹配所有情况。下面这个例子使用(Int,Int)元祖。
```swift
let somePoint = (1, 1)
switch somePoint {
case (0, 0):
    print("(0, 0) is at the origin")
case (_, 0):
    print("(\(somePoint.0), 0) is on the x-axis")
case (0, _):
    print("(0, \(somePoint.1)) is on the y-axis")
case (-2...2, -2...2):
    print("(\(somePoint.0), \(somePoint.1)) is inside the box")
default:
    print("(\(somePoint.0), \(somePoint.1)) is outside of the box")
}
// Prints "(1, 1) is inside the box"
```
#### Value 绑定
swift case可以绑定值或者他匹配的值到临时常量或者变量上,因为绑定到了常量或者变量上,这样这个case内的语句就可以访问到这个他。
```swift
let anotherPoint = (2, 0)
switch anotherPoint {
case (let x, 0):
    print("on the x-axis with an x value of \(x)")
case (0, let y):
    print("on the y-axis with a y value of \(y)")
case let (x, y):
    print("somewhere else at (\(x), \(y))")
}
// Prints "on the x-axis with an x value of 2"

//多个模式在一个case中时也支持值绑定
let stillAnotherPoint = (9, 0)
switch stillAnotherPoint {
case (let distance, 0), (0, let distance):
    print("On an axis, \(distance) from the origin")
default:
    print("Not on an axis")
}
```
#### Where
swift case可以使用`where`来做额外的条件验证。*(有点意思)*
```swift
let yetAnotherPoint = (1, -1)
switch yetAnotherPoint {
case let (x, y) where x == y:
    print("(\(x), \(y)) is on the line x == y")
case let (x, y) where x == -y:
    print("(\(x), \(y)) is on the line x == -y")
case let (x, y):
    print("(\(x), \(y)) is just some arbitrary point")
}
// Prints "(1, -1) is on the line x == -y"
```
### Control Transfer Statements(控制跳转)
swift中有5个控制跳转语句`continue`,`break`,`fallthrough`,`return`,`throw`
**continue** 停止当前循环,执行下一次循环  
**break** 立即结束整个控制流,可以用在`switch`或者循环中。   
**fullthrough** 可以让switch匹配到一个case之后继续想下匹配  
### Labeled Statements(标签)*(不愿用)*
。。。。
### Early Exit(提前退出)
`guard`语句和`if`类似,依赖于条件来决定是否执行代码。`guard`要求条件必须为真才会执行代码块,和`if`不同之处是`guard`必须有一个`else`语句,当条件不为true时执行else代码块。**guard** 可读性比较高
```swift
func greet(person: [String: String]) {
    guard let name = person["name"] else {
        return
    }
    print("Hello \(name)!")

    guard let location = person["location"] else {
        print("I hope the weather is nice near you.")
        return
    }
    print("I hope the weather is nice in \(location).")
}
greet(person: ["name": "John"])
// Prints "Hello John!"
// Prints "I hope the weather is nice near you."
greet(person: ["name": "Jane", "location": "Cupertino"])
// Prints "Hello Jane!"
// Prints "I hope the weather is nice in Cupertino."
```
### Checking API Availability(检查Api是否可用)
如果在swift中调用了不存在的api,会在编译时报错。  
使用`if`或者`guard`来判断api在运行时是否可用。编译器会使用可用的api来执行代码
```swift
if #available(iOS 10, macOS 10.12, *) {
    // Use iOS 10 APIs on iOS, and use macOS 10.12 APIs on macOS
} else {
    // Fall back to earlier iOS and macOS APIs
}
```
上面代码的意思是版本号大于IOS10,或者macOS10.12的平台上使用`if`代码块。`*`是必须的,表示其他任何平台。`if`语句表示代码执行的最低版本。   
通常可用的条件列表包含名称和版本号,名称可以是"iOS, macOS, watchOS, and tvOS" 例如 IOS 10 ,macOS 10.12。
```swift
if #available(platform name version, ..., *) {
    statements to execute if the APIs are available
} else {
    fallback statements to execute if the APIs are unavailable|
}
```
## 函数(Functions)
函数也是一种类型,这意味着函数可以被当做参数,或者返回值。
### 参数与返回值
函数可以有多个参数,也可以没有参数,可以有返回值,也可以没有。
```swift
func sayHello(){
    print("sayHello")
}
func sayHello(name:String)->String{
    print("hello \(name)")
    return "say hello"
}
```
函数可以返回一个元祖来包含多个返回值。
```swift
func minMax(array: [Int]) -> (min: Int, max: Int) {
    var currentMin = array[0]
    var currentMax = array[0]
    for value in array[1..<array.count] {
        if value < currentMin {
            currentMin = value
        } else if value > currentMax {
            currentMax = value
        }
    }
    return (currentMin, currentMax)
    //返回一个元祖,上面定义了元祖元素的名字,所以当我们获得函数返回值的时候,可以用名称获取对应的值
}
var list=[1,2,3,4,1,12,4,234,23,67]
var result=minMax(array:list)//2.0会有报错,因为2.0没有默认将array参数标签(label)设为array
print(result.min)
print(result.max)
```
函数也可以返回optional类型
```swift
func minMax(array: [Int]) -> (min: Int, max: Int)? {
    return nil
}
var list=[1,2,3,4,1,12,4,234,23,67]
if let result=minMax(array:list){
    print(result.min)
    print(result.max)
}
guard let test=minMax(array:list) else{
    print("nothing")
}
print(result.min)
print(result.max)
```
函数参数默认都有标签,且标签名为参数名,通常我们会自定义标签。增加代码的可读性。如果给参数添加了自定义标签,传递参数时必须使用自定义标签。如果不希望参数有标签的话,可以使用`_`代替标签,这样传参数时就不需要标签名。   
函数体内部使用的时参数名而不是标签名。标签相当于对外,参数名对内。(挺有意思)
```swift
func greet(person: String, from hometown: String) -> String {
    return "Hello \(person)!  Glad you could visit from \(hometown)."
}
print(greet(person: "Bill", from: "Cupertino"))
func someFunction(_ firstParameterName: Int, secondParameterName: Int) {
    // In the function body, firstParameterName and secondParameterName
    // refer to the argument values for the first and second parameters.
}
someFunction(1, secondParameterName: 2)
```
函数也支持默认值,但是我们都会讲带默认值的参数列表放在最后。
#### 可变参数
函数的一个参数可以接收一个或者多个相同类型的值(类似于数组列表)。调用函数式可以向这个参数传递不同数量的同类型数值。在函数体内部这个参数类型被变成数组。
```swift
func arithmeticMean(_ numbers: Double...) -> Double {
    var total: Double = 0
    for number in numbers {
        total += number
    }
    return total / Double(numbers.count)
}
arithmeticMean(1, 2, 3, 4, 5)
// returns 3.0, which is the arithmetic mean of these five numbers
arithmeticMean(3, 8.25, 18.75)
// returns 10.0, which is the arithmetic mean of these three numbers”
```
函数的参数默认值常量,如果在函数体内部改签参数的值,会报错。如果你希望在函数运行结束后参数的修改是持续的,那么需要把参数定义为`in-out`。   
只需在参数前面加上`inout`关键字。in-out参数有一个值被传到函数中,这个值在函数中修改,然后这个值会传回给原始变量并修改其值。只能把变量当做in-out参数,常量和字面值因为不可修改所以不能传递。对于`in-out`参数,传参时在变量前添加`&`。
```swift
func swapTwoInts(_ a: inout Int, _ b: inout Int) {
    let temporaryA = a
    a = b
    b = temporaryA
}
var someInt = 3
var anotherInt = 107
swapTwoInts(&someInt, &anotherInt)
print("someInt is now \(someInt), and anotherInt is now \(anotherInt)")
// Prints "someInt is now 107, and anotherInt is now 3"
```
### 函数类型
每一个函数都有一个特殊的"function type",有参数类型和返回类型组成。
```swift
func addTwoInts(_ a: Int, _ b: Int) -> Int {
    return a + b
}
func multiplyTwoInts(_ a: Int, _ b: Int) -> Int {
    return a * b
}
func printHelloWorld() {
    print("hello, world")
}
```
上面前两个函数类型为(Int,Int)->Int,后一个为()->Void
#### 使用函数类型
函数类型跟其他类型一样用法
```swift
func addTwoInts(_ a: Int, _ b: Int) -> Int {
    return a + b
}
var mathFunction: (Int, Int) -> Int = addTwoInts
print("Result: \(mathFunction(2, 3))")
```
这里相当于变量mathFunction类型为(Int,Int)->Int,因为addTwoInts和他类型一致,所以可以赋值给他。然后就可以正常调用了。
#### 函数类型被当做参数传递
```swift
func printMathResult(_ mathFunction: (Int, Int) -> Int, _ a: Int, _ b: Int) {
    print("Result: \(mathFunction(a, b))")
}
printMathResult(addTwoInts, 3, 5)
```
#### 函数类型被当做返回类型
```swift
func stepForward(_ input: Int) -> Int {
    return input + 1
}
func stepBackward(_ input: Int) -> Int {
    return input - 1
}
func chooseStepFunction(backward: Bool) -> (Int) -> Int {
    return backward ? stepBackward : stepForward
}
var currentValue = 3
let moveNearerToZero = chooseStepFunction(backward: currentValue > 0)
// moveNearerToZero now refers to the stepBackward() function

//moveNearerToZero=stepBackward类型为(Int)->Int

print("Counting to zero:")
// Counting to zero:
while currentValue != 0 {
    print("\(currentValue)... ")
    currentValue = moveNearerToZero(currentValue)
}
print("zero!")
// 3...
// 2...
// 1...
// zero!
```
#### 内嵌函数
上面所介绍的都是全局函数,他们存在于全局域中。函数也可定义在一个函数体内部,也就是内嵌函数。内嵌函数对外是不可见的,只对当前的函数内可见,当然要想对外可见,我们可以通过当前把它返回出来。
```swift
func chooseStepFunction(backward: Bool) -> (Int) -> Int {
    func stepForward(input: Int) -> Int { return input + 1 }
    func stepBackward(input: Int) -> Int { return input - 1 }
    return backward ? stepBackward : stepForward
}
var currentValue = -4
let moveNearerToZero = chooseStepFunction(backward: currentValue > 0)
// moveNearerToZero now refers to the nested stepForward() function”

while currentValue != 0 {
    print("\(currentValue)... ")
    currentValue = moveNearerToZero(currentValue)
}
print("zero!")
// -4...
// -3...
// -2...
// -1...
// zero!”
```

## 闭包(Closures)
.....

## 枚举(Enumerations)
枚举是定义一个新的类型。case可以分开定义,也可以放在一行。当变量类型为enum时,可以省略enum名称直接用`.case`给其赋值
```swift
enum CompassPoint {
    case north
    case south
    case east
    case west
}
enum Planet {
    case mercury, venus, earth, mars, jupiter, saturn, uranus, neptune
}
var directionToHead = CompassPoint.west
directionToHead = .east
```
### switch 匹配enum
因为directionToHead是enum类型所以匹配时直接用`.case`,如果用'enum'需要穷举enum所有的项,否则会报错。
```swift
directionToHead = .south
switch directionToHead {
case .north:
    print("Lots of planets have a north")
case .south:
    print("Watch out for penguins")
case .east:
    print("Where the sun rises")
case .west:
    print("Where the skies are blue")
}
// Prints "Watch out for penguins"
```
### 原始值
枚举成员可以有默认值,默认值的类型一致.定义时要在添加类型名称,如果没有给成员赋值的话,swift会根据类型给定自动给定原始值.
```swift
enum ASCIIControlCharacter: Character {
    case Tab = "\t"
    case LineFeed = "\n"
    case CarriageReturn = "\r"
}

enum Planet: Int {
    case Mercury = 1, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune
}
//这里会自动给Mercury后面的成员原始值加1.

enum CompassPoint: String {
    case North, South, East, West
}
//String类型成员默认原始值为成员名

//通过rawValue可以获取原始值
let p=Planet.Venus.rawValue
```
### 从原始值初始化
如果设置了原始值类型,那么枚举对象会得到一个初始化方法,他接受原始值类型的值,从而获取到枚举成员,或者nil.这个方法会去匹配所有的成员,如果匹配到了则返回,没有则返回nil,所有她的返回类型是个`optional`.
```swift
let possiblePlanet = Planet(rawValue: 7)
// possiblePlanet is of type Planet? and equals Planet.uranus

enum Planet:Int{
    case venus,earth,uranus
}
let p1=Planet(rawValue:1)
print(p1!)
//"earth\n"
let p2=Planet(rawValue:4)
//nil
```
## 类和结构体(Classes and Structures)
### 类和结构体对比
- 定义属性用于存储值
- 定义函数用于提供功能
- 定义下标用于访问值
- 定义构造方法用于初始化
- 通过扩展来添加新的功能
- 实现协议来提供通用功能

类有一些结构体没有的特性
- 继承
- 类型转化允许在运行时检查和解释类的实例
- 结构函数允许在实例销毁前做一些操作
- 类的实例的引用计数可以有很多

### 定义
```swift
struct Resolution {
    var width = 0
    var height = 0
}
class VideoMode {
    var resolution = Resolution()
    var interlaced = false
    var frameRate = 0.0
    var name: String?
}
```
### 类和结构体实例
```swift
let someResolution = Resolution()
let someVideoMode = VideoMode()
```
### 访问属性
```swift
print("The width of someResolution is \(someResolution.width)")
print("The width of someVideoMode is \(someVideoMode.resolution.width)")
someVideoMode.resolution.width = 1280
```
### 结构体成员构造hanshu
所有的结构体都会自动有一个构造函数,参数为所有的属性.类没有默认的成员构造函数.
```swift
let vga = Resolution(width:640, height: 480)
```
### 值和引用类型
结构体和枚举都是值类型,这意味着,赋值操作是一个复制的过程,创建新的实例.而类是引用类型,赋值操作时没有创建新的实例,而是让变量引用同一个地址.String,Array,Dictionary都是值类型他们是通过结构体实现的.
判断两个变量是否引用同一个类实例使用`===`判断.`==`只是判断是否有值相等.

## 属性(Properties)
属性将值和特定的类,结构体,枚举链接起来.存储属性用于存储值,而计算属性用于计算出一个值.计算属性可以在类,结构体,枚举中使用,而存储属性只能用于类和结构体.  
还可以定义属性观察期,来监听属性的变化.
### 存储属性
存储属性实际就是常量或者变量,它作为类或者结构体实例的一部分.  
对于结构体,如果有存储属性被定义为常量属性,定义了之后就不能改变该属性的值.对于常量结构体实例,任何属性值都不可被修改,因为他是值类型
```swift
struct FixedLengthRange {
    var firstValue: Int
    let length: Int
}
var rangeOfThreeItems = FixedLengthRange(firstValue: 0, length: 3)

rangeOfThreeItems.firstValue=10
rangeOfThreeItems.length=10//报错

let rangeOfFourItems = FixedLengthRange(firstValue: 0, length: 4)
rangeOfThreeItems.firstValue=10//报错
```
### 延迟存储属性
延迟存储属性在知道访问时才会去计算.他必须是变量,因为他可能在实例化之后才能使用,而常量必须要在定义时给定值.  
当实例初始化值依赖于外部条件,而外部条件要等到实例初始化后才能知道的情况下很有用.对于需要使用大量计算才能获取到值得值得属性,而这个值只有在需要用到时才计算的情况下也很有帮助.  
下面这个例子避免初始化时的复杂操作
```swift
class DataImporter {
    /*
    这个类从外部导入大量数据,这些操作会耗费很长时间
     */
    var fileName = "data.txt"
    // 其他的操作,这里省略...
}

class DataManager {
    lazy var importer = DataImporter()
    var data = [String]()
    // 这个类需要使用导入数据实例
}

let manager = DataManager()
manager.data.append("Some data")
manager.data.append("Some more data")
//因为importer属性是延迟属性,所以这里初始化的时候并不会立刻去做数据导入操作,
//从而可以直接快速实例化.当用到importer时候再去实例化这个属性.这样可以提高效率.
```
### 计算属性
计算属性并不存储值,它提供`get`和可选的`set`,计算属性可以在 **类,结构体,枚举** 中使用.使用`set`时默认参数名为`newValue`我们可以自定义一个名字.
```swift
struct Point {
    var x = 0.0, y = 0.0
}
struct Size {
    var width = 0.0, height = 0.0
}
struct Rect {
    var origin = Point()
    var size = Size()
    var center: Point {
        get {
            let centerX = origin.x + (size.width / 2)
            let centerY = origin.y + (size.height / 2)
            return Point(x: centerX, y: centerY)
        }
        set(newCenter) {//自定义了newCenter代替newValue
            origin.x = newCenter.x - (size.width / 2)
            origin.y = newCenter.y - (size.height / 2)
        }
    }
}
var square = Rect(origin: Point(x: 0.0, y: 0.0), size: Size(width: 10.0, height: 10.0))
let initialSquareCenter = square.center
square.center = Point(x: 15.0, y: 15.0)
print("square.origin is now at (\(square.origin.x), \(square.origin.y))")
// Prints "square.origin is now at (10.0, 10.0)
```
### 只读计算属性
如果只有`get`没有`set`那么就是一个只读计算属性.对于只读属性可以简化,直接return.
```swift
struct Cuboid {
    var width = 0.0, height = 0.0, depth = 0.0
    var volume: Double {
        return width * height * depth
    }
}
let fourByFiveByTwo = Cuboid(width: 4.0, height: 5.0, depth: 2.0)
print("the volume of fourByFiveByTwo is \(fourByFiveByTwo.volume)")
// Prints "the volume of fourByFiveByTwo is 40.0
```
### 属性观察器
属性观察器可以设置在任何一个非延迟属性性.他用来监听属性值得变化并作出一些反馈.可以通过重写方式来给继承的属性添加观察器.对于非重写的计算属性,你不需要添加观察器,因为你可以在`set`里面进行操作.  
属性观察器有两个选择:
- `willSet`在值被保存之前调用
- `didSet`在值被保存之后调用

`willSet`默认常量参数名为`newValue`,newValue是新的值,他是即将要设置的值.`didSet`默认常量参数名为`oldValue`,oldValue是属性原来的值.参数名都可以自定义.
```swift
class StepCounter {
    var totalSteps: Int = 0 {
        willSet(newTotalSteps) {
            print("新的值为:\(newTotalSteps)")
        }
        didSet {
            print("原始值为:\(oldValue)")
        }
    }
}
var sc=StepCounter()
sc.totalSteps=10
//新的值为:10
//原始值为:0
```
### 全局变量和局部变量
计算属性和属性观察器都可以用于全局变量和局部变量.全局变量实在function, method, closure, or type context之外定义的变量,局部变量是在function, method, or closure context.内定义的变量.前几章的全局和局部变量,都是 *存储变量*.存储变量和存储属性一样都提供存储空间来并且允许读写.  
我们可以定义`计算变量`和并且给`存储变量`设置观察器

> 全局常量和变量都是延迟计算的,和延迟属性类似.只不过他们不需要显示使用`lazy`.局部变量永远都不会延迟计算的.

### 类型属性
实例属性属于实例,类型属性属于类型,无论创建多少个实例,这个属性只会有一个.所有实例共享.存储属性,常量,变量,计算变量都可作为实例属性.   
类型属性必须初始化.
### 类型属性定义
`static`来定义静态或者可变类型属性.对于计算属性可以使用`class`关键字,这样他就可以再子类中被重写.
```swift
struct SomeStructure {
    static var storedTypeProperty = "Some value."
    static var computedTypeProperty: Int {
        return 1
    }
}
enum SomeEnumeration {
    static var storedTypeProperty = "Some value."
    static var computedTypeProperty: Int {
        return 6
    }
}
class SomeClass {
  static var storedTypeProperty = "Some value."
    static var computedTypeProperty: Int {
        return 27
    }
    class var overrideableComputedTypeProperty: Int {
        return 107
    }
}
```
### 类型属性的访问
类型属性只能通过类型来访问.
```swift
struct AudioChannel {
    static let thresholdLevel = 10
    static var maxInputLevelForAllChannels = 0
    var currentLevel: Int = 0 {
        didSet {
            if currentLevel > AudioChannel.thresholdLevel {
                // cap the new audio level to the threshold level
                currentLevel = AudioChannel.thresholdLevel
            }
            if currentLevel > AudioChannel.maxInputLevelForAllChannels {
                // store this as the new overall maximum input level
                AudioChannel.maxInputLevelForAllChannels = currentLevel
            }
        }
    }
}
```
## 方法(Methods)
方法与函数定义方式一样.
### self属性
每个实例都有一个隐含属性`self`,他完全等于当前实例.可以再函数体内使用`self`来访问实例的属性等.但是`self`并非强制要求写.如果不写swift会假定当前变量是该实例的属性.当时当函数参数名称与属性名称一样时需要`self`来区分.
```swift
func increment() {
    self.count += 1
}
//不加self
func increment() {
    count += 1
}
```
### 修改值类型的属性值
枚举和结构体属于值类型,通常不可以直接修改他们的属性值.  
如果确实需要在方法中修改属性的值,那么需要定义方法为`mutating`,如果用`let`实例化的话, `mutating`方法不可调用,因为该实例的属性不可更改.
```swift
struct Point {
    var x = 0.0, y = 0.0
    mutating func moveBy(x deltaX: Double, y deltaY: Double) {
        x += deltaX
        y += deltaY
    }
}
var somePoint = Point(x: 1.0, y: 1.0)
somePoint.moveBy(x: 2.0, y: 3.0)
print("The point is now at (\(somePoint.x), \(somePoint.y))")
// Prints "The point is now at (3.0, 4.0)
```
### 在`mutating`方法中给self赋值
`mutating`方法中可以给self赋予一个完全新的值,上面的方法可以改写为:
```swift
struct Point {
    var x = 0.0, y = 0.0
    mutating func moveBy(x deltaX: Double, y deltaY: Double) {
        self = Point(x: x + deltaX, y: y + deltaY)
      }
}
```
枚举类型中的`mutating`也可以修改`self`
```swift
enum TriStateSwitch {
    case off, low, high
    mutating func next() {
        switch self {
        case .off:
            self = .low
        case .low:
            self = .high
        case .high:
            self = .off
        }
    }
}
var ovenLight = TriStateSwitch.low
ovenLight.next()
// ovenLight is now equal to .high
ovenLight.next()
// ovenLight is now equal to .off
```
### 类型方法
通过`static`可以定义类型方法,对于类可以用`class`,来定义类型防范这样子类可以重写它.在类型方法内部`self`指向的是类型本身而不是实例.
```swift
class SomeClass {
    class func someTypeMethod() {
        // type method implementation goes here
    }
}
SomeClass.someTypeMethod()
```
在类型方法内可以直接调用该类型的其他类型方法,而不需要该类型作为前缀.

## 下标(Subscripts)
类,枚举,结构体,都可以定义下标访问的快捷方式来访问集合中的元素.我们可以使用下标方式访问设置值,而不需要写独立的访问和设置方法.例如数组可以用 someArray[index]来访问元素,对于字典可以用someDictionary[key].   
可以定义多个下标方法,通过索引类型来进行重载.也可以自定义多个参数,来满足一些需求.
### 下标写法
`set`的默认参数名为`newValue`,对于只读下标不许要写`set`或者直接用`return`即可
```swift
subscript(index: Int) -> Int {
    get {
        // return an appropriate subscript value here
    }
    set(newValue) {
        // perform a suitable setting action here
    }
}

struct TimesTable {
    let multiplier: Int
    subscript(index: Int) -> Int {
        return multiplier * index
    }
}
let threeTimesTable = TimesTable(multiplier: 3)
print("six times three is \(threeTimesTable[6])")
// Prints "six times three is 18
```
### 下标选项
下标方法可以接受任意多个参数.这些参数可以是任意类型的.这个方法的返回值也可以是任意类型.但是不可以使用`in-out`参数,而且参数也不可以有默认值.

## 继承(Inheritance)
### 重写
子类可以覆盖掉父类的实例方法,类方法,实例属性,下标方法.通过`override`重写.在重写的函数中调用父类的函数通过`super`.    
可以再子类中给父类的属性重写观察器.
```swift
class AutomaticCar: Car {
    override var currentSpeed: Double {
        didSet {
            gear = Int(currentSpeed / 10.0) + 1
        }
    }
}
```
重写属性的Getters和Setters
```swift
class Car: Vehicle {
    var gear = 1
    override var description: String {
        return super.description + " in gear \(gear)"
    }
}
```
### 防止重写
如果不希望被子类重写,需要添加`final`例如`final var, final func, final class func, and final subscript`

## 构造函数(Initialization)
### 给存储属性设置初始值
类和结构体在初始化时必须为所有的存储属性设置初始值.
#### 构造函数
没有参数的`init()`.可以在构造函数中给定值,也可以给定在变量声明时默认值
```swift
struct Fahrenheit {
    var temperature: Double
    init() {
        temperature = 32.0
    }
}
var f = Fahrenheit()
print("The default temperature is \(f.temperature)° Fahrenheit")
// Prints "The default temperature is 32.0° Fahrenheit
```
### 自定义构造函数
构造函数与普通函数类似，可以提供参数，也可以无参数。默认情况下swift会给参数一个默认label，也可以自定义label，与普通函数label一样。`_`表示调用时不需要传递`label`。
```swift
struct Celsius {
    var temperatureInCelsius: Double
    init(fromFahrenheit fahrenheit: Double) {
        temperatureInCelsius = (fahrenheit - 32.0) / 1.8
    }
    init(fromKelvin kelvin: Double) {
        temperatureInCelsius = kelvin - 273.15
    }
}
let boilingPointOfWater = Celsius(fromFahrenheit: 212.0)
// boilingPointOfWater.temperatureInCelsius is 100.0
let freezingPointOfWater = Celsius(fromKelvin: 273.15)
// freezingPointOfWater.temperatureInCelsius is 0.0
```
### Optional属性
如果属性在定义时不确定有值，或者在运行当中可能会不存在值，那么可以设置为`Optional`，他不需要在构造时赋值。
```swift
class SurveyQuestion {
    var text: String
    var response: String?
    init(text: String) {
        self.text = text
    }
    func ask() {
        print(text)
    }
}
let cheeseQuestion = SurveyQuestion(text: "Do you like cheese?")
cheeseQuestion.ask()
// Prints "Do you like cheese?"
cheeseQuestion.response = "Yes, I do like cheese.
```
### 构造时给常量属性赋值
在构造函数中给常量属性赋值，一旦赋值后，这个属性的值就不可再修改
```swift
class SurveyQuestion {
    let text: String
    var response: String?
    init(text: String) {
        self.text = text
    }
    func ask() {
        print(text)
    }
}
let beetsQuestion = SurveyQuestion(text: "How about beets?")
beetsQuestion.ask()
// Prints "How about beets?"
beetsQuestion.response = "I also like beets. (But not with cheese.)"
```
### 默认构造函数
如果没有提供自定义构造函数时，swift会提供一个不带任何参数的构造函数。这种情况下必须确保声明变量时已经赋值（除了`Optional`类型）。但是对于结构体类型，构造函数包含了所有属性参数。
```swift
class ShoppingListItem {
    var name: String?
    var quantity = 1
    var purchased = false
}
var item = ShoppingListItem()
```
### 代理构造函数
构造函数内可以调用其他构造函数，来初始化一些变量，从而达到代码复用。
### 构造函数的继承和重写
swift中父类的构造函数不会默认被子类继承。


## 析构函数(Deinitialization)
## 自动引用计数(Automatic Reference Counting)
## 可选链(Optional Chaining)
## 错误处理(Error Handling)
## 类型转换(Type Casting)
## 嵌套类型(Nested Types)
## 扩展(Extensions)
## 协议(Protocols)
## 泛型(Generics)
## 访问控制(Access Control)
## 高级运算符(Advanced Operators)
