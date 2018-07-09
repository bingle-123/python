# [iOS.9.Programming.Fundamentals.with.Swift]()
## The architecture of swift
### 所有东西都是对象(类似于python)
数值也是对象例如数字‘1’ 1.successor()。  
验证一个东西是否是对象，可以试试能不能修改它。在swift中对象类型是extended，例如在Int对象上增加一个函数：
```swift
extension Int {
    func sayHello() {
       print("Hello, I'm \(self)")
    }
}
1.sayHello() // outputs: "Hello, I'm 1"
```
swift中有三种对象类型：class ，struct(例如数值1)，enum  
swift中所有变量必须预先定义，有两种定义变量方式:var,let。let定义不可变变量，var定义可变变量
### 文件结构
#### Module
module比文件级别高，module可以有无数个文件组成，module内的文件完全可以互相访问，但是module必须通过`import`才能访问其它module。例如:import UIkit。  
#### 变量定义
在文件顶部定义的变量，是全局变量，会在程序运行期间一支存在。
#### 函数定义
顶部定义的函数是全局函数，所有的代码都可以访问它们。
#### 对象类型定义
class,struct,enum的定义
### 作用域和生命周期
swift作用域控制访问，以及生命周期。
- module
- file
- object
- 花括号
#### 私有化
private var name:String?="test"

## Functions
有3种方式，让函数不用return
- func say1(s:String) -> Void { print(s) }
- func say2(s:String) -> () { print(s) }这里的()因为函数是可以返回元祖的
- func say3(s:String) { print(s) }
函数对象 ()->()
### 外部参数名
函数的参数可以有一个外部参数名，它可以被当做label来使用。
```swift
//内部名和外部名一致
func repeatString(s:String, times:Int) -> String {
    var result = ""
    for _ in 1...times { result += s }
    return result
}
let s = repeatString("hi", times:3)
//内部名和外部名不同
func repeatString(s:String, times n:Int) -> String {
    var result = ""
    for _ in 1...n { result += s}
    return result
}
```
上面的函数，第一个参数只有内部名称，第二个参数的外部名和内部名都是times。  
`第一个函数没有默认外部名`because the function name usually clarifies sufficiently what the first parameter is for.  
`func say(s:String, _ times:Int){}`如果用`_`代替外部名，那么传参数时可以不用`external_name:value`而是`say("woof", 3)`
### 重载
swift允许函数名一致，只要他们的参数或返回值不同就行。  
但是需要注意的是，如果参数一致，返回不一致，那么在调用函数时swift可能不知道调用哪一个，所以不许确认返回值和当前调用的上下文一致，例如：
```swift

func say() -> String {
   return "one"
}
func say() -> Int {
    return 1
}
//如果想成功调用say()
let s:String=say() //s="one"
let ss=say()+" two"//ss="one two"
let m:Int=say()//m=1
let mm=say()+2//m=3
```
### 参数默认值
```swift
func say(s:String, times:Int = 1) {
    for _ in 1...times {
        print(s)
    }
}
```
### 不确定数量参数
如果接受的参数属于统一类型，并且数量不固定，那么用`...`，调用时用`,`分隔参数。
```swift
func sayStrings(arrayOfStrings:String...) {
       for s in arrayOfStrings { print(s) }
}
```
### 被忽略参数(不知道这是虾米玩意)
### 可被修改的参数
默认情况下函数的参数十一`let`定义的，也就是说他的值是不可改变的。如果希望在函数内部修改参数的值，那么参数需要用`var`定义。  
swift没有`指针概念`，如果想要修改对应参数的原始值，那么需要使用`inout`来定义参数：`func removeFromString(inout s:String, character c:Character) -> Int`,调用函数时参数需要带上`&`：removeFromString(&s,character:Character("l"))，参数定义应该是`var`
> 如果传递的是一个class实例，那么不用inout就可以直接修改该参数。所以这也是一种方法

