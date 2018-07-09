# CSS

## 选择器

```
- .class   .intro    Selects all elements with class="intro"    1
- #id       #firstname    Selects the element with id="firstname"    1
- *           *    Selects all elements    2
- element    p    Selects all <p> elements    1
- element,element    div, p    Selects all <div> elements and all <p> elements    1
- element element    div p    Selects all <p> elements inside <div> elements    1
- element>element    div > p    Selects all <p> elements where the parent is a <div> element    2
- element+element    div + p    Selects all <p> elements that are placed immediately after <div> elements    2
- element1~element2    p ~ ul    Selects every <ul> element that are preceded by a <p> element    3
- [attribute]            [target]    包含此属性
- [attribute=value]        [target=_blank] 等于
- [attribute~=value]    [title~=flower]    包含单词
- [attribute|=value]    [lang|=en]    lang=en的所有元素    2
- [attribute^=value]    a[href^="https"] 开头
- [attribute$=value]    a[href$=".pdf"]    结尾
- [attribute*=value]    a[href*="w3schools"]    包含
- :active    a:active
- ::after    p::after    在元素后面插入
- ::before    p::before    在元素之前插入
- :checked    input:checked    所有checked input元素3
- :disabled    input:disabled    所有diable的input元素
- :empty    p:empty    选择所有不包含子元素的p元素(包含文本节点)
- :enabled    input:enabled    所有enabled的input元素
- :first-child    p:first-child    选则所有作为第一个子元素的p元素
- ::first-letter    p::first-letter    选择所有元素的第一个字符
- ::first-line    p::first-line    选择所有元素的第一行
- :first-of-type    p:first-of-type    Selects every <p> element that is the first <p> element of its parent
- :focus    input:focus    所有focus状态的input元素
- :hover    a:hover    鼠标移动到元素上时
- :in-range    input:in-range    选择值在指定范围内的input元素
- :invalid    input:invalid    选择值是valid的input元素
- :lang(language)    p:lang(it)    选择所有lang为it的元素
- :last-child    p:last-child    选择作为父级最后一个子元素的元素
- :last-of-type    p:last-of-type    Selects every <p> element that is the last <p> element of its parent    3
- :link    a:link    选择所有为访问的a
- :not(selector)    :not(p)    选择所有不是<p>的元素 这里p可以替换为class id等
- :nth-child(n)    p:nth-child(2)    选择作为第n个子元素的p元素
- :nth-last-child(n)    p:nth-last-child(2)    从尾部开始计算
- :nth-last-of-type(n)    p:nth-last-of-type(2)    Selects every <p> element that is the second <p> element of its parent, counting from the last child    3
- :nth-of-type(n)    p:nth-of-type(2)    Selects every <p> element that is the second <p> element of its parent    3
- :only-of-type    p:only-of-type    Selects every <p> element that is the only <p> element of its parent    3
- :only-child    p:only-child    Selects every <p> element that is the only child of its parent    3
- :optional    input:optional    所有非required得input元素
- :out-of-range    input:out-of-range     选择值不在指定范围内的input元素
- :read-only    input:read-only 所有readonly得input
- :read-write    input:read-write    选择非只读input
- :required    input:required    所有required的input
- :root    :root    Selects the document's root element    3
- ::selection    ::selection    Selects the portion of an element that is selected by a user
- :target    #news:target    Selects the current active #news element (clicked on a URL containing that anchor name)    3
- :valid    input:valid    所有valid的input
- :visited    a:visited 所有访问过的a
```

## 函数

cal()

```css
#div1 {
    position: absolute;
    left: 50px;
    width: calc(100% - 100px);
    border: 1px solid black;
    background-color: yellow;
    padding: 5px;
    text-align: center;
}
```

attr()

```css
a:after {
    content: " (" attr(href) ")";
}
```

## 实体

