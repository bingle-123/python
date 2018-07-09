# 架构

HTML模版-->组件-->注入服务-->模块化

## 模块 (Modules)

每个应用都有一个模块(根模块)，习惯上命名为AppModule。任何一个模块都带有@NgModule装饰器类。

### NgModule

NgModule是一个装饰器函数，它接收一个用来描述模块属性的元数据对象。其中最重要的属性是：

- declarations （声明） - 本模块中拥有的视图类。 Angular 有三种视图类： 组件 、 指令 和 管道 。
- exports - 声明（ declaration ）的子集，它可用于其它模块中的组件 模板 。
- imports - 本 模块组件模板中需要由其它模块导出的类。
- providers - 服务 的创建者。本模块把它们加入全局的服务表中，让它们在应用中的任何部分都可被访问到。
- bootstrap - 标识出应用的主视图（被称为 根组件 ），它是所有其它视图的宿主。只有 根模块 才能设置 bootstrap 属性。

```javascript
import { NgModule }      from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
@NgModule({
  imports:      [ BrowserModule ],
  providers:    [ Logger ],
  declarations: [ AppComponent ],
  exports:      [ AppComponent ],
  bootstrap:    [ AppComponent ]
})
export class AppModule { }
```

引导跟模块来启动应用

```javascript
import { platformBrowserDynamic } from '@angular/platform-browser-dynamic';
import { AppModule } from './app.module';

platformBrowserDynamic().bootstrapModule(AppModule);
```

## 组件 (Components)

组件负责控制屏幕上的一小块地方，我们称之为视图

## 模板 (Templates)

通过组件的自带的 **模板** 来定义视图。模板以HTML形式存在，用来告诉Angular如何渲染组件(视图)。

```html
<h2>Hero List</h2>
<p><i>Pick a hero from the list</i></p>
<ul>
  <li *ngFor="let hero of heroes" (click)="selectHero(hero)">
    {{hero.name}}
  </li>
</ul>
<hero-detail *ngIf="selectedHero" [hero]="selectedHero"></hero-detail>
```

## 元数据 (Metadata)

我们用 装饰器 (decorator) 来附加元数据到类上。

## 数据绑定 (Data Binding)

四种方式：

- {{hero.name}} 插值表达式 ：在
- 标签中显示了组件的 hero.name 属性的值。
- [hero] 属性绑定 ：把父组件 HeroListComponent 的 selectedHero 的值传到子组件 HeroDetailComponent 的 hero 属性中。
- (click) 事件绑定 ：当用户点击英雄的名字时，调用组件的 selectHero 方法。
- [(ngModel)]=""双向绑定

## 指令 (Directives)

Angular 模板是 动态的 。当 Angular 渲染它们时，它会根据 指令 提供的操作指南对 DOM 进行修改。

`@Component` 装饰器实际上就是一个 `@Directive`装饰器,只是扩展了一些面向模板的属性。

还有两种类型指令：

- 结构型指令 通过在 DOM 中 **添加、移除和替换元素** 来修改布局。例如：`*ngIf`,`*ngFor`
- 属性型指令 **修改一个现有元素的外观或行为** ，例如`[(ngModel)]`,`ngClass`,`ngSwitch`,`ngStyle`

## 服务 (Services)

服务 分为很多种，包括：值、函数，以及应用所需的特性,几乎任何东西都可以是一个服务。 典型的服务是一个类，具有专注的、良好定义的用途。它应该做一件具体的事情，把它做好。

## 依赖注入 (Dependency Injection)

"依赖注入"是提供类的新实例的一种方式，还负责处理好类所需的全部依赖。大多数依赖都是服务。 Angular 也使用依赖注入提供我们需要的组件以及这些组件所需的服务。

Angular 能通过查看构造函数的参数类型，来得知组件需要哪些服务。 例如， HeroListComponent 组件的构造函数需要一个HeroService： `constructor(private service: HeroService) { }`

当 Angular 创建组件时，会首先为组件所需的服务找一个 注入器（ Injector ） 。

**注入器** 是一个维护服务实例的容器，存放着以前创建的实例。 如果没有服务实例-->创建并返回。

必须在要求注入 HeroService 之前，把一个叫 HeroService 的提供商 Provider 到注入器。我们通常会把提供商添加到 根模块 上，以便任何地方使用的都是服务的同一个实例。

