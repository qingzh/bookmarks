# Java SSH
Web Framework
* [struts][] 主要负责表示层的显示
* [spring][] 利用它的IOC和AOP来处理控制业务(负责对数据库的操作)
* [hibernate][] 数据持久化到数据库

在用jsp的servlet做web开发，有个web.xml的映射文件
 * `<listener>`
 * `<filter>`
 * `<filter-mapping>` 文件映射
 * `<welcome-file-list>`

URL映射：一个URL对应一个java文件；根据java文件里编写的内容显示在浏览器上(即网页)。所以网页名字是随便写的，不管是.php .jsp .do还是其他的什么都对应这个java文件，这个java文件里的代码进行什么操作就干什么，显示一句话还是连接数据库还是跳转到其他页面等等，这个java文件把数据进行封装起到安全和便于管理的作用。其实这个java文件编译过来是.class的一个字节码文件，没有那么一个类似html嵌入标签和代码的网页文件。他与jsp文件区别就是jsp把代码嵌入到html标签中。

还有servlet或者struts中html表单的 *action* 中的提交名称对应一个java文件，struts一般是.do的，都和上面一样是映射。

---
### Spring
Spring是一个解决了许多在J2EE开发中常见的问题的强大框架。 Spring提供了管理业务对象的一致方法并且鼓励了注入对接口编程而不是对类编程的良好习惯。Spring的架构基础是基于使用JavaBean属性的Inversion of Control容器。然而，这仅仅是完整图景中的一部分：Spring在使用IoC容器作为构建完关注所有架构层的完整解决方案方面是独一无二的。 Spring提供了唯一的数据访问抽象，包括简单和有效率的JDBC框架，极大的改进了效率并且减少了可能的错误。Spring的数据访问架构还集成了Hibernate和其他O/R mapping解决方案。Spring还提供了唯一的事务管理抽象，它能够在各种底层事务管理技术，例如JTA或者JDBC事务提供一个一致的编程模型。Spring提供了一个用标准Java语言编写的AOP框架，它给POJOs提供了声明式的事务管理和其他企业事务--如果你需要--还能实现你自己的aspects。这个框架足够强大，使得应用程序能够抛开EJB的复杂性，同时享受着和传统EJB相关的关键服务。Spring还提供了可以和IoC容器集成的强大而灵活的MVC Web框架。

* `@Requestmapping(value, params, method, headers, consumes, produces)`:
* `@RequestParam()`

---
### Struts
Struts是一个基于Sun J2EE平台的MVC框架，主要是采用Servlet和JSP技术来实现的。由于Struts能充分满足应用开发的需求，简单易用，敏捷迅速，在过去的一年中颇受关注。Struts把Servlet、JSP、自定义标签和信息资源(message resources)整合到一个统一的框架中，开发人员利用其进行开发时不用再自己编码实现全套MVC模式，极大的节省了时间，所以说Struts是一个非常不错的应用框架。

---
### Hibernate
Hibernate是一个开放源代码的对象关系映射框架，它对JDBC进行了非常轻量级的对象封装，使得Java程序员可以随心所欲的使用对象编程思维来操纵数据库。 Hibernate可以应用在任何使用JDBC的场合，既可以在Java的客户端程序实用，也可以在Servlet/JSP的Web应用中使用，最具革命意义的是，Hibernate可以在应用EJB的J2EE架构中取代CMP，完成数据持久化的重任。，Hibernate可以在应用EJB的J2EE架构中取代CMP，完成数据持久化的重任。

[spring]: http://baike.baidu.com/view/23023.htm 'spring'
[struts]: http://jackweijie.iteye.com/blog/214772 'struts'
[hibernate]: http://baike.baidu.com/view/7291.htm 'hibernate'