可以使用 [实体字符](https://www.w3schools.com/cssref/css_entities.asp) 来填写字符

```css
i:after {
    content: ' \00A7';
}
```

## 单位

### 相对长度

- em Relative to the font-size of the element (2em means 2 times the size of the current font) Try it
- ex Relative to the x-height of the current font (rarely used) Try it
- ch Relative to width of the "0" (zero)
- rem Relative to font-size of the root element
- vw Relative to 1% of the width of the viewport* Try it
- vh Relative to 1% of the height of the viewport* Try it
- vmin Relative to 1% of viewport's* smaller dimension Try it
- vmax Relative to 1% of viewport's* larger dimension Try it
- %

### 绝对长度

```
- cm    centimeters Try it
- mm    millimeters Try it
- in    inches (1in = 96px = 2.54cm) Try it
- px *    pixels (1px = 1/96th of 1in) Try it
- pt    points (1pt = 1/72 of 1in) Try it
- pc    picas (1pc = 12 pt)
```

## 字体

```css
@font-face
{
font-family: myFirstFont;
src: url('Sansation_Light.ttf'),
     url('Sansation_Light.eot'); /* IE9+ */
}
div
{
font-family:myFirstFont;
}
```

## 2D转换

```css
div
{
transform: rotate(30deg);
-ms-transform: rotate(30deg);        /* IE 9 */
-webkit-transform: rotate(30deg);    /* Safari and Chrome */
-o-transform: rotate(30deg);        /* Opera */
-moz-transform: rotate(30deg);        /* Firefox */
}
```

2D转换支持的属性

- transform 向元素应用 2D 或 3D 转换。 3
- transform-origin 允许你改变被转换元素的位置。 3
- matrix(n,n,n,n,n,n) 定义 2D 转换，使用六个值的矩阵。
- translate(x,y) 定义 2D 转换，沿着 X 和 Y 轴移动元素。
- translateX(n) 定义 2D 转换，沿着 X 轴移动元素。
- translateY(n) 定义 2D 转换，沿着 Y 轴移动元素。
- scale(x,y) 定义 2D 缩放转换，改变元素的宽度和高度。
- scaleX(n) 定义 2D 缩放转换，改变元素的宽度。
- scaleY(n) 定义 2D 缩放转换，改变元素的高度。
- rotate(angle) 定义 2D 旋转，在参数中规定角度。
- skew(x-angle,y-angle) 定义 2D 倾斜转换，沿着 X 和 Y 轴。
- skewX(angle) 定义 2D 倾斜转换，沿着 X 轴。
- skewY(angle) 定义 2D 倾斜转换，沿着 Y 轴。

## 3D转换

```css
div
{
transform: rotateX(120deg);
-webkit-transform: rotateX(120deg);    /* Safari 和 Chrome */
-moz-transform: rotateX(120deg);    /* Firefox */
}
```

转换属性

- transform 向元素应用 2D 或 3D 转换。
- transform-origin 允许你改变被转换元素的位置。
- transform-style 规定被嵌套元素如何在 3D 空间中显示。
- perspective 规定 3D 元素的透视效果。
- perspective-origin 规定 3D 元素的底部位置。
- backface-visibility 定义元素在不面对屏幕时是否可见。 2D Transform 方法 函数 描述
- matrix3d(n,n,n,n,n,n,n,n,n,n,n,n,n,n,n,n) 定义 3D 转换，使用 16 个值的 4x4 矩阵。
- translate3d(x,y,z) 定义 3D 转化。
- translateX(x) 定义 3D 转化，仅使用用于 X 轴的值。
- translateY(y) 定义 3D 转化，仅使用用于 Y 轴的值。
- translateZ(z) 定义 3D 转化，仅使用用于 Z 轴的值。
- scale3d(x,y,z) 定义 3D 缩放转换。
- scaleX(x) 定义 3D 缩放转换，通过给定一个 X 轴的值。
- scaleY(y) 定义 3D 缩放转换，通过给定一个 Y 轴的值。
- scaleZ(z) 定义 3D 缩放转换，通过给定一个 Z 轴的值。
- rotate3d(x,y,z,angle) 定义 3D 旋转。
- rotateX(angle) 定义沿 X 轴的 3D 旋转。
- rotateY(angle) 定义沿 Y 轴的 3D 旋转。
- rotateZ(angle) 定义沿 Z 轴的 3D 旋转。
- perspective(n) 定义 3D 转换元素的透视视图。

## 过度

```css
div
{
transition: width 2s;
-moz-transition: width 2s;    /* Firefox 4 */
-webkit-transition: width 2s;    /* Safari 和 Chrome */
-o-transition: width 2s;    /* Opera */
}
```

过度属性

- transition 简写属性，用于在一个属性中设置四个过渡属性。
- transition-property 规定应用过渡的 CSS 属性的名称。
- transition-duration 定义过渡效果花费的时间。默认是 0。
- transition-timing-function 规定过渡效果的时间曲线。默认是 "ease"。
- transition-delay 规定过渡效果何时开始。默认是 0。

## 动画

```html
<!DOCTYPE html>
<html>
<head>
<style>
div
{
width:100px;
height:100px;
background:red;
animation:myfirst 5s;
-moz-animation:myfirst 5s; /* Firefox */
-webkit-animation:myfirst 5s; /* Safari and Chrome */
-o-animation:myfirst 5s; /* Opera */
}

@keyframes myfirst
{
from {background:red;}
to {background:yellow;}
}

@-moz-keyframes myfirst /* Firefox */
{
from {background:red;}
to {background:yellow;}
}

@-webkit-keyframes myfirst /* Safari and Chrome */
{
from {background:red;}
to {background:yellow;}
}

@-o-keyframes myfirst /* Opera */
{
from {background:red;}
to {background:yellow;}
}
</style>
</head>
<body>

<div></div>

<p><b>注释：</b>本例在 Internet Explorer 中无效。</p>

</body>
</html>

<!DOCTYPE html>
<html>
<head>
<style>
div
{
width:100px;
height:100px;
background:red;
position:relative;
animation:myfirst 5s;
-moz-animation:myfirst 5s; /* Firefox */
-webkit-animation:myfirst 5s; /* Safari and Chrome */
-o-animation:myfirst 5s; /* Opera */
}

@keyframes myfirst
{
0%   {background:red; left:0px; top:0px;}
25%  {background:yellow; left:200px; top:0px;}
50%  {background:blue; left:200px; top:200px;}
75%  {background:green; left:0px; top:200px;}
100% {background:red; left:0px; top:0px;}
}

@-moz-keyframes myfirst /* Firefox */
{
0%   {background:red; left:0px; top:0px;}
25%  {background:yellow; left:200px; top:0px;}
50%  {background:blue; left:200px; top:200px;}
75%  {background:green; left:0px; top:200px;}
100% {background:red; left:0px; top:0px;}
}

@-webkit-keyframes myfirst /* Safari and Chrome */
{
0%   {background:red; left:0px; top:0px;}
25%  {background:yellow; left:200px; top:0px;}
50%  {background:blue; left:200px; top:200px;}
75%  {background:green; left:0px; top:200px;}
100% {background:red; left:0px; top:0px;}
}

@-o-keyframes myfirst /* Opera */
{
0%   {background:red; left:0px; top:0px;}
25%  {background:yellow; left:200px; top:0px;}
50%  {background:blue; left:200px; top:200px;}
75%  {background:green; left:0px; top:200px;}
100% {background:red; left:0px; top:0px;}
}
</style>
</head>
<body>

<p><b>注释：</b>本例在 Internet Explorer 中无效。</p>

<div></div>

</body>
</html>
```

动画属性

- @keyframes 规定动画。
- animation 所有动画属性的简写属性，除了 animation-play-state 属性。
- animation-name 规定 @keyframes 动画的名称。
- animation-duration 规定动画完成一个周期所花费的秒或毫秒。默认是 0。
- animation-timing-function 规定动画的速度曲线。默认是 "ease"。
- animation-delay 规定动画何时开始。默认是 0。
- animation-iteration-count 规定动画被播放的次数。默认是 1。
- animation-direction 规定动画是否在下一周期逆向地播放。默认是 "normal"。
- animation-play-state 规定动画是否正在运行或暂停。默认是 "running"。
- animation-fill-mode 规定对象动画时间之外的状态。

## 新的用户界面属性(基本不支持)

- appearance 允许您将元素设置为标准用户界面元素的外观 3
- box-sizing 允许您以确切的方式定义适应某个区域的具体内容。 3
- icon 为创作者提供使用图标化等价物来设置元素样式的能力。 3
- nav-down 规定在使用 arrow-down 导航键时向何处导航。 3
- nav-index 设置元素的 tab 键控制次序。 3
- nav-left 规定在使用 arrow-left 导航键时向何处导航。 3
- nav-right 规定在使用 arrow-right 导航键时向何处导航。 3
- nav-up 规定在使用 arrow-up 导航键时向何处导航。 3
- outline-offset 对轮廓进行偏移，并在超出边框边缘的位置绘制轮廓。 3
- resize 规定是否可由用户对元素的尺寸进行调整。 3

## 颜色渐变

- linear-gradient 线性渐变
- radial-gradient 径向梯度
- repeating-linear-gradient 重复线性渐变
- repeating-radial-gradient 重复径向梯度

background: linear-gradient(direction, color-stop1, color-stop2, ...);

```css
#grad {
  background: red; /* For browsers that do not support gradients */
  background: -webkit-linear-gradient(left, red , yellow); /* For Safari 5.1 to 6.0 */
  background: -o-linear-gradient(right, red, yellow); /* For Opera 11.1 to 12.0 */
  background: -moz-linear-gradient(right, red, yellow); /* For Firefox 3.6 to 15 */
  background: linear-gradient(to right, red , yellow); /* Standard syntax */
}
// 从左上角开始
#grad {
  background: red; /* For browsers that do not support gradients */
  background: -webkit-linear-gradient(left top, red, yellow); /* For Safari 5.1 to 6.0 */
  background: -o-linear-gradient(bottom right, red, yellow); /* For Opera 11.1 to 12.0 */
  background: -moz-linear-gradient(bottom right, red, yellow); /* For Firefox 3.6 to 15 */
  background: linear-gradient(to bottom right, red, yellow); /* Standard syntax */
}
```

线性渐变使用角度来制定方向

如果想要更多地控制渐变的方向，您可以定义一个角度，而不是预定义的方向（从底部到顶部，从右到左，到右下角等）。

```css
#grad {
  background: red; /* For browsers that do not support gradients */
  background: -webkit-linear-gradient(-90deg, red, yellow); /* For Safari 5.1 to 6.0 */
  background: -o-linear-gradient(-90deg, red, yellow); /* For Opera 11.1 to 12.0 */
  background: -moz-linear-gradient(-90deg, red, yellow); /* For Firefox 3.6 to 15 */
  background: linear-gradient(-90deg, red, yellow); /* Standard syntax */
}
```

重复线性

```css
#grad {
  background: red; /* For browsers that do not support gradients */
  /* Safari 5.1 to 6.0 */
  background: -webkit-repeating-linear-gradient(red, yellow 10%, green 20%);
  /* Opera 11.1 to 12.0 */
  background: -o-repeating-linear-gradient(red, yellow 10%, green 20%);
  /* Firefox 3.6 to 15 */
  background: -moz-repeating-linear-gradient(red, yellow 10%, green 20%);
  /* Standard syntax */
  background: repeating-linear-gradient(red, yellow 10%, green 20%);
}
```

径向梯度

```css
#grad {
  background: red; /* For browsers that do not support gradients */
  background: -webkit-radial-gradient(red 5%, yellow 15%, green 60%); /* Safari 5.1-6.0 */
  background: -o-radial-gradient(red 5%, yellow 15%, green 60%); /* For Opera 11.6-12.0 */
  background: -moz-radial-gradient(red 5%, yellow 15%, green 60%); /* For Firefox 3.6-15 */
  background: radial-gradient(red 5%, yellow 15%, green 60%); /* Standard syntax */
}

#grad {
  background: red; /* For browsers that do not support gradients */
  background: -webkit-radial-gradient(circle, red, yellow, green); /* Safari */
  background: -o-radial-gradient(circle, red, yellow, green); /* Opera 11.6 to 12.0 */
  background: -moz-radial-gradient(circle, red, yellow, green); /* Firefox 3.6 to 15 */
  background: radial-gradient(circle, red, yellow, green); /* Standard syntax */
}

/*使用不同大小的关键字*/
/*size参数定义了渐变的大小。它可以取四个值：
最近端
最远的端
最近的角
最远的角落*/
#grad1 {
  background: red; /* For browsers that do not support gradients */
  /* Safari 5.1 to 6.0 */
  background: -webkit-radial-gradient(60% 55%, closest-side, red, yellow, black);
  /* For Opera 11.6 to 12.0 */
  background: -o-radial-gradient(60% 55%, closest-side, red, yellow, black);
  /* For Firefox 3.6 to 15 */
  background: -moz-radial-gradient(60% 55%, closest-side, red, yellow, black);
  /* Standard syntax */
  background: radial-gradient(closest-side at 60% 55%, red, yellow, black);
}
#grad2 {
  /* Safari 5.1 to 6.0 */
  background: -webkit-radial-gradient(60% 55%, farthest-side, red, yellow, black);
  /* Opera 11.6 to 12.0 */
  background: -o-radial-gradient(60% 55%, farthest-side, red, yellow, black);
  /* For Firefox 3.6 to 15 */
  background: -moz-radial-gradient(60% 55%, farthest-side, red, yellow, black);
  /* Standard syntax */
  background: radial-gradient(farthest-side at 60% 55%, red, yellow, black);
}
```

重复径向梯度

```css
#grad {
  background: red; /* For browsers that do not support gradients */
  /* For Safari 5.1 to 6.0 */
  background: -webkit-repeating-radial-gradient(red, yellow 10%, green 15%);
  /* For Opera 11.6 to 12.0 */
  background: -o-repeating-radial-gradient(red, yellow 10%, green 15%);
  /* For Firefox 3.6 to 15 */
  background: -moz-repeating-radial-gradient(red, yellow 10%, green 15%);
  /* Standard syntax */
  background: repeating-radial-gradient(red, yellow 10%, green 15%);
}
```


## object-fit 

img 和 video 大小

fill - This is default. The replaced content is sized to fill the element's content box. If necessary, the object will be stretched or squished to fit

contain - The replaced content is scaled to maintain its aspect ratio while fitting within the element's content box

cover - The replaced content is sized to maintain its aspect ratio while filling the element's entire content box. The object will be clipped to fit

none - The replaced content is not resized

scale-down - The content is sized as if none or contain were specified (would result in a smaller concrete object size)

## Multi-column

- column-count	Specifies the number of columns an element should be divided into
- column-fill	Specifies how to fill columns
- column-gap	Specifies the gap between the columns
- column-rule	A shorthand property for setting all the column-rule-* properties
- column-rule-color	Specifies the color of the rule between columns
- column-rule-style	Specifies the style of the rule between columns
- column-rule-width	Specifies the width of the rule between columns
- column-span	Specifies how many columns an element should span across
- column-width	Specifies a suggested, optimal width for the columns
- columns	A shorthand property for setting column-width and column-count

## User Interface Properties

- box-sizing	Allows you to include the padding and border in an element's total width and height
- nav-down	Specifies where to navigate when using the arrow-down navigation key
- nav-index	Specifies the tabbing order for an element
- nav-left	Specifies where to navigate when using the arrow-left navigation key
- nav-right	Specifies where to navigate when using the arrow-right navigation key
- nav-up	Specifies where to navigate when using the arrow-up navigation key
- outline-offset	Adds space between an outline and the edge or border of an element
- resize	Specifies whether or not an element is resizable by the user

## Media Queries

```css

@media screen and (max-width: 699px) and (min-width: 520px) {
    ul li a {
        padding-left: 30px;
        background: url(email-icon.png) left center no-repeat;
    }
}

@media screen and (max-width: 1000px) and (min-width: 700px) {
    ul li a:before {
        content: "Email: ";
        font-style: italic;
        color: #666666;
    }
}


@media screen and (min-width: 1001px) {
    ul li a:after {
        content: " (" attr(data-email) ")";
        font-size: 12px;
        font-style: italic;
        color: #666666;
    }
}

@media screen and (max-width: 699px) and (min-width: 520px), (min-width: 1151px) {
    ul li a {
        padding-left: 30px;
        background: url(email-icon.png) left center no-repeat;
    }
}
```

## Grid `display: grid;`