```javascript
providers: [
  BackendService,
  HeroService,
  Logger
],
```

也可以在 `@Component`元数据中的 providers 属性中把它注册在组件层：

```javascript
@Component({
  selector:    'hero-list',
  templateUrl: 'app/hero-list.component.html',
  providers:   [ HeroService ]
})
```

# 显示数据

模版绑定数据

# 事件绑定

使用 Angular 事件绑定 机制来响应 任何 DOM 事件 。

```javascript
@Component({
  selector: 'click-me',
  template: `
    <button (click)="onClickMe()">Click me!</button>
    {{clickMessage}}`
})
export class ClickMeComponent {
  clickMessage = '';

  onClickMe() {
    this.clickMessage = 'You are my hero!';
  }
}
```

## 通过 $event 对象取得用户输入

```javascript
template: `
  <input (keyup)="onKey($event)">
  <p>{{values}}</p>
`
//
export class KeyUpComponent_v1 {
  values = '';
  // without strong typing
  onKey(event:any) {
    this.values += event.target.value + ' | ';
  }
}
```

## 从一个模板引用变量中获得用户输入

```javascript
@Component({
  selector: 'loop-back',
  template: `
    <input #box (keyup)="0">
    <p>{{box.value}}</p>
  `
})
export class LoopbackComponent { }
//
@Component({
  selector: 'key-up2',
  template: `
    <input #box (keyup)="onKey(box.value)">
    <p>{{values}}</p>
  `
})
export class KeyUpComponent_v2 {
  values = '';
  onKey(value: string) {
    this.values += value + ' | ';
  }
}
//
@Component({
  selector: 'key-up2',
  template: `
    <input #box (keyup)="onKey($event)">
    <p>{{values}}</p>
  `
})
export class KeyUpComponent_v2 {
  values = '';
  onKey(key: any) {
    this.values = key.keyCode;
  }
}
```

box即使input元素本身，修改input值的时候，会立即影响到p标签。

## 按键事件过滤 ( 通过 key.enter)

```javascript
@Component({
  selector: 'key-up3',
  template: `
    <input #box (keyup.enter)="values=box.value">
    <p>{{values}}</p>
  `
})
export class KeyUpComponent_v3 {
  values = '';
}
```

## blur( 失去焦点 ) 事件

可以同时绑定blur事件

```javascript
@Component({
  selector: 'key-up4',
  template: `
    <input #box
      (keyup.enter)="values=box.value"
      (blur)="values=box.value">

    <p>{{values}}</p>
  `
})
export class KeyUpComponent_v4 {
  values = '';
}
```

# 表单

[(ngModel)] 内幕:

```html
<input type="text" class="form-control" id="name"
       required
       [ngModel]="model.name" name="name"
       (ngModelChange)="model.name = $event" />
  TODO: remove this: {{model.name}}
```

ngModelChange 并不是

<input>

元素的事件。 它实际上是一个来自 ngModel 指令的事件属性。 当 Angular 在表单中看到一个[(x)] 的绑定目标时， 它会期待这个 x 指令有一个名为 x 的输入属性，和一个名为 xChange 的输出属性。

模板表达式中的另一个古怪之处是 model.name = $event 。 我们以前看到的 $event 变量是来自 DOM 事件的。 但 ngModelChange 属性不会生成 DOM 事件----它是一个 Angular EventEmitter 类型的属性，当它触发时， 它返回的是输入框的值----它恰好和我们希望赋给模型上 name 属性的值一样。

## 通过 ngModel 跟踪修改状态与有效性验证

状态       | 为真时的 CSS 类 | 为假时的 CSS 类
:------- | :--------- | :-----------
控件已经被访问过 | ng-touched | ng-untouched
控件值已经变化  | ng-dirty   | ng-pristine
控件值是有效的  | ng-valid   | ng-invalid

input绑定到spy，通过spy显示当前css名称

```html
<input type="text" class="form-control" id="name"
  required
  [(ngModel)]="model.name" name="name"
  #spy />
<br>TODO: remove this: {{spy.className}}
```

当input发生变化时，他的class也会变化，刚启动应用时的class="form-control ng-untouched ng-pristine ng-valid"

## 通过 ngSubmit 来提交表单