### 函数内的函数
函数可以定义在任何地方，函数可以返回一个函数(类似于装饰器)。
### 递归
```swift
func countDownFrom(ix:Int) {
    print(ix)
    if ix > 0 { // stopper
        countDownFrom(ix-1) // recurse!
    }
}
```
### 函数做为参数
```swift
func doThis(f:()->()) {
    f()
}
```
### 匿名函数
```swift
print(
    {
        () -> String in
        return "hello"
    }()
)
//
{
    () -> () in
    self.myButton.frame.origin.y += 20
}
{
    (finished:Bool) -> () in
    print("finished: \(finished)")
}
//
UIView.animateWithDuration(0.4,
    animations: {
       () -> () in
       self.myButton.frame.origin.y += 20
       },
    completion: {
           (finished:Bool) -> () in
           print("finished: \(finished)")
}
)
```

### 闭包
闭包值得是函数可以访问，函数外的变量
```swift
var s=10
func test(){
    print(s)
}
```
## 变量和简单类型
1.全局变量
2.属性
- 对象属性
- class/static属性 用static或者class定义
3.本地变量：函数内部变量
### 变量以计算方式初始化
```swift
var val=1
let timed : Bool = {
       if val == 1 {
           return true
       } else {
           return false
       }
}()
```
### 被计算变量
变量不是直接定义值，而是跟随一个函数,变量必须定义为`var`变量类型必须带上
get会在取值时调用,返回值必须与变量类型一致,  
set会在赋值时调用,他会默认接收一个参数newValue,也可以用其他名字`set(val){}`
不一定一定要有set,如果没有set的话变量是只读的
```swift
var now : String {
       get {
           return NSDate().description
       }
       set {
           print(newValue)
    }
}
//
var now : String {
    return NSDate().description
}
```

### 变量观察者(有点意思)
变量赋值有两个会触发两个函数`willSet`,`didSet`,变量必须是`var`  
默认情况下`willSet`接受`newValue`参数,也可以自定义一个名字`willSet(newVal)`,
`didSet`接受一个'oldValue'参数,也可以自定义`didSet(oldVal)`
```swift
var s = "whatever" {
    willSet {
        print(newValue)
    }
    didSet {
        print(oldValue)
        // self.s = "something else"
    }
}

class Test{
    var name:String

    var street:String{
        willSet{
            print(self.test)
        }
        didSet{
            print(self.test)
        }
    }
    init(_ name:String,_ street:String) {
      self.name=name
      self.street=street
    }
}
var test:Test=Test("name","test"){
    willSet{
        print(test.street)
    }
    didSet{
        print(test.street)
    }
}
test.street="new name"
//这里不会触发test的事件,但是会触发Test.street事件
```
### 惰性初始化
有三种惰性初始化变量
- 全局变量:全局变量默认就是惰性初始化,当代码访问到他时才会初始化
- 静态属性:跟全局变量一样
- 对象属性:对象属性默认不是惰性初始化,用`lazy`标签定义,并且必须为`var`,当被访问是他才会初始化
惰性初始化经常被用于单例模式
```swift
class MyClass {
    static let sharedMyClassSingleton = MyClass()
}
```
## 内置简单类型
`Bool`,`Numbers:Int Double`,`String`,`Character:String.characters`,`Range`,`Tuple`,`Optional`
### Range
- `...`:a...b表示从a到b包含b
- `..<`:a..<b 不包含b
```swift
let r = 1...3
let r = -1000...(-1) //最后一个是负数必须用`()`
//用于for循环
for ix in 1... 3 {
    print(ix) // 1, then 2, then 3
}

let ix = 4// ... an Int...
if (1...3).contains(ix) {} // 检查是否包含ix

let s = "hello"
let arr = Array(s.characters)
let result = arr[1...3]
let s2 = String(result) // "ell"
```
### 元祖
```swift
var pair : (Int, String)
var pair : (Int, String) = (1, "One")
var (ix, s) = (1, "One")
let pair = (1, "One")
//解析
let (_, s) = pair // now s is "One"

//元祖元祖定义名字
let pair : (first:Int, second:String) = (1, "One")
let pair = (first:1, second:"One")
var pair = (first:1, second:"One")
let x = pair.first // 1
pair.first = 2
let y = pair.0 // 2
```
### Optional
如果一个变量被赋值为`Optional类型`,那么在此给他赋值时必须使用同一类型的Optional,
```swift
var stringMaybe = Optional("howdy")
stringMaybe=Optional("test")//都是字符串Optional
stringMaybe="test2"//这里的stringMaybe认识Optional("test2"),自动进行了转换
stringMaybe=Optional(123)//出错
//另一种定义方式
var stringMaybe?
var stringMaybe?="test"
//函数参数也可以是Optional
func optionalExpecter(s:String?) {}
```
解析Optional
```swift
var stringMaybe = Optional("howdy")
print(stringMaybe!)//打印howdy而不是Optional("howdy")
```
如果optional类型没有赋值的话它的值是nil
```swift
var stringMaybe : String? = "Howdy"
print(stringMaybe) // Optional("Howdy")
if stringMaybe == nil {
   print("it is empty") // does not print
}
stringMaybe = nil
print(stringMaybe) // nil
if stringMaybe == nil {
   print("it is empty") // prints
}
```
*Optional的比较,如果optional不是nil那么会自动解析出值进行比较*

