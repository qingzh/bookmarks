# BDD Testing
* Cucumber
* RobotFramework
* SpecFlow
* JBehave
* Fitness
* Concordion

* [InfoQ: Comparison between Cucumber and RobotFramework][1]
> 1. RobotFramework 的关键字本质是函数，所以用关键字来编写用例实际上也是在编写代码；和Cucumber的step definition是一样的。但是由于RobotFramework提供了可视化编写界面；会给人一种“我没有在写代码”的感觉。
2. RobotFramework 对中文的支持更好

对比结果：
| Cucumber | RobotFramework |
| -------- | -------------- |
| 使用自然语言，更易读 | 使用关键字机制，更容易上手 |
| 支持表格参数 | 提供了RIDE，对于不熟悉编码的人来说比较友好 |
| 支持多种格式report | 能够控制关键字的scope |
| 支持四种状态的测试步骤：Passed, Failed, Skipped, Pending | Log 和 Report 非常好 |
| 支持使用变形器消除重复 | 使用变量文件的机制来描述不同环境 |
| 有商用的在线Cucumber系统：Cucumber Pro | 丰富的关键字库，支持扩展 |

* 底层被测系统：Web? Rest? or others
* 测试库的选择：
 * 易用成都
 * 可持续性：是否有开源(或商业)支持
 * 测试库所用语言
* 上层测试框架：Cucumber, RobotFramework, Behave 等

## Cucumber

### Cucumber in Python 
Lettuce, Behave is Cucumber in Python

#### Lettuce
The issues we had with Lettuce that stopeed us using it were:
* Lack of tags
* The hooks functionality was patchy. For instance it was very hard to clean up the `world` variable between scenario outlines. *Behave* clears the scenario-level context between outlines automatcally
* Lettuce's handling of stdout would occasionally cause it to crash mid-run in such a way that cleanup hooks were never run
* Lettuce uses import hackery so `.pyc` files are left around and the module namespace is polluted

* Single decorator for *step* definitions `@step`
* The context variable, `world`, is simply a shared holder of attributes. It never gets cleaned up during the run
* Hooks are declared using decorators rather than as simple functions
* No support for tags
* Step definition code files can be anywhere in the feature directory hierarchy

### Cucumber in Java

#### Cucumber-JVM 

## Behave

[1]: http://www.infoq.com/cn/articles/cucumber-robotframework-comparison 'Comparison between Cucumber and RobotFramework'