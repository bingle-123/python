# 快速上手

每个 Angular 应用至少有一个模块（根模块），习惯上命名为AppModule。

根模块在一些小型应用中可能是唯一的模块，大多数应用会有很多特性模块，每个模块都是一个内聚的代码块专注于某个应用领域、工作流或紧密相关的功能。

Angular 模块（无论是根模块还是特性模块）都是一个带有@NgModule装饰器的类。

NgModule是一个装饰器函数，它接收一个用来描述模块属性的元数据对象。其中最重要的属性是：
- declarations - 声明本模块中拥有的视图类。Angular 有三种视图类：组件、指令和管道。
- exports - declarations 的子集，可用于其它模块的组件模板。
- imports - 本模块声明的组件模板需要的类所在的其它模块。
- providers - 服务的创建者，并加入到全局服务列表中，可用于应用任何部分。
- bootstrap - 指定应用的主视图（称为根组件），它是所有其它视图的宿主。只有根模块才能设置bootstrap属性。


# 声明周期

ngOnChanges()
当Angular（重新）设置数据绑定输入属性时响应。 该方法接受当前和上一属性值的SimpleChanges对象当被绑定的输入属性的值发生变化时调用，首次调用一定会发生在ngOnInit()之前。

ngOnInit()	
在Angular第一次显示数据绑定和设置指令/组件的输入属性之后，初始化指令/组件。在第一轮ngOnChanges()完成之后调用，**只调用一次**。

ngDoCheck()	
检测，并在发生Angular无法或不愿意自己检测的变化时作出反应。**在每个Angular变更检测周期中调用**，ngOnChanges()和ngOnInit()之后。

ngAfterContentInit()	
当把内容投影进组件之后调用。第一次ngDoCheck()之后调用，只调用一次。**只适用于组件**。

ngAfterContentChecked()	
每次完成被投影组件内容的变更检测之后调用。ngAfterContentInit()和每次ngDoCheck()之后调用**只适合组件**。

ngAfterViewInit()	
初始化完组件视图及其子视图之后调用。第一次ngAfterContentChecked()之后调用，**只调用一次。只适合组件**。

ngAfterViewChecked()	
每次做完组件视图和子视图的变更检测之后调用。ngAfterViewInit()和每次ngAfterContentChecked()之后调用。**只适合组件**。

ngOnDestroy	
当Angular每次销毁指令/组件之前调用并清扫。 在这儿反订阅可观察对象和分离事件处理器，以防内存泄漏。在Angular销毁指令/组件之前调用。