## 对象类型
### 对象类型定义方式
```swift
class Manny {}
struct Moe {}
enum Jack {}
```
对象类型内部可以定义:
- 初始化器:初始化器用来生成对象实例,初始化器是一个特殊的函数
- 属性:在对象定义的顶部,默认情况下作为实例的属性;属性可以是static/class,对于enum和struct可以用static来定义,对于class用class来定义;这两个特殊属性可以直接用对象类型来访问.他们只有一个值,所有的对象实例共享.
- 函数:跟属性类似,也有static/class.
- 下标:下标是一个特殊的函数,当用[]访问时调用
#### 初始化器
```swift
class Dog {
    var name = ""
    var license = 0
    init(name:String) {
        self.name = name
    }
    init(license:Int) {
        self.license = license
    }
    init(name:String, license:Int) {
        self.name = name
        self.license = license
    }
}
//三个不同的构造函数,依据传递的参数类型不同
```
如果构造函数返回`nil`表示生成实例失败,构造函数后面跟随`!`;这样放回的是一个Dog()!如果生成了实例,那么会自动解析出实例,否则就是nil.
```swift
class Dog {
    let name : String
    let license : Int
    init!(name:String, license:Int) {
        self.name = name
        self.license = license
        if name.isEmpty {
            return nil }
        if license <= 0 {
           return nil
        }           
    }
}
```
#### 属性
```swift
class Moi {
    let first = "Matt"
    let last = "Neuburg"
    let whole = self.first + " " + self.last // compile error
}
class Moi {
    let first = "Matt"
    let last = "Neuburg"
    var whole : String {
       return self.first + " " + self.last
    }
}
class Moi {
    let first = "Matt"
    let last = "Neuburg"
    lazy var whole : String = self.first + " " + self.last
}
```
#### 下标

