# Selenium in Python
## [Selenium][selenium] 主要功能
> * 在浏览器中打开/关闭网页
* 和网页的交互（选择元素，填表，提交，滚动网页等）
* 提取网页数据

### Selenium 的坑
1. 元素未加载完全
> 当我们在打开了一个页面后，选择一个元素进行操作时，有可能会遇到 selenium 提示对应元素不可见的错误，原因在于页面没有加载完毕导致的，所以，selenium 提供了一个 waits 来等到对应的条件已经为真时，再进行相应的操作，这个比单纯的 sleep() 来进行等待要健壮的多，并且是 selenium 推崇的方式

  * WebDriverWait

2. Chrome 配置下载路径

3. Chrome 处理xls文件
  * xlrd

4. 编译器里的路径，例如cygwin:
  * Chrome
`
    options = ChromeOptions()
    real_path = os.path.dirname(os.path.realpath(__file__))
    #download_directory = os.path.join(real_path, 'downloads')
    download_directory = 'E:\downloads'
    prefs = {"download.default_directory":download_directory}
    options.add_experimental_option('prefs', prefs)
`
  * Firefox
`
    fp = webdriver.FirefoxProfile()

    fp.set_preference("browser.download.folderList",2)
    fp.set_preference("browser.download.manager.showWhenStarting",False)
    fp.set_preference("browser.download.dir",getcwd())
    fp.set_preference("browser.helperApps.neverAsk.saveToDisk","text/csv")

    browser = webdriver.Firefox(firefox_profile=fp)
`
> u'/cygdrive/d/github/webdriver/downloads'

[selenium]: https://selenium-python.readthedocs.org/ Selenium Documents