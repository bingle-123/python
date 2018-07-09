# less

```less
#header {
  color: black;
  .navigation {
    font-size: 12px;
  }
  .logo {
    width: 300px;
  }
}
.bordered {
  border-top: dotted 1px black;
  border-bottom: solid 2px black;
}
#menu a {
  color: #111;
  .bordered;
}

.post a {
  color: red;
  .bordered;
}
```

`&`表示当前样式的父级

```less
.clearfix {
  display: block;
  zoom: 1;

  &:after {
    content: " ";
    display: block;
    font-size: 0;
    height: 0;
    clear: both;
    visibility: hidden;
  }
}
.button {
  &-ok {
    background-image: url("ok.png");
  }
  &-cancel {
    background-image: url("cancel.png");
  }

  &-custom {
    background-image: url("custom.png");
  }
}
// 编译结果
.clearfix {
  display: block;
  zoom: 1;
}
.clearfix:after {
  content: " ";
  display: block;
  font-size: 0;
  height: 0;
  clear: both;
  visibility: hidden;
}
.button-ok {
  background-image: url("ok.png");
}
.button-cancel {
  background-image: url("cancel.png");
}
.button-custom {
  background-image: url("custom.png");
}

```

## 运算

任何数字、颜色或者变量都可以参与运算。

```less
@base: 5%;
@filler: @base * 2;
@other: @base + @filler;
input{
    color: #888 / 4;
    background-color: @base-color + #111;
    height: 100% / 2 + @filler;
}
```

函数

Less 内置了多种函数用于转换颜色、处理字符串、算术运算等。这些函数在函数手册中有详细介绍。

函数的用法非常简单。下面这个例子将介绍如何将 0.5 转换为 50%，将颜色饱和度增加 5%，以及颜色亮度降低 25% 并且色相值增加 8 等用法：

```less
@base: #f04615;
@width: 0.5;

.class {
  width: percentage(@width); // returns `50%`
  color: saturate(@base, 5%);
  background-color: spin(lighten(@base, 25%), 8);
}
```
## 命名空间和访问

```less
#bundle {
  .button {
    display: block;
    border: 1px solid black;
    background-color: grey;
    &:hover {
      background-color: white
    }
  }
}
#header a {
  color: orange;
  #bundle > .button;
}
//
#bundle .button {
  display: block;
  border: 1px solid black;
  background-color: grey;

}
#bundle .button:hover {
  background-color: white;
}
#header a {
  color: orange;
  display: block;
  border: 1px solid black;
  background-color: grey;
}
#header a:hover {
  background-color: white;
}
```

## 作用域

```less
@var: red;
#page {
  #header {
    color: @var; // white
  }
  @var: white;
}
```

## 导入
可以导入一个 .less 文件，此文件中的所有变量就可以全部使用了。如果导入的文件是 .less 扩展名，则可以将扩展名省略掉：
```less
@import "library"; // library.less
@import "typo.css";
```

## 变量插入

```less
// Variables
@mySelector: banner;

// Usage
.@{mySelector} {
  font-weight: bold;
  line-height: 40px;
  margin: 0 auto;
}

// Variables
@images: "../img";
// 用法
body {
  color: #444;
  background: url("@{images}/white-sand.png");
}

//导入模块之前必须先定义好变量的名称
// Variables
@themes: "../../src/themes";
// Usage
@import "@{themes}/tidal-wave.less";

//属性
@property: color;
.widget {
  @{property}: #0ee;
  background-@{property}: #999;
}
//变量名
@fnord:  "I am fnord.";
@var:    "fnord";
content: @@var;
```