heroForm 变量引用的是 NgForm 指令，它代表的是表单的整体。Angular 自动创建了 NgForm 指令，并且把它附加到 `form` 标签上。

NgForm 指令为普通的 form 元素扩充了额外的特性。 它持有我们通过 ngModel 指令和 name 属性为各个元素创建的那些控件类，并且监视它们的属性变化，包括有效性。 它还有自己的 valid 属性，只有当 每一个被包含的控件 都有效时，它才有效。

```html
<form *ngIf="active" (ngSubmit)="onSubmit()" #heroForm="ngForm"/>
<button type="submit" class="btn btn-default" [disabled]="!heroForm.form.valid">Submit</button>
```

# 依赖注入

```javascript
import { Injectable } from '@angular/core';
import { HEROES }     from './mock-heroes';
@Injectable()
export class HeroService {
  getHeroes() { return HEROES;  }
}
```

## 配置注入器

我们并不需要自己创建一个 Angular 注入器。 Angular 在启动期间会自动为我们创建一个全应用级注入器。

我们在AppModule中使用NgModule中配置的provider就是一个注入器。在这里注入的服务，全局都可以访问到。但是有一些服务我们只需在特定的组件中使用，这是后就不需要放在根model里面，而是在`@component`中定义。

```javascript
@Component({
  selector: 'my-heroes',
  providers: [HeroService],
  template: `
  <h2>Heroes</h2>
  <hero-list></hero-list>
  `
})
```

## 为注入准备 HeroListComponent

下面的HeroService是在全局注入。这里import进来然后在构造函数中调用。

```javascript
import { Component }   from '@angular/core';
import { Hero }        from './hero';
import { HeroService } from './hero.service';
@Component({
  selector: 'hero-list',
  template: `
  <div *ngFor="let hero of heroes">
    {{hero.id}} - {{hero.name}}
  </div>
  `
})
export class HeroListComponent {
  heroes: Hero[];
  constructor(heroService: HeroService) {
    this.heroes = heroService.getHeroes();
  }
}
```

## 服务需要别的服务

当一个服务以来与另外一个服务时，我们还是通过构造函数来实现

```javascript
import { Injectable } from '@angular/core';
import { HEROES }     from './mock-heroes';
import { Logger }     from '../logger.service';
@Injectable()
export class HeroService {
  constructor(private logger: Logger) {  }
  getHeroes() {
    this.logger.log('Getting heroes ...');
    return HEROES;
  }
}
```

`@Component`,`@Directive`,`@Pipe`都是InjectableMetadata 的子类型

## 创建和注册日志服务

## Provider 类和 provide 对象常量

`providers: [Logger]`是`[{ provide: Logger, useClass: Logger }]`的简写。第一个是令牌 token ，它作为键值 key 使用，用于定位依赖值，以及注册这个提供商。第二个是一个 provider definition object。

## 别名类提供商

我们不能升级OldLogger组件并使用它。可以使用别名来替换他。

```javascript
[ NewLogger,
  // Not aliased! Creates two instances of `NewLogger`
  { provide: OldLogger, useClass: NewLogger}]

[ NewLogger,
  // Alias OldLogger w/ reference to NewLogger
  { provide: OldLogger, useExisting: NewLogger}]
```

## 值提供商

```javascript
// An object in the shape of the logger service
let silentLogger = {
  logs: ['Silent logger says "Shhhhh!". Provided via "useValue"'],
  log: () => {}
};

[{ provide: Logger, useValue: silentLogger }]
```

## 工厂提供商

有时我们需要动态创建这个依赖值，因为它所需要的信息我们直到最后一刻才能确定。 比如，也许这个信息会在浏览器的会话中不停的变化。假设这个可注入的服务没法通过独立的源访问此信息。

```javascript
constructor(
  private logger: Logger,
  private isAuthorized: boolean) { }

getHeroes() {
  let auth = this.isAuthorized ? 'authorized ' : 'unauthorized';
  this.logger.log(`Getting heroes for ${auth} user.`);
  return HEROES.filter(hero => this.isAuthorized || !hero.isSecret);
}
//
let heroServiceFactory = (logger: Logger, userService: UserService) => {
  return new HeroService(logger, userService.user.isAuthorized);
};
//
export let heroServiceProvider =
  { provide: HeroService,
    useFactory: heroServiceFactory,
    deps: [Logger, UserService]
  };
```

