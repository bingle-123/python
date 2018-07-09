# [swift编程](http://shop.oreilly.com/product/9781785887512.do)
var 定义变量，语句末尾不需要添加";",  
一次性定义多个变量，可以忽略var。var a=10,b=20  
var pi:Any? `Any`表示这个变量可以是任意类型，`？`表示可以暂时不给初始化值  
pi=3.14  
`is` 可以判断一个变量的类型  
pi is Int //false  
pi is Double //true  
`swfit中不同类型变量是不可以直接操作的,必须强制转换为统一类型`
## 类型
### 数值类型
Int,Float,Double,Decimal,Binary,Octal,Hexadecimal  
```swift
var three = 3
var threePointOne = 3.1
three + threePointOne //这里会报错因为两个类型不一致
Double(three)+threePointOne //正确
```
#### 将变量转换为String
“Message was legit: \(message)” `\()`可以将变量拼接到String中，`()`中的内容是可以计算的: `“2 + 2 is \(2 + 2)”`  
如果用 `“2 + 2 is ” + (2 + 2)`会报错，因为没有String和Int类型，所以需要转换类型：`“2 + 2 is ” + String(2 + 2)`  
#### 可选变量
如果一个变量加了"?"那么这个变量类型会变成类似Optional,表示这个变量可能包涵值也可能是nil,
如果你确认一个这个对象有值得话可以用`!`将他取出。使用Optional原因有多个，首先：我们保证这个变量在后面会被赋值，例如class实例。
```swift
var hasSomething:String?="hey there"
hasSomething! //hey there
print(hasSomething)//"Optional("hey there")\n"

if let message=hasSomething{
    "message was legit: \(message)"
}else{
    "there was no message"
}
```
`!`可以让Optional对象自动解析，但是他和普通变量定义有什么区别呢：  
普通类型变量我们需要在初始化的时候赋值给他。有时候我们不知道初始化值，但是我们确定在后面会给这个变量赋值。
```swift
var hasSomething:String!="hey there"
hasSomething //hey there
print(hasSomething)//hey there
//-----------------------------------
class SomeUIView:UIView {
       @IBOutlet var someButton:UIButton!
       var buttonWidth:CGFloat!
       override func awakeFromNib() {
           self.buttonOriginalWidth = self.button.frame.size.width
}}
//这段代码中我们没办法直接给someButton初始化值，因为他只能运行中的其它函数赋值。
```
### 元祖
`let purchaseEndpoint = (“buy”,“POST”,”/buy/”)`,元祖中元素的类型可以随意，`let purchaseEndpoint = (“buy”,“POST”,”/buy/”,true)`,访问元素的方法:
```swift
purchaseEndpoint.1 // “POST”
purchaseEndpoint.2 // “/buy/”
```
元祖中的元素也可以命名，这样就可以通过名称访问元素，而不仅仅是下标
```swift
 let purchaseEndpoint = (name: “buy”, httpMethod: “POST”,URL:“/buy/”,useAuth:true)
 purchaseEndpoint.httpMethod = “POST”
```
从元祖中一次性取出所有值，赋给变量`let (purchaseName, purchaseMethod, purchaseURL, _) = purchaseEndpoint`,`_`表示忽略这个位置的元素
## 流程控制
### 循环
#### 普通循环
`for initialization; conditional expression; increment { statement }`,循环通常是这样。  
循环内定义的变量只在循环内可见，如果要读取循环内变量，这个变量必须在进入循环之前定义。
#### for in
```swift
for i in 1...4{
    print("\(i)")
}
```
`1...4` 表示1234。也可以使用`1..<4`表示123
如果不需要使用`i`可以用`_`代替
```swift
for _ in 1...4{
    print("hello")
}
```
我们可以用for in 循环一个数组
```swift
class Tire { var air = 0 }
var tires = [Tire]()
for _ in 1...4 {
   tires.append(Tire())
}
print("We have \(tires.count) tires")
for tire in tires {
   tire.air = 100
   print("This tire is filled \(tire.air)%")
}
print("All tires have been filled to 100%")
```
循环其它对象，例如字符串
```swift
for char in “abcdefghijklmnopqrstuvwxyz”.characters {
       print(char)
}
   // a
   // b
   // c
   // etc....
```
有时候我们会通过获取数组长度来进行循环，并根据下表获取数组元素。但是数组提供了一个方法`enumerate`，可以同时读取下标与元素。
```swift
let numbers = ["zero", "one", "two", "three", "four"]
for (i, numberString) in numbers.enumerate() {
       print("Number at index \(i) is \(numberString)")
}
```
swift也支持`while`和`do-while`
### 条件语句
#### if-else
只能接受Bool做为条件,所以任何非`true`和`false`都需要强制`Bool()`转换。
`!`,`&&`,`||`
#### switch
switch 必须包涵default。一旦匹配后将不再往下执行，因为`自动添加了break`
```swift
var num = 5
switch num {
    case 2:print(“It’s two”)
    case 3:print(“It’s three”)
    default:print(“It’s something else”)
}
```
case 条件也可以是`n...m`
```swift
var num = 5
switch num {
    // including 2,3,4,5,6
    case 2...6:print(“num is between 2 and 6”)
    default:print(“None of the above”)
}
```
case 提交还可以是元祖解析
```swift
var geo = (2,4)
switch geo {
    //(anything, 5)
    case (_,5):print(“It’s (Something,5)”)
    case (5,_):print(“It’s (5,Something)”)
    case (1...3,_):print(“It’s (1 or 2 or 3, Something)”)
    case (1...3,3...6):print(“This would have matched but Swift already found a match”)
    default:print(“It’s something else”)
}
```
## 数组
数组定义:`var myFirstArray:Array<Int> = Array<Int>()`这表示数组中的元素都是Int类型，如果想要不同类型可以使用`var mixedArray:[AnyObject] = [1,"hi",3.0,Float(4)]`  
也可以快速定义Int数组：`var quickerArray = [Int]()`或者`var arrayOfInts = [1,2,3,4]`  
### swift中存在可变数组和不可变数组：  
`var mutableArray = [1,2,3,4,5]`可变  
`let immutableArray = [1,2,3,4,5]`不可变
### 数组方法
var raining = ["cats"]
raining.insert("dogs",atIndex: 0)
raining.removeLast()
raining.removeAtIndex(1)
raining+= [“dogs”,“pigs”,“wolves”]
## 字典
字典与数组一样，元素类型一致。
```swift
var people:Dictionary<Int,String> = [186574663:“John Smith”,
                                        198364775:“Francis Green”,
                                        176354888:“Trevor Kalan”]
people[176354888] // “Trevor Kalan”
//或者这么定义
var people = [186574663:“John Smith”,
              198364775:“Francis Green”,
              176354888:“Trevor Kalan”]
```
`字典返回的是optional类型`因为你想访问的数据有可能不存在，如果你确定数据存在，可以用`!`：`people[176354888]! // “Trevor Kalan”`  
### 给键设置值  
`people[384958338] = “Skip Wilson”`  
如果字典不包含这个键，就创建，如果包涵就更新该建  
### 删除键
`people[384958338] = nil` 或者  
`people.removeValueForKey(176354888)`如果改建存在值，就删除该键并返回值。如果没有该键，就返回nil。
### 循环字典
```swift
for (ssn,name) in people {
   print(“SSN: \(ssn) Name: \(name)”)
}
// SSN: 198364775 Name: Francis Green
// SSN: 176354888 Name: Trevor Kalan
// SSN: 186574663 Name: John Smith
//循环键
for ssn in people.keys {
   print(“SSN: \(ssn)”)
}
//循环值
for name in people.values {
   print(“Name: \(name)”)
}
```
### 方法属性
count可以返回键值对数量  
people=[:]可以直接清空字典
## 函数
函数包涵3个部分：函数名，参数，返回类型
```swift
func functionName(parameterName: parameterType) -> returnType { //code
}
//例如
func sayhello(){
    print("hello")
}
sayhello()
//例如
func sayHello(name: String) {
     print(“Hello, \(name)!”)
}
//例如
func sayHello(name: String, numberOfTimes: Int) {
     for _ in 1...numberOfTimes {
       sayHello(name)
     }
}
sayHello("your name",numberOfTimes:5)
```
`上面的函数相当于只有一个参数，然后用","将参数分离`
> 貌似函数第一个参数都不能带参数名，原因暂时没发现