```swift
struct Digit {
    var number : Int
    init(_ n:Int) {
        self.number = n
    }
    subscript(ix:Int) -> Int {
        get {
           let s = String(self.number)
           return Int(String(s[s.startIndex.advancedBy(ix)]))!
        }
    }   
}
var d = Digit(1234)
let aDigit = d[1] // 2
//set函数
struct Digit {
    var number : Int
    init(_ n:Int) {
       self.number = n
    }
    subscript(ix:Int) -> Int {
        get {
           let s = String(self.number)
           return Int(String(s[s.startIndex.advancedBy(ix)]))!
        }
        set {
           var s = String(self.number)
           let i = s.startIndex.advancedBy(ix)
           s.replaceRange(i...i, with: String(newValue))
           self.number = Int(s)!
        }
    }
}
var d = Digit(1234)
d[0] = 2 // now d.number is 2234
```
#### 内部类型定义
需要通过类型名称才能访问到内部类型
```swift
class Dog {
    struct Noise {
        static var noise = "Woof"
    }
    func bark() {
        print(Dog.Noise.noise)
    }
}
Dog.Noise.noise = "Arf"
```
### Enum
enum类似于一个已知状态的集合,集合中任意一个元素独立
```swift
enum Filter {
    case Albums
    case Playlists
    case Podcasts
    case Books
}
let type = Filter.Albums
//如果确认变量的类型可以省略Enum名称直接用`.`
let type : Filter = .Albums
//如果确认函数的参数类型也是enum那么传参数时也可以省略enum名称
func filterExpecter(type:Filter) {}
filterExpecter(.Albums)
```
#### 给固定值
固定值通过`.rawValue`获取
```swift
//这里Mannie=0,Moe=1,....
enum PepBoy : Int {
    case Mannie
    case Moe
    case Jack
}
//这里Albums="Albums",Playlists="Playlists",....
enum Filter : String {
    case Albums
    case Playlists
    case Podcasts
    case Books
}
//也可以自己赋值
enum Filter : String {
    case Albums = "Albums"
    case Playlists = "Playlists"
    case Podcasts = "Podcasts"
    case Books = "Audiobooks"
}
let type = Filter.Albums
print(type.rawValue) // Albums

//除了给固定值,还可以给函数等..
enum Error {
    case Number(Int)
    case Message(String)
    case Fatal(n:Int, s:String)
}
let err : Error = .Fatal(n:-12, s:"Oh the horror")
//特殊赋值
let fatalMaker = Error.Fatal
let err = fatalMaker(n:-1000, s:"Unbelievably bad error")

```
#### Enum构造器
```swift
enum Filter : String {
    case Albums = "Albums"
    case Playlists = "Playlists"
    case Podcasts = "Podcasts"
    case Books = "Audiobooks"
    static var cases : [Filter] = [Albums, Playlists, Podcasts, Books]
    init(_ ix:Int) {
       self = Filter.cases[ix]
    }
}
let type1 = Filter.Albums
let type2 = Filter(rawValue:"Playlists")!
let type3 = Filter(2) // .Podcasts
//要判断range范围是否合法
enum Filter : String {
    case Albums = "Albums"
    case Playlists = "Playlists"
    case Podcasts = "Podcasts"
    case Books = "Audiobooks"
    static var cases : [Filter] = [Albums, Playlists, Podcasts, Books]
    init!(_ ix:Int) {
       if !(0...3).contains(ix) {
           return nil
        }
       self = Filter.cases[ix]
    }
}
```
#### 函数
如果函数需要改变自己的值那么需要加上`mutating`
```swift
enum ShapeMaker {
    case Rectangle
    case Ellipse
    case Diamond
    func drawShape (p: CGMutablePath, inRect r : CGRect) -> () {
        switch self {
            case Rectangle: CGPathAddRect(p, nil, r)
            case Ellipse: CGPathAddEllipseInRect(p, nil, r)
            case Diamond:
               CGPathMoveToPoint(p, nil, r.minX, r.midY)
               CGPathAddLineToPoint(p, nil, r.midX, r.minY)
               CGPathAddLineToPoint(p, nil, r.maxX, r.midY)
               CGPathAddLineToPoint(p, nil, r.midX, r.maxY)
               CGPathCloseSubpath(p)
        }
    }
}
//
enum Filter : String {
    case Albums = "Albums"
    case Playlists = "Playlists"
    case Podcasts = "Podcasts"
    case Books = "Audiobooks"
    static var cases : [Filter] = [Albums, Playlists, Podcasts, Books]
    mutating func advance() {
        var ix = Filter.cases.indexOf(self)!
        ix = (ix + 1) % 4
        self = Filter.cases[ix]
    }
}

```
### Struct
几乎所有的内置类型都是struct,Int,String,Array,Range,Struct...,
#### 初始化,属性,方法
struct没有也不需要明确的构造方法,因为他不保存属性,或者说他保存的属性都定义了默认值.默认struct有一个init()方法不带参数,这里可以直接用Digit()初始化.
```swift
struct Digit {
    var number=42
}

struct Digit {
    var number:Int
}
//这里也是合法的应为struct会有一个默认的init()方法给每个属性指定默认值.但是
//如果添加了自己的init方法就不行了
```
但是如果你定义了一个自己的init()那么就不能这样子了.
```swift
 struct Digit {
    var number = 42
    init() {}
    init(number:Int) {
        self.number = number
    }
}
```
如果要在其他代码中改变struct属性值,那么这个属性必须`var`定义,如果在struct内部改变变量值必须使用`mutating`,并且变量是`var`定义.
### class
class和struct类似,但是有几个关键不同点:
*引用类型*,*继承*
#### 数值类型和引用类型
enum和struct是数值类型,class是引用类型,数值类型是不可变类型:就是不可以改变其属性值,引用类型是可变类型:可以改变其属性值  
```swift
struct Digit{
    var number:Int
    init(_ n:Int){
        self.number=n
    }
}
```
这里定义变量`var d=Digit(123);d.number=45`看起来好像改变了struct对象的值,但是并没有改变.swift会生成一个新的struct独享,替换原有的对象.   
通常想要改变一个变量的属性需要用`var`定义,但是因为class是引用类型,所以即使用`let`声明他,也可以改变他的属性值.   
在函数传参时,如果改变数值类型参数的属性必须用`var`声明
```swift
func digitChanger(var d:Digit) {
    d.number = 42
}
```
但是对于class对象不需要
```swift
func dogChanger(d:Dog) {
    d.name = "Rover"
}
```
对于数值类型,赋值操作会赋值一份数据,两份数据只是值相同,没有其他任何关联.但是引用类型改变一处将会改变所有的引用.
```swift
//数值类型
var d = Digit(123)
print(d.number) // 123
var d2 = d // assignment!
d2.number = 42
print(d.number) // 123
//函数调用也不会改变原始参数值
func digitChanger(var d:Digit) {
    d.number = 42
}
var d = Digit(123)
print(d.number) // 123
digitChanger(d)
print(d.number) // 123

//引用类型
var fido = Dog()
print(fido.name) // Fido
var rover = fido // assignment!
rover.name = "Rover"
print(fido.name) // Rover
//函数调用后将会改变原始引用的值
func dogChanger(d:Dog) { // no "var" needed
    d.name = "Rover"
}
var fido = Dog()
print(fido.name) // "Fido"
dogChanger(fido)
print(fido.name) // "Rover"
```
#### 子类和父类
```swift
class Quadruped {
   func walk () {
       print("walk walk walk")
   }
}
class Dog : Quadruped {}
class Cat : Quadruped {}
//方法重写override
class Dog : Quadruped {
   func bark () {
       print("woof")
   }
}
class NoisyDog : Dog {
    override func bark () {
       for _ in 1...3 {
           super.bark()
       }
    }
}
```
#### 构造函数
class有一个默认init()不带任何参数,如果自定义了init(params)需要调用init(params)初始化.
构造函数有3类:  
`默认构造函数`:类没有保存任何属性,或者所有属性在定义时都有了默认值   
`自定义构造函数`:如果类的属性有任何一个没有在定义时给默认值,那么必须给出自定义构造函数初始化它.他生成类的实例时必须调用自定义构造函数中的任意至少一个.  
`便捷构造函数`:通过关键字`convenience`定义,他必须调用self.init(...),这里的构造函数必须在这个类中定义的自定义构造函数,或者是另外一个便捷构造函数.
```swift
//没有保存任何属性
class Dog {
}
let d = Dog()
//属性定义时给定了默认值
class Dog {
    var name = "Fido"
}
let d = Dog()  
//自定义构造函数
class Dog {
   var name : String
   var license : Int
   init(name:String, license:Int) {
        self.name = name
        self.license = license
   }
}
let d = Dog(name:"Rover", license:42)
//便捷构造函数
class Dog {
    var name : String
    var license : Int
    init(name:String, license:Int) {
        self.name = name
        self.license = license
    }
    convenience init(license:Int) {
        self.init(name:"Fido", license:license)
    }
    convenience init() {
        self.init(license:1)
    }
}
let d = Dog()
```
#### 子类构造函数
没有定义构造函数:   
他将会集成父类的构造函数   
只有便捷构造函数:   
If a subclass doesn’t have to have any initializers of its own, it is eligible to declare convenience initializers, and these work exactly as convenience initializers always do, because inheritance supplies self with the designated initializers that the convenience initializers must call.   
自定义构造函数:  
每一个自定义构造函数必须调用父类的一个构造函数`super.init(...)`     
父类的构造函数可以被子类覆盖:    
- 一个构造函数与父类的便捷构造函数匹配,那么他必须定义为便捷构造函数,并且不可用`override`
- 如果一个构造函数匹配父类的自定义构造,那么他可以是一个自定义构造函数或者便捷构造函数,并且必须用`override`定义
通常子类包含任何一个自定义构造函数时,任何一个构造函数都不会继承.但是如果子类覆盖(override)了所有的父类自定义构造函数,那么子类会继承父类的便捷构造函数
Failable构造函数:   
```swift
class Dog {
    var name : String
    var license : Int
    init(name:String, license:Int) {
        self.name = name
        self.license = license
    }
    convenience init(license:Int) {
        self.init(name:"Fido", license:license)
    }
}
class NoisyDog : Dog {
    override init(name:String, license:Int) {
        super.init(name:name, license:license)
    }
}
//这里NoisyDog 覆盖了父类所有的自定义构造函数,所以他继承了父类的便捷构造函数
let nd1 = NoisyDog(name:"Rover", license:1)
let nd2 = NoisyDog(license:2)
```
Required构造函数:   
如果一个类有子类那么子类必须覆盖这个构造函数,这里不能使用`override`而是同样使用`required`
```swift
class Dog {
    var name : String
    required init(name:String) {
        self.name = name
    }
}
class NoisyDog : Dog {
    var obedient = false
    init(obedient:Bool) {
        self.obedient = obedient
        super.init(name:"Fido")
    }
    required init(name:String) {
        super.init(name:name)
    }
}
```
#### 类的Deinitializer
这个方法会在对象销毁时调用.子类的Deinitializer会在父类的Deinitializer之前调用.
#### 类的属性和方法
子类可以覆盖父类的属性,他必须使用`override`,有两个额外的规则:
- 如果父类的属性是可写的,那么子类`override`时可能要添加`setter`和`getter`
- 子类`override`后可能是个`compute`变量;1.如果父类的属性是保存的,那么子类不许包含`getter`和`setter`;2.If the superclass property is computed, the subclass’s computed variable override must reimplement all the accessors that the superclass implements. If the superclass property is read-only (it has just a getter), the override can add a setter

