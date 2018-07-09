# FormData

```js
var formData = new FormData();

formData.append("username", "Groucho");
formData.append("accountnum", 123456); // number 123456 is immediately converted to a string "123456"

// HTML file input, chosen by user
formData.append("userfile", fileInputElement.files[0]);

// JavaScript file-like object
var content = '<a id="a"><b id="b">hey!</b></a>'; // the body of the new file...
var blob = new Blob([content], { type: "text/xml"});

formData.append("webmasterfile", blob);

var request = new XMLHttpRequest();
request.open("POST", "http://foo.com/submitform.php");
request.send(formData);
```
FormData的append方法可以写入Blob,File或者String.如果一个值不是Blob或者File,那么他会被转化为String

File接口继承自Blob

```js
var formElement = document.querySelector("form");
var formData = new FormData(formElement);
var request = new XMLHttpRequest();
request.open("POST", "submitform.php");
formData.append("serialnumber", serialNumber++);
request.send(formData);
```
可以直接从form中导入数据,然后还可以添加额外的数据

`data.append("myfile", myBlob, "filename.txt");`

如果直接写入Blob,那么第三个参数可以为Blob添加文件名


#  [Range](https://www.quirksmode.org/dom/range_intro.html)


# Selection