## 非类依赖

```javascript
export interface AppConfig {
  apiEndpoint: string;
  title: string;
}

export const HERO_DI_CONFIG: AppConfig = {
  apiEndpoint: 'api.heroes.com',
  title: 'Dependency Injection'
};

// FAIL!  Can't use interface as provider token
[{ provide: AppConfig, useValue: HERO_DI_CONFIG })]

// FAIL! Can't inject using the interface as the parameter type
constructor(private config: AppConfig){ }
```

上面失败是因为angular不能够使用interface作为注入令牌。

### 解决方法

解决方案是定义和使用一个 OpaqueToken( 不透明的令牌 ) 。定义方式类似于这样：

```javascript
import { OpaqueToken } from '@angular/core';

export let APP_CONFIG = new OpaqueToken('app.config');

providers: [{ provide: APP_CONFIG, useValue: HERO_DI_CONFIG }]

constructor(@Inject(APP_CONFIG) config: AppConfig) {
  this.title = config.title;
}
```

## 直接使用注入器工作

很少直接使用他

```javascript
@Component({
  selector: 'my-injectors',
  template: `
  <h2>Other Injections</h2>
  <div id="car">{{car.drive()}}</div>
  <div id="hero">{{hero.name}}</div>
  <div id="rodent">{{rodent}}</div>
  `,
  providers: [Car, Engine, Tires, heroServiceProvider, Logger]
})
export class InjectorComponent {
  car: Car = this.injector.get(Car);
  heroService: HeroService = this.injector.get(HeroService);
  hero: Hero = this.heroService.getHeroes()[0];
  constructor(private injector: Injector) { }
  get rodent() {
    let rousDontExist = `R.O.U.S.'s? I don't think they exist!`;
    return this.injector.get(ROUS, rousDontExist);
  }
}
```

# 模版语法

## 绑定语法：概览

单向从数据源到视图目标，Property,Attribute,类,样式。

```
{{expression}}
[target] = "expression"
bind-target = "expression"
```

单向从视图目标到数据源,事件。

```
(target) = "statement"
on-target = "statement"
```

双向

```
[(target)] = "expression"
bindon-target = "expression"
```

一旦我们开始数据绑定，我们就不再跟 Attribute 打交道了。我们并不是在设置 Attribute ， 而是在设置 DOM 元素、组件和指令的 Property。

Attribute 是由 HTML 定义的。 Property 是由 DOM(Document Object Model) 定义的。

- 少量 HTML Attribute 和 Property 之间有着 1:1 的映射。 id 就是一个例子。
- 有些 HTML Attribute 没有对应的 Property 。 colspan 就是一个例子。
- 有些 DOM Property 没有对应的 Attribute 。 textContent 就是一个例子。
- 大量 HTML Attribute 看起来映射到了 Property ......但却不像我们想象的那样！

**Attribute 初始化 DOM Property ，然后它们的任务就完成了。 Property 的值可以改变； Attribute 的值不能改变。**

当浏览器渲染 `<input type="text" value="Bob">` 时，它创建了一个对应的 DOM 节点，它的 value Property 被 初始化为 " Bob "。

当用户在输入框中输入" Sally "时， DOM 元素的 value Property 变成了" Sally "。 但是这个 HTMLvalue Attribute 保持不变。 如果我们通过 input.getAttribute('value') // 返回 "Bob" 语句获取这个 input 元素的 Attribute ，就会明白这一点。

**就算名字相同， HTML Attribute 和 DOM Property 也不是同一样东西。**

**模板绑定是通过 Property 和 事件 来工作的，而不是 Attribute 。**

> 在 Angular 2 的世界中， Attribute 唯一的作用是用来初始化元素和指令的状态。 当进行数据绑定时，我们只是在与元素和指令的 Property 和事件打交道，而 Attribute 就完全靠边站了

## 绑定目标

数据绑定的目标 是 DOM 中的某些东西。 这个目标可能是 ( 元素 | 组件 | 指令 ) 的 Property 、 ( 元素 | 组件 | 指令 ) 的事件，或 ( 极少数情况下 ) 一个 Attribute 名。