### 返回类型
```swift
func sum(a: Int, b: Int) -> Int {
     return a + b
}
```
这里表示函数接受两个参数，然后返回Int类型的值。
#### 返回多个值
swift只能返回一个值，但是我们可以让他返回一个元祖
```swift
func sumAndCeiling(a: Int, b: Int) -> (Int, Int) {
       let ceiling = a > b ? a : b
       let sum = a + b
       return (sum, ceiling)
}
let result = sumAndCeiling(4, b: 52)
let sum = result.0
let ceiling = result.1
print(sum)
print(ceiling)
```
我们知道元祖内元素是可以命名的，因为有的时候我们可能不知到元祖元素的顺序，但是我们知道每个元素的名字，这样我们就可以通过名字来获取元素，而且避免顺序带来的问题
```swift
func sumAndCeiling(a: Int, b: Int) -> (sum: Int, ceiling: Int) {
       let ceiling = a > b ? a : b
       let sum = a + b
       return (sum, ceiling)
}
let result = sumAndCeiling(4, b: 52)
let sum = result.sum
let ceiling = result.ceiling
print(sum)
print(ceiling)
```
### 函数参数
- 外部参数
- 默认参数值
- 可变参数
- In－Out参数
- 函数做为参数
#### 外部参数
有时当你调用一个函数将每个参数进行命名是非常有用的，以表明你传递给函数的每个参数的目的。  
如果你希望用户函数调用你的函数时提供参数名称,除了设置本地地的参数名称，也要为每个参数定义外部参数名称。你写一个外部参数名称在它所支持的本地参数名称之前,之间用一个空格来分隔：
```swift
func introduce(nameOfPersonOne nameOne: String, nameOfPersonTwo nameTwo:
   String) {
       print(“Hi \(nameOne), I’d like you to meet \(nameTwo).”)
}
introduce(nameOfPersonOne: “John”, nameOfPersonTwo: “Joe”)
// Hi John, I’d like you to meet Joe.
```
`如果为参数提供一个外部参数名称，调用该函数时外部名称必须始终被使用。`
> 外部参数名不是必须的，但是他可以增强可读性....

