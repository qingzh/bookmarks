# Unit Test
> * What 什么是单元测试
* Why 为什么要做单元测试
* How 怎么做单元测试

---

# What is Unit Test
> * 什么是单元测试  
  * 最小代码块，最基本功能
  * 最少依赖，可独立执行
  * 易于执行，可重现，可自动化

>* 什么不是单元测试：
  * 访问数据库
  * 访问网络（如 RESTful 服务接口）
  * 访问文件系统
  * 不能独立运行
  *  运行单元测试需要额外的配置等

---

# Why Unit Test
> * 可持续的替代手动测试
* 保证基本功能达到预期
* 减少可预期的bug
* 有助于团队协作

---

# How to do Unit Test
> Python 单元测试 *unittest*:
* test fixture 测试现场
* test case 测试用例
* test suite 测试集
* test runner 测试执行 
   * settings.TEST_RUNNER: *django.test.simple.DjangoTestSuiteRunner*

---

# What's a Test Case
> * Setup 建立测试现场
* Action 执行
* Assertion 断言
* Teardown 清理测试现场

---

# What's a Test Case
![Django Unittest](https://docs.djangoproject.com/en/1.5/_images/django_unittest_classes_hierarchy.png)

---
# Code 
<pre><code>
def check_email_available(request):
    get_vars = request.GET
    js = {'success': False}
    if len(User.objects.filter(email=get_vars['email'])) > 0:
        js['value'] = _("An account with the Email '{email}' already exists.").format(
            email=get_vars['email'])
        js['field'] = 'email'
        return JsonResponse(js, status=200)
    js['success'] = True
    return JsonResponse(js, status=200)
</code></pre>

# Unit Testing
<pre><code>
class CheckEmailTest(TestCase):
    def setUp(self):
        # Create the test client
        self.client = Client()
        self.url = reverse('student.views.check_email_available')

    def test_email_available(self):
        post_params = {'email': 'test8f9g@gmail.com'}
        with patch('student.models.AUDIT_LOG') as mock_audit_log:
            result = self.client.get(self.url, post_params)
        # Assertion: Check response and log
        self._assert_response(result, success=True)

    def test_email_unavailable(self):
        post_params = {'email': 'test8f9g@edx.org'}
        with patch('student.models.AUDIT_LOG') as mock_audit_log:
            result = self.client.get(self.url, post_params)
        # Assertion: Check response and log
        self._assert_response(result, success=False)
</code></pre>

---

<pre><code>
class LoginAjaxTest(TestCase):
    def setUp(self):
        self.email = 'bryantly@126.com'
        self.client = Client()
        self.url = reverse('login')

    def test_login_success(self):
        post_params = {'email': self.email, 'password':'12345678'}
        with patch('student.models.AUDIT_LOG') as mock_log:
            result = self.client.post(self.url, post_params)
        self._assert_response(result, success=True)

    def test_login_failure_password_blank(self):
        post_params = {'email': self.email, 'password':''}
        with patch('student.models.AUDIT_LOG') as mock_log:
            result = self.client.post(self.url, post_params)
        expectedDict = {'issue':'blank', 'field':'password'}
        self._assert_response(result, success=False, **expectedDict)

</code></pre>

---

#  Unittest in Django
>1. 寻找django.test.TestCase的子类
2. 建立用于测试的数据库
3. 寻找以 test开头的方法
4. 建立实例
5. 检测结果

---

# Test Doubles
>1. Dummy Object: 需要传递但不会真正调用
2. Fake Object: 是真正接口或抽象类的简易实现
3. Test Stub: 传递间接的输入
4. Mock Object: 记录间接的输出 

---

# Why Mock
> * 真实对象的行为具有不确定性，例如网络延迟
* 真实对象难以创建，例如和UI交互
* 真实对象的行为难以模拟，例如网络错误
* 真实对象运行效率很低，读写数据库等
* 真实对象还没有实现

---
# Mock in Python
> Python mock 模块
* MagicMock()
* patch(), patch.object(), patch.dict()
<pre><code>
from StringIO import StringIO
class classA(object):
    def get_value(self, x):
        # TODO: get value of x
def foo(x):
    print '{}{}'.format(x, '>10' if classA().get_value(x) >10 else '<=10')
</code></pre><pre><code>
@patch('sys.stdout', new_callable=StringIO)
@patch('__main__.classA', new_callable=MagicMock)
def test_value_gt_10(mock_class, mock_stdout):
	mock_class.return_value.get_value.return_value = 11
	foo('fooCallable')
	assert mock_stdout.getvalue() == 'fooCallable>10\n'
</code></pre><pre><code>
@patch('sys.stdout', new_callable=StringIO)
@patch('__main__.classA', new_callable=MagicMock)
def test_value_lt_10(mock_class, mock_stdout):
	mock_class.return_value.get_value.return_value = 10
	foo('foo')
	assert mock_stdout.getvalue() == 'foo<=10\n'
</code></pre>

 foo()函数：
>1. 获取classA().get_value(x)的返回值
2. 当返回值>10，打印x+'>10'到标准输出
3. 当返回值<=10，打印x+'<=10'到标准输出

哪些需要mock：
>1.  标准输出('sys.stdout') 
用 'StringIO' 假扮 'sys.stdout' 获取间接输出：
`@patch('sys.stdout', new_callable=StringIO)`
2. 间接输入 classA.get_value(x)
用 'MagicMock' 假扮 '\_\_main\_\_.classA' 传递间接输入：
Mock classA: 
  `@patch('__main__.classA', new_callable=MagicMock)`
Mock classA().get_value():
  `mock_class.return_value.get_value.return_value = 30`


---

# UnitTest in Edx
> * Factory 的修改
* TestCase 的更新
* 自动化配置

---

# 相关阅读
#### [edx 测试概要](https://github.com/edx/edx-platform/blob/master/docs/en_us/internal/testing.rst)
> * [*voidspace mock*](http://www.voidspace.org.uk/python/mock/)
* [*FactoryBoy*](https://readthedocs.org/projects/factoryboy/): 批量生成数据
* [*unittest*](http://docs.python.org/2/library/unittest.html): Python单元测试
* [*jasmine*](http://jasmine.github.io/): JS单元测试
* [Dummy HTTP server](https://docs.djangoproject.com/en/dev/topics/testing/overview/): 简易的HTTP客户端
* UI Acceptance Tests