```
//元素的 Property
<img [src] = "heroImageUrl">

//组件的 Property
<hero-detail [hero]="currentHero"></hero-detail>

//指令的 Property
<div [ngClass] = "{selected: isSelected}"></div>

//元素的事件
<button (click) = "onSave()">Save</button>

//组件的事件
<hero-detail (deleteRequest)="deleteHero()"></hero-detail>

//指令的事件
<div (myClick)="clicked=$event">click me</div>

//事件与 Property
<input [(ngModel)]="heroName">

//Attribute 例外情况
<button [attr.aria-label]="help">help</button>

//class property
<div [class.special]="isSpecial">Special</div>

//style property
<button [style.color] = "isSpecial ? 'red' : 'green'">
```

## 属性绑定

`<img [src]="heroImageUrl">`等同于`<img bind-src="heroImageUrl">`

元素属性可能是最常见的绑定目标，但 Angular 会先去看这个名字是否是某个已知指令的属性名，就像下面的例子中一样：

`<div [ngClass]="classes">[ngClass] binding to the classes property</div>`

> 从技术的角度看， Angular 正在匹配一个指令的 input 的名字。这个名字是指令的 inputs 数组中所列的名字之一，或者是一个带有 `@Input()` 装饰器的属性。 这样的 inputs 被映射到了指令自己的属性。

## 方括号

属性绑定时不可以省略`[]`

## 一次性字符串初始化

如果目标属性接受字符串值。我们经常这样在标准 HTML 中用这种方式初始化 Attribute 。 `<hero-detail prefix="You are my" [hero]="currentHero"></hero-detail>`

## Attribute 、 Class 和 Style 绑定

模板语法为那些不太适合使用属性绑定的场景提供了专门的单向数据绑定形式。

```
<table border=1>
  <!--  expression calculates colspan=2 -->
  <tr><td [attr.colspan]="1 + 1">One-Two</td></tr>

  <!-- ERROR: There is no `colspan` property to set!
    <tr><td colspan="{{1 + 1}}">Three-Four</td></tr>
  -->

  <tr><td>Five</td><td>Six</td></tr>
</table>
```

```
<!-- toggle the "special" class on/off with a property -->
<div [class.special]="isSpecial">The class binding is special</div>

<!-- binding to `class.special` trumps the class attribute -->
<div class="special"
     [class.special]="!isSpecial">This one is not so special</div>
```

```
<button [style.color] = "isSpecial ? 'red': 'green'">Red</button>
<button [style.background-color]="canSave ? 'cyan': 'grey'" >Save</button>
```

## 事件绑定

`<button (click)="onSave()">Save</button>`等同于`<button on-click="onSave()">On Save</button>` 元素事件可能是更常见的目标，但 Angular 会先看这个名字是否能匹配上已知指令的事件属性,别名 input/output 属性 章节有更多关于该 myClick 指令的解释。

```
<!-- `myClick` is an event on the custom `MyClickDirective` -->
<div (myClick)="clickMessage=$event">click with myClick</div>
```

### $event 和事件处理语句

`$event`就是一个 DOM 事件对象 ，它有像 target 和 target.value

```
<input [value]="currentHero.firstName"
       (input)="currentHero.firstName=$event.target.value" >
```

### 使用 EventEmitter 实现自定义事件

要用到`@output()`,在自身内部触发事件，然后通知他的父级执行相应的方法

```
template: `
<div>
  <img src="{{heroImageUrl}}">
  <span [style.text-decoration]="lineThrough">
    {{prefix}} {{hero?.fullName}}
  </span>
  <button (click)="delete()">Delete</button>
</div>`
//这里是在hero-detail组件

// This component make a request but it can't actually delete a hero.
deleteRequest = new EventEmitter<Hero>();

//button点击后触发deleteRequest
delete() {
  this.deleteRequest.emit(this.hero);
}

//下面是父级组件调用
<hero-detail (deleteRequest)="deleteHero($event)" [hero]="currentHero"></hero-detail>
```

# 使用 NgModel 进行双向数据绑定

> 要使用 ngModel 做双向数据绑定，得先把 FormsModule 导入我们的模块并把它加入 NgModule 装饰器的 imports 数组。

```javascript
import { NgModule } from '@angular/core';
import { BrowserModule }  from '@angular/platform-browser';
import { FormsModule } from '@angular/forms';
import { AppComponent } from './app.component';
@NgModule({
  imports: [
    BrowserModule,
    FormsModule
  ],
  declarations: [
    AppComponent
  ],
  bootstrap: [ AppComponent ]
})
export class AppModule { }
```

