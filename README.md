# 划词翻译器

​	一个简单的词翻译器。

​	百度翻译的API.....

​	目前支持任何语言翻译到*中文*, *法语*, *英语*, *文言文*, *日语*，可以根据自己的喜好修改翻译方法。



### 使用方法

​	首先你需要拥有一个自己的百度翻译的ID与KEY，如何申请:https://jingyan.baidu.com/article/3f16e00305bb552591c10304.html

```python
	gui = GUI(appid='your_id', key='your_key')
```

​	官方文档:http://api.fanyi.baidu.com/product/113

​	如果想增加翻译的类型，或者指定翻译语言，也可以自己修改🎶
