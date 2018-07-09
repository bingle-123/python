# Angular模块

Angular模块是带有`@NgModule`装饰器函数的类。`@NgModule`接收一个元数据对象，该对象告诉Angular如何编译和运行模块代码。 它标记出该模块拥有的`组件、指令和管道`， 并把它们的一部分公开出去，以便外部组件使用它们。

## 声明指令和组件

```javascript
import { Directive, ElementRef, Renderer } from '@angular/core';

@Directive({ selector: '[highlight]' })
/** Highlight the attached element in gold */
export class HighlightDirective {
  constructor(renderer: Renderer, el: ElementRef) {
    renderer.setElementStyle(el.nativeElement, 'backgroundColor', 'gold');
    console.log(
      `* AppRoot highlight called for ${el.nativeElement.tagName}`);
  }
}
/////
template: '<h1 highlight>{{title}}</h1>'
////
declarations: [
  AppComponent,
  HighlightDirective,
],
```

```javascript
import { Component, Input } from '@angular/core';

@Component({
  moduleId: module.id,
  selector: 'app-title',
  templateUrl: 'title.component.html',
})
export class TitleComponent {
  @Input() subtitle = '';
  title = 'Angular Modules';
}
///////////////
import { Component } from '@angular/core';

@Component({
  selector: 'my-app',
  template: '<app-title [subtitle]="subtitle"></app-title>'
})
export class AppComponent {
  subtitle = '(v1)';
}
/////////
declarations: [
  AppComponent,
  HighlightDirective,
  TitleComponent,
],
```

## 服务提供商

```javascript
import { Injectable } from '@angular/core';

@Injectable()
/** Dummy version of an authenticated user service */
export class UserService {
  userName = 'Sherlock Holmes';
}
//
<h1 highlight>{{title}} {{subtitle}}</h1>
<p *ngIf="user">
  <i>Welcome, {{user}}</i>
<p>
//
import { Component, Input } from '@angular/core';
import { UserService } from './user.service';

@Component({
  moduleId: module.id,
  selector: 'app-title',
  templateUrl: 'title.component.html',
})
export class TitleComponent {
  @Input() subtitle = '';
  title = 'Angular Modules';
  user = '';

  constructor(userService: UserService) {
    this.user = userService.userName;
  }
}
//
providers: [ UserService ],
```

## 导入"支持模块"

`imports: [ BrowserModule, FormsModule ],`

## 特性模块

# 动画

# HTTP请求


# 路由与导航

在用户使用应用程序时， Angular 的 路由器 能让用户从一个 视图 导航到另一个视图。

## 基础知识

### base href=""

大多数带路由的应用都要在 `index.html` 的 标签下先添加一个元素，来告诉路由器该如何合成导航用的 URL 。 app中`<base href="/">`

### 从路由库中导入

Angular 的路由器是一个可选的服务，它用来呈现指定的 URL 所对应的视图,`@angular/router`,`import { Routes, RouterModule } from '@angular/router';`

### 配置

该应用将有一个 router （路由器） 。当浏览器的地址变化时，该路由器会查找相应的 Route （路由定义，简称路由），并据此确定所要显示的组件。需要先配置路由器，才会有路由信息。 首选方案是用带有"路由数组"的 provideRouter 工厂函数（ [provideRouter(routes)] ）来启动此应用。

```javascript
import { ModuleWithProviders } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

const appRoutes: Routes = [
  { path: 'hero/:id', component: HeroDetailComponent },
  { path: 'crisis-center', component: CrisisCenterComponent },
  {
    path: 'heroes',
    component: HeroListComponent,
    data: {
      title: 'Heroes List'
    }
  },
  { path: '', component: HomeComponent },
  { path: '**', component: PageNotFoundComponent }
];

export const appRoutingProviders: any[] = [

];

export const routing: ModuleWithProviders = RouterModule.forRoot(appRoutes);
```

> RouterConfig 是一个 路由 数组，它会决定如何导航。 每个 Route 会把一个 URL 的 path 映射到一个组件。

> **path中不能用斜线 / 开头** 。路由器会为我们解析和生成 URL ，以便在多个视图间导航时，可以自由使用相对路径和绝对路径。 第一个路由中的 :id 是一个路由参数的令牌 (Token) 。比如 /hero/42 这个 URL 中，" 42 "就是 id 参数的值。 此 URL 对应的 HeroDetailComponent 组件将据此查找和展现 id 为 42 的英雄。 在本章中稍后的部分，我们将会学习关于路由参数的更多知识。