## [(ngModel)] 内幕

通过分别绑定到

<input>

元素的 value 属性和 input 事件，我们能达到同样的效果

```html
<input [value]="currentHero.firstName" (input)="currentHero.firstName=$event.target.value" >

<input [ngModel]="currentHero.firstName" (ngModelChange)="currentHero.firstName=$event">
<!-- ngModel 输入属性设置元素的值属性，而 ngModelChange 输出属性监听元素值的变化。 实现细节对每种元素都很特定，所以 NgModel 指令只和元素一起工作，比如输入框， -->
```

`<input [(ngModel)]="currentHero.firstName">`

> [(ngModel)] 是一个更通用的模式中的具体例子，在这里， Angular 会把 [(x)] 语法去掉语法糖，变成了一个供属性绑定用的输入属性 x ，和一个供事件绑定用的输出属性 xChange 。 Angular 通过在模板表达式的原始字符串后面追加上 =$event ，来构建出供事件绑定用的模板语句。利用这一行为，我们也可以自己写出具有双向绑定功能的指令。[(x)]="e" <==> [x]="e" (xChange)="e=$event"

如果需要强制将input值做修改，可以使用`<input [ngModel]="currentHero.firstName" (ngModelChange)="setUpperCaseFirstName($event)">`这里强制将输入大写。

## 内置指令

### NgClass

CSS 类绑定 是添加或删除 单个 类的最佳途径。

```javascript
<div [class.special]="isSpecial">The class binding is special</div>
```

当我们想要同时添加或移除 多个 CSS 类时， NgClass 指令可能是更好的选择。绑定到一个 key:value 形式的控制对象，是应用 NgClass 的好方式。这个对象中的每个 key 都是一个 CSS 类名，如果它的 value 是 true ，这个类就会被加上，否则就会被移除。

```javascript
setClasses() {
  let classes =  {
    saveable: this.canSave,      // true
    modified: !this.isUnchanged, // false
    special: this.isSpecial,     // true
  };
  return classes;
}

<div [ngClass]="setClasses()">This div is saveable and special</div>
```

### NgStyle

样式绑定 是设置 单一 样式值的简单方式。

```javascript
<div [style.font-size]="isSpecial ? 'x-large' : 'smaller'" >
  This div is x-large.
</div>
```

如果我们要同时设置 多个 内联样式， NgStyle 指令可能是更好的选择。我们通过把它绑定到一个 key:value 控制对象的形式使用 NgStyle 。 对象的每个 key 是样式名，它的 value 就是能用于这个样式的任何值。考虑一个类似于 setStyles 的组件方法，它返回一个定义三种样式的对象：

```javascript
setStyles() {
  let styles = {
    // CSS property names
    'font-style':  this.canSave      ? 'italic' : 'normal',  // italic
    'font-weight': !this.isUnchanged ? 'bold'   : 'normal',  // normal
    'font-size':   this.isSpecial    ? '24px'   : '8px',     // 24px
  };
  return styles;
}
<div [ngStyle]="setStyles()">
  This div is italic, normal weight, and extra large (24px).
</div>
```

### NgIf

可见性和 NGIF 不是一回事

```javascript
<!-- isSpecial is true -->
<div [class.hidden]="!isSpecial">Show with class</div>
<div [class.hidden]="isSpecial">Hide with class</div>

<!-- HeroDetail is in the DOM but hidden -->
<hero-detail [class.hidden]="isSpecial"></hero-detail>

<div [style.display]="isSpecial ? 'block' : 'none'">Show with style</div>
<div [style.display]="isSpecial ? 'none'  : 'block'">Hide with style</div>
```

### ngSwitch

```javascript
<span [ngSwitch]="toeChoice">
  <span *ngSwitchCase="'Eenie'">Eenie</span>
  <span *ngSwitchCase="'Meanie'">Meanie</span>
  <span *ngSwitchCase="'Miney'">Miney</span>
  <span *ngSwitchCase="'Moe'">Moe</span>
  <span *ngSwitchDefault>other</span>
</span>
```

### NgFor

`<div *ngFor="let hero of heroes; let i=index">{{i + 1}} - {{hero.fullName}}</div>`