#### 默认值
如果参数被设置默认值，那么他必须使用外部名。如果你不想给默认参数传递值，可以用`_`做为外部名称。
```swift
func addPunctuation(sentence sentence: String, punctuation: String = “.”) ->String {
    return sentence + punctuation
}
```
#### 可变参数
有时候我们需要传递不定数量的参数给函数，这里就需要用`...`
```swift
func average(numbers numbers: Int...) -> Int {
       var total = 0
       for n in numbers {
           total += n
       }
    return total / numbers.count
}
print(average(numbers:1,2,3,4,5))
```
对于可变参数，必须使用`,`将参数分割。有时候你有一个Int数组像传递进去，可以使用数组做为参数类型：
```swift
func average(numbers: [Int]) -> Int {
       var total = 0
       for n in numbers {
           total += n
        }
    return total / numbers.count
}
```
#### 常量参数与变量参数
```swift
func test(a:Int,b:Int){
    a=10
}
test(10,b:20)
//error: cannot assign to value: 'a' is a 'let' constant
```
默认情况下，函数参数都是常量参数，在函数内部改变其值，是会报错的。如果想改变参数值，就必须使用变量参数：
```swift
func test(var a:Int,b:Int){
    a=10
}
test(20,b:20)
```
#### 输入输出参数
有时候我们希望在函数内部改变函数外部变量的值,可以用inout关键字，调用函数是参数必须带上`&`。
```swift
func incrementNumber(inout number number: Int, increment: Int = 1) {
       number += increment
}
var totalPoints = 0
incrementNumber(number: &totalPoints)
```
### 函数类型
swift函数是一种类型，所以他可以传递给变量，当做参数等等。通常函数类型为：`(parameterTypes) -> ReturnType`
```swift
func double(num: Int) -> Int {
       return num * 2
}
//double 类型为(Int)->Int
var myFunc:(Int) -> Int = double
//将double赋值给myFunc

func modifyInt(number number: Int, modifier:(Int) -> Int) -> Int {
       return modifier(number)
}
```
## Enum
```swift
enum Suit{
    case Hearts
    case Clubs
    case Diamonds
    case Spades
}
```
这里定义了四个枚举成员变量，case表示这一行定义一个变量。  
可以在一行定义多个成员
```swift
enum Suit{
    case Hearts, Clubs, Diamonds, Spades
}
```
每个枚举的定义都是定义一个全新的类型，与Int等类似。如果某个变量被赋值为枚举类型，那么可以直接`.`来设置他的值。
```swift
enum CompassPoint {
    case North
    case South
    case East
    case West
}
var directionToHead = CompassPoint.West
directionToHead = .South
switch directionToHead {
    case .North:
        print("Lots of planets have a north")
    case .South:
        print("Watch out for penguins")
    case .East:
        print("Where the sun rises")
    case .West:
        print("Where the skies are blue")
}
// 输出"Watch out for penguins”
```
## Struct和class
### 类和结构体对比
#### 共同点
- 定义属性用于储存值
- 定义方法用于提供功能
- 定义下标用于通过下标语法访问值
- 定义初始化器用于生成初始化值
- 通过扩展以增加默认实现的功能
- 符合协议以对某类提供标准功能
#### class独有特点
- 继承允许一个类继承另一个类的特征
- 类型转换允许在运行时检查和解释一个类实例的类型
- 取消初始化器允许一个类实例释放任何其所被分配的资源
- 引用计数允许对一个类的多次引用
### 定义
定义方式相似
```swift
class SomeClass {
    // class definition goes here
}
struct SomeStructure {
    // structure definition goes here
}
struct Resolution {
    var width = 0
    var heigth = 0
}
class VideoMode {
    var resolution = Resolution()
    var interlaced = false
    var frameRate = 0.0
    var name: String?
}
```
### 实例
```swift
let someResolution = Resolution()
let someVideoMode = VideoMode()
```
### 属性访问
```swift
someVideoMode.resolution.width = 12880
```
### 初始化
```swift
//struct
let vga = resolution（width:640, heigth: 480）
var cinema = vga
```
`因为struct和enum都是值类型，所以这里的cinema＝hd，不是同一个实例，只是她们的值相同，也就是修改vga不会影响cinema`  
类的实例是引用类型，如果多个变量引用同一个实例，那么`===` 操作时返回true。但是这对与struct或者enum不会成立，因为她们是值类型，每次都是拷贝一份  
`swift建议新建struct对象时传递初始化值，并且定义的时候加上默认值`   
### 可变性
如果在struct内部的函数会改变struct内部变量，那么这个函数必须定义为`mutating`
```swift
struct someStruct {
    var property1 = “Hi there”
    func method1() {
       property1 = “Hello there”
       // property1 belongs to the class itself
       // so we can’t change this with making some changes
    }
    // ERROR: cannot assign to ‘property1’ in ‘self’
}
//因为property1是属于someStruct的一个实例
struct someStruct {
    var property1 = “Hi there”
    mutating func method1() {
               property1 = “Hello there”
    }
    // does not throw an error! YAY
}
```
## Class
```swift
class Car {
       let make = “Ford”
       let model = “Taurus”
       let year = 2014
}
//下面定义会出错 error: class ‘Car’ has no initializers
class Car {
       let make:String
       let model:String
       let year:Int
}
```
在struct中可以不给变量初始化值，在class中如果属性没有初始化值，那么必须定义一个init()函数来初始化，swift中没有提供默认的init()
### 初始化
初始化函数中定义所有为给默认值的属性，可以调用函数。。
```swift
 struct GeoPoint {
       var lat:Double
       var long:Double
       init() {
           lat = 32.23232
           long = 23.3434343
       }
}
```
`函数名重复 貌似C，参数不同`
```swift
struct GeoPoint {
        var x = 0.0
        var y = 0.0
        var length = 0.0
        init() {}
        init(x:Double,y:Double) {
            self.x = x
            self.y = y
        }
        init(length:Double) {
             self.length = length
        }
}
var regularPoint = GeoPoint()
var pointWithSize = GeoPoint(x: 2.0, y: 2.0)
var otherPoint = GeoPoint(length: 5.4)
```
### 属性观察器
swift提供了两个功能，`willSet`,`disSet`。willSet会在属性赋值之前调用，didSet会在属性赋值之后调用
```swift
class VideoMode {
    var interlaced = false
    var frameRate = 0.0
    var name: String?="init"{
        willSet(newName){
            print("before set \(newName)")
        }
        didSet(oldName){
            print("after set \(oldName)")
        }
    }
}
var  vm=VideoMode()
vm.name="test name"
// before set test name
// after set init
```
### 函数
swift有三种访问控制
- private:只能在源文件内被访问
- internal:在目标定义的任何地方都可以访问
- public:公开
默认函数是internal
#### 类函数
```swift
class Car {
    var name = “Ford”
    var distance = 0
    class func getCarVersion() -> String {
       return “5.0.1”
    }
}
var car1 = Car()
print(car1.distance)
Car.getCarVersion()
```
### 继承
```swift
class Animal {
    var name:String
    var numberOfLegs:Int
    func move() -> String{
       return “\(name) is moving.”
    }
    init(name:String,numberOfLegs:Int) {
       self.name = name
       self.numberOfLegs = numberOfLegs
    }
}
class Dog:Animal {
    var breed:String
    override func move() -> String {
       return “\(name) the \(breed) is moving.”
    }
    init(name: String, numberOfLegs: Int,breed:String) {
       self.breed = breed
       super.init(name: name, numberOfLegs: numberOfLegs)
    }
}
class Bichon:Dog {
    var fluffynessLevel:Double
    init(name: String, numberOfLegs: Int, breed: String,
        fluffynessLevel:Double) {
        self.fluffynessLevel = fluffynessLevel
        super.init(name: name, numberOfLegs: numberOfLegs, breed: breed)
    }
}
var penny = Bichon(name: “Penny”, numberOfLegs: 4, breed: “Bichon”,
  fluffynessLevel: 100.1)
penny.move() // “Penny the Bichon Frise is moving.”
```