> 第三个路由中的 **data 属性用来存放于每个具体路由有关的任意信息**。**该数据可以被任何一个激活路由访问**，并能用来保存诸如 页标题、面包屑以及其它只读数据。本章稍后的部分，我们将使用 resolve 守卫 来获取这些附加数据。

> 第四个路由中的 empty path 匹配各级路由的默认路径。 它还支持在不扩展 URL 路径的前提下添加路由。 第四个路由中的 ** 代表该路由是一个 通配符 路径。如果当前 URL 无法匹配上我们配置过的任何一个路由中的路径，路由器就会匹配上这一个。当需要显示 404 页面或者重定向到其它路由时，该特性非常有用。

> 这些路由的定义顺序 是故意如此设计的。路由器使用 先匹配者优先 的策略来匹配路由，所以，具体路由应该放在通用路由的前面。在上面的配置中，带静态路径的路由被放在了前面，后面是空路径路由，因此它会作为默认路由。而通配符路由被放在最后面，这是因为它是最通用的路由，应该 只在 前面找不到其它能匹配的路由时才匹配它。

### 路由插座

有了这份配置，当本应用在浏览器中的 URL 变为 /heroes 时，路由器就会匹配到 path 为 heroes 的 Route ，并在宿主视图中的 RouterOutlet 中显示 HeroListComponent 组件。`<router-outlet></router-outlet>`

### 路由器链接

现在，我们已经有了配置好的一些路由，还找到了渲染它们的地方，但又该如何导航到它呢？固然，从浏览器的地址栏直接输入 URL 也能做到，但是大多数情况下，导航是某些用户操作的结果，比如点击一个 A 标签。

我们往 A 标签上添加了 RouterLink 指令。由于我们知道链接中不包含任何动态信息，因此我们使用一次性绑定的方式把它绑定到我们路由中的 path 值。

如果 RouterLink 需要动态信息，我们就可以把它绑定到一个能返回路由链接数组（ 链接参数数组 ）的模板表达式上。 路由器最终会把此数组解析成一个 URL 和一个组件视图。

我们还往每个 A 标签上添加了一个 RouterLinkActive 指令，用于在相关的 RouterLink 被激活时为所在元素添加或移除 CSS 类。 该指令可以直接添加到该元素上，也可以添加到其父元素上。

```javascript
template: `
  <h1>Angular Router</h1>
  <nav>
    <a routerLink="/crisis-center" routerLinkActive="active">Crisis Center</a>
    <a routerLink="/heroes" routerLinkActive="active">Heroes</a>
  </nav>
  <router-outlet></router-outlet>
`
```

### 路由器状态

在导航时的每个生命周期成功完成时，路由器会构建出一个 ActivatedRoute 组成的树，它表示路由器的当前状态。 我们可以在应用中的任何地方用 Router 服务及其 routerState 属性来访问当前的 RouterState 值。

路由器状态为我们提供了从任意激活路由开始向上或向下遍历路由树的一种方式，以获得关于父、子、兄弟路由的信息。

### 路由器中的关键词汇及其含义

- Router(路由器):为激活的 URL 显示应用组件。管理从一个组件到另一个组件的导航
- RouterModule （路由器模块）:一个独立的 Angular 模块，用于提供所需的服务提供商，以及用来在应用视图之间进行导航的指令。
- Routes （路由数组）:定义了一个路由数组，每一个都会把一个 URL 路径映射到一个组件。
- Route （路由）:定义路由器该如何根据 URL 模式（ pattern ）来导航到组件。大多数路由都由路径和组件类构成。
- RouterOutlet （路由插座）:该指令（ `<router-outlet>` ）用来标记出路由器该在哪里显示视图。
- RouterLink （路由链接）:该指令用来把一个可点击的 HTML 元素绑定到路由。 点击带有绑定到 字符串 或 链接参数数组 的 routerLink 指令的 A 标签就会触发一次导航。
- RouterLinkActive （活动路由链接）:当 HTML 元素上或元素内的 routerLink 变为激活或非激活状态时，该指令为这个 HTML 元素添加或移除 CSS 类。
- ActivatedRoute （激活的路由）:为每个路由组件提供提供的一个服务，它包含特定于路由的信息，比如路由参数、静态数据、解析数据、全局查询参数和全局碎片（ fragment ）。
- RouterState （路由器状态）:路由器的当前状态包含了一棵由程序中激活的路由构成的树。它包含一些用于遍历路由树的快捷方法。
- 链接参数数组:这个数组会被路由器解释成一个路由操作指南。我们可以把一个 RouterLink 绑定到该数组，或者把它作为参数传给 Router.navigate 方法
- 路由组件:一个带有 RouterOutlet 的 Angular 组件，它根据路由器的导航来显示相应的视图。
