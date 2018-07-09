# Redux

## 基本思想

- Web 应用是一个状态机，视图与状态是一一对应的
- 所有的状态，保存在一个对象里面

## 基本概念和API

### Store

Store就是保存数据的地方,整个应用只有一个store `import { createStore } from 'redux';const store = createStore(fn);`

### State

State对象包含所有数据,如果想要获取某一时刻数据,需要store生成数据快照`const state = store.getState();`

一个 State 对应一个 View。只要 State 相同，View 就相同。你知道 State，就知道 View 是什么样，反之亦然。

### Action
State的变化导致view变化.但是用户无法解除State,只能接触到view,所以view导致state变化,Action就是view发出的通知,表示state要发生变化.

Action 是一个对象。其中的type属性是必须的，表示 Action 的名称。其他属性可以自由设置

```javascript
const action = {
  type: 'ADD_TODO',
  payload: 'Learn Redux'
};
//Action 的名称是ADD_TODO，它携带的信息是字符串Learn Redux。
```
Action 描述当前发生的事情。改变 State 的唯一办法，就是使用 Action。它会运送数据到 Store。

#### Action Creator
View 要发送多少种消息，就会有多少种 Action。如果都手写，会很麻烦。可以定义一个函数来生成 Action，这个函数就叫 Action Creator。
```javascript
const ADD_TODO = '添加 TODO';

function addTodo(text) {
  return {
    type: ADD_TODO,
    text
  }
}

const action = addTodo('Learn Redux');
```
#### store.dispatch()
store.dispatch()是 View 发出 Action 的唯一方法。

```javascript
import { createStore } from 'redux';
const store = createStore(fn);

store.dispatch({
  type: 'ADD_TODO',
  payload: 'Learn Redux'
});
```

###  Reducer

Store 收到 Action 以后，必须给出一个新的 State，这样 View 才会发生变化。这种 State 的计算过程就叫做 Reducer。
Reducer 是一个函数，它接受 Action 和当前 State 作为参数，返回一个新的 State。

```javascript
const reducer = function (state, action) {
  // ...
  return new_state;
};
```
#### store.subscribe()
Store 允许使用store.subscribe方法设置监听函数，一旦 State 发生变化，就自动执行这个函数
显然，只要把 View 的更新函数（对于 React 项目，就是组件的render方法或setState方法）放入listen，就会实现 View 的自动渲染。
store.subscribe方法返回一个函数，调用这个函数就可以解除监听。
```javascript
let unsubscribe = store.subscribe(() =>
  console.log(store.getState())
);

unsubscribe();
```
