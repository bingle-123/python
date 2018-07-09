# 快速了解

ionic2.0 主要使用typescript来编程

## 第一个应用

npm install -g ionic@beta

ionic start StartApp tutorial --v2

ionic serve

## 项目目录

### www/index.html

项目的入口，他用来设置js，css以及启动应用。基本不用管这个文件。

ionic会去寻找html中的`<ion-app></ion-app>`

还有两个js`<script src="cordova.js"></script><script src="build/js/app.bundle.js"></script>`

build/js/app.bundle.js级连了ionic,angular,还有我们自己js

### app

是我们的应用的主文件，绝大部分代码都写在这里，这里是应用启动前的文件源码，默认是typesript。应用启动时他们会被自动编译成js，es5或者es6。

app.ts 是我们的app的入口

```typescript
@Component({
  templateUrl: 'build/app.html'
})
class MyApp {
  constructor() {
  }
}

ionicBootstrap(MyApp
```

每个app都有一个root组建用来控制应用的其余部分。

app.html是应用的主要模板

```html
<ion-menu [content]="content">

  <ion-toolbar>
    <ion-title>Pages</ion-title>
  </ion-toolbar>

  <ion-content>
    <ion-list>
      <button ion-item *ngFor="let p of pages" (click)="openPage(p)">
        {{p.title}}
      </button>
    </ion-list>
  </ion-content>

</ion-menu>

<ion-nav id="nav" [root]="rootPage" #content swipeBackEnabled="false"></ion-nav>
```

这里的我们把ion-menu作为边菜单，ion-nav是主内容区域。ion-menu的content绑定到ion-nav的content本地变量上，这样他就知道应该在哪里出现。

## 添加页面

下面我们来看看如何在我们的应用中创建页面，并在页面之间跳转。