ngFor 指令有时候会性能较差，特别是在大型列表中。 对一个条目的一点小更改、移除或添加，都会导致级联的 DOM 操作。我们给它一个 追踪 函数， Angular 就可以避免这种折腾。追踪函数告诉 Angular ：我们知道两个具有相同 hero.id 的对象其实是同一个英雄。 下面就是这样一个函数:

```javascript
trackByHeroes(index: number, hero: Hero) { return hero.id; }
<div *ngFor="let hero of heroes; trackBy:trackByHeroes">({{hero.id}}) {{hero.fullName}}</div>
```

### `*` 与 <template>

`*`是一种语法糖，它让那些需要借助模板来修改`HTML`布局的指令更易于读写。 NgFor 、 NgIf 和 NgSwitch 都会添加或移除元素子树，这些元素子树被包裹在 `<template>` 标签

我们没有看到`<template>` 标签，那是因为这种 `*` 前缀语法让我们忽略了这个标签，而把注意力直接聚焦在所要包含、排除或重复的那些`HTML`元素上。

```html
<hero-detail template="ngIf:currentHero" [hero]="currentHero"></hero-detail>

<template [ngIf]="currentHero">
  <hero-detail [hero]="currentHero"></hero-detail>
</template>


<span [ngSwitch]="toeChoice">
  <!-- with *NgSwitch -->
  <span *ngSwitchCase="'Eenie'">Eenie</span>
  <span *ngSwitchCase="'Meanie'">Meanie</span>
  <span *ngSwitchCase="'Miney'">Miney</span>
  <span *ngSwitchCase="'Moe'">Moe</span>
  <span *ngSwitchDefault>other</span>

  <!-- with <template> -->
  <template [ngSwitchCase]="'Eenie'"><span>Eenie</span></template>
  <template [ngSwitchCase]="'Meanie'"><span>Meanie</span></template>
  <template [ngSwitchCase]="'Miney'"><span>Miney</span></template>
  <template [ngSwitchCase]="'Moe'"><span>Moe</span></template>
  <template ngSwitchDefault><span>other</span></template>
</span>


<hero-detail template="ngFor let hero of heroes; trackBy:trackByHeroes" [hero]="hero"></hero-detail>
<template ngFor let-hero [ngForOf]="heroes" [ngForTrackBy]="trackByHeroes">
  <hero-detail [hero]="hero"></hero-detail>
</template>

```

## 模板引用变量

`ref-`和`#`定义效果一致

```javascript
<!-- phone refers to the input element; pass its `value` to an event handler -->
<input #phone placeholder="phone number">
<button (click)="callPhone(phone.value)">Call</button>

<!-- fax refers to the input element; pass its `value` to an event handler -->
<input ref-fax placeholder="fax number">
<button (click)="callFax(fax.value)">Fax</button>
```

### NgForm 和模板引用变量

```javascript
<form (ngSubmit)="onSubmit(theForm)" #theForm="ngForm">
  <div class="form-group">
    <label for="name">Name</label>
    <input class="form-control" name="name" required [(ngModel)]="currentHero.firstName">
  </div>
  <button type="submit" [disabled]="!theForm.form.valid">Submit</button>
</form>
```

## 声明输入和输出属性

```javascript
@Input()  hero: Hero;
@Output() deleteRequest = new EventEmitter<Hero>();
//或者
@Component({
  inputs: ['hero'],
  outputs: ['deleteRequest'],
})
```
输入属性通常接收数据值。 输出属性暴露事件生产者，比如 EventEmitter 对象。

### 输入 / 输出属性别名

```javascript
@Output('myClick') clicks = new EventEmitter<string>(); //  @Output(alias) propertyName = ...
<div (myClick)="clickMessage=$event">click with myClick</div>

@Directive({
  outputs: ['clicks:myClick']  // propertyName:alias
})
```

## 管道

```
<!-- Pipe chaining: convert title to uppercase, then to lowercase -->
<div>
  Title through a pipe chain:
  {{title | uppercase | lowercase}}
</div>
```

## 安全导航操作符 ( ?. ) 和空属性路径

```
The current hero's name is {{currentHero?.firstName}}

<!--No hero, div not displayed, no error -->
<div *ngIf="nullHero">The null hero's name is {{nullHero.firstName}}</div>

The null hero's name is {{nullHero && nullHero.firstName}}

```
