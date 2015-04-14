# Selenium in Python
## [Selenium][selenium] 主要功能
> * 在浏览器中打开/关闭网页
* 和网页的交互（选择元素，填表，提交，滚动网页等）
* 提取网页数据

### Selenium 的坑
1. 元素未加载完全
> 当我们在打开了一个页面后，选择一个元素进行操作时，有可能会遇到 selenium 提示对应元素不可见的错误，原因在于页面没有加载完毕导致的，所以，selenium 提供了一个 waits 来等到对应的条件已经为真时，再进行相应的操作，这个比单纯的 sleep() 来进行等待要健壮的多，并且是 selenium 推崇的方式

[selenium]: https://selenium-python.readthedocs.org/ Selenium Documents