类可以包含`static`和`class`成员,他们都会被子类继承.但是`static`成员不可被`override`.但是子类可以把父类中非`static`成员`override`为`static`

### Type Reference
swift中可以通过`dynamicType`属性来获得对象的`Type`
```swift
class Dog {
    class var whatDogsSay : String {
        return "Woof"
    }
    func bark() {
        print(self.dynamicType.whatDogsSay)
    }
}
```
```swift
class Dog {
    class var whatDogsSay : String {
        return "Woof"
    }
    func bark() {
        print(self.dynamicType.whatDogsSay)
    }
}
class NoisyDog : Dog {
    override class var whatDogsSay : String {
        return "Woof woof woof"
    }
}
let nd = NoisyDog()
nd.bark() // Woof woof woof
```
我们可以把`Type`当做参数传给函数,因为`Type`也是一个对象,通过他我们可以创建各种特殊函数例如工厂函数
```swift
func typeExpecter(whattype:Dog.Type) {
}
typeExpecter(Dog) // or: typeExpecter(Dog.self)
let d = Dog() // or: let d = NoisyDog()
typeExpecter(d.dynamicType) // or: typeExpecter(d.dynamicType.self)
```
```swift
class Dog {
    var name : String
    init(name:String) {
        self.name = name
    }
}
class NoisyDog : Dog {
}
func dogMakerAndNamer(whattype:Dog.Type) -> Dog {
    let d = whattype.init(name:"Fido") // 这里会报错,因为编译器不知道init(name:String)是否被所有的子类继承,所以需要添加`required`声明
    return d
}
```
这里会报错,因为编译器不知道init(name:String)是否被所有的子类继承,所以需要添加`required`声明
```swift
class Dog {
    var name : String
    required init(name:String) {
        self.name = name
    }
}
class NoisyDog : Dog {
}
func dogMakerAndNamer(whattype:Dog.Type) -> Dog {
    let d = whattype.init(name:"Fido")
    return d
}
let d = dogMakerAndNamer(Dog) // d is a Dog named Fido
let d2 = dogMakerAndNamer(NoisyDog) // d2 is a NoisyDog named Fido
```
可以使用多态性实现更有效的方式
```swift
class Dog {
    var name : String
    required init(name:String) {
           self.name = name
    }
    class func makeAndName() -> Self {//这里使用Self可以保证返回的是子类类型
        let d = self.init(name:"Fido")
        return d
    }
}
class NoisyDog : Dog {
}
let d = Dog.makeAndName() // d is a Dog named Fido
let d2 = NoisyDog.makeAndName() // d2 is a NoisyDog named Fido
```
- .dynamicType  
In code, sent to an instance: the polymorphic (internal) type of this instance, regardless of how the instance reference is typed. Static/class members are accessible through an instance’s dynamicType.
- .Type  
In declarations, sent to a type: the polymorphic type (as opposed to an instance of the type). For example, in a function declaration, Dog means a Dog instance is expected (or an instance of one its subclasses), but Dog.Type means that the Dog type itself is expected (or the type of one of its subclasses).
- .self  
In code, sent to a type: the type. For example, to pass the Dog type where Dog.Type is expected, you can pass Dog.self. (It is not illegal to send .self to an instance, but it is pointless.)
- self  
In instance code, this instance, polymorphically.In static/class code, this type, polymorphically; self.init(...) instantiates the type.
- Self  
In a method declaration, when specifying the return type, this class or this instance’s class, polymorphically.

### Protocol
有时候两个struct拥有一些共同的属性,但是struct没有继承机制,所以这里要用到protocol.   
protocol是一个对象类型,但是并没存在protocol对象,我们无法实例化他.  
protocol只是列出一些属性和方法,属性没有值.实际的对象类型将会完整的定义他们.
```swift
protocol Flier {
    func fly()
}
struct Bird : Flier {
    func fly() {
    }
}
func tellToFly(f:Flier) {
       f.fly()
}
struct Bee : Flier {
    func fly() {
    }
}
let b = Bee()
tellToFly(b)
```
这样任何一种类型,enum,struct,class,protocol都可以使用Flier.


## Xcode7
### 文件目录结构
project_name.xcodeproj,保存着项目信息:项目包含哪些文件,如何编译项目  
Base.lproj包含两个文件Main.storyboard and LaunchScreen.storyboard  
Assets.xcassets资源目录  
在Project navigator的分组,不会影响项目编译,他只是为了方便查看
### The Target
target是一个集合,它包含编译项目的规则和设置.编译的时候其实就是在编译target,有时候编译多个target  
在Project navigator点击最顶层项目名称,中间的editor会显示target的编辑页面
#### Build Phases
The build phases are both a report to you on how the target will be built and a set of instructions to Xcode on how to build the target
- Compile Sources  
  包含被编译的文件 and the resulting compiled code is copied into the app.
- Copy Bundle Resources  
  包含被复制到app中的资源文件,这样app运行时,系统就能找到他们
有时候可能需要添加Run Script build phase,他是shell命令,点击作伴+按钮添加
### From Project to Running App
app文件结构
```
Base.lproj  
    LaunchScreen.storyboardc  
    Main.storyboardc  
Empty Window  
Frameworks  
    libswiftContacts.dylib  
    libswiftCore.dylib  
    libswiftCoreGraphics.dylib  
    libswiftCoreImage.dylib  
    libswiftDarwin.dylib  
    libswiftDispatch.dylib  
    libswiftFoundation.dylib  
    libswiftObjectiveC.dylib  
    libswiftUIKit.dylib  
Info.plist  
PkgInfo  
```
### Nib Files
定义用户界面
### Code Files and the App Launch Process

## Cococa
