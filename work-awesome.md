* 原型设计工具Axure
* 用Lucene搭建了一个单机版本的搜索服务
* RubyOnRails
* java+jetty
* ElasticSearch, CS:
文／祝威廉（简书作者）
原文链接：http://www.jianshu.com/p/9e0aba6eaaa1
著作权归作者所有，转载请联系作者获得授权，并标注“简书作者”。

CS作为一个分布式索引服务，特点有：

* 分布式架构
* 支持索引数据分片
* 支持构建离线全量索引过程中合并线上新增数据的机制
* 支持数据热备
* 拥有一个剥离配套的统一查询引擎
* 支持模块化，组件化

CS的核心是是查询引擎和索引存储剥离。一些高级功能，比如跨索引检索，结果二次排序，摘要提取，获取详细内容展示，都是作为模块放在查询引擎中。当然统一查询引擎最核心的意义还是在于可以快速更新二次排序的引擎。当然这还需要有一些其他架构做支撑。
有新的模块添加，只需重启查询引擎，而不需要重启索引存储服务。索引文件重新打开是非常消耗CPU,IO的,常常会造成机器负载瞬间飙升，导致很多搜索维护人员轻易不敢重启服务。在CS不存在这个问题。

* 本质上大数据平台是一种解决问题的范式，一个通用的分布式计算存储平台。

#### 数据支撑平台


Hadoop/Spark/HBase 体系，支撑BI,数据离线分析，推荐协同计算等


分布式索引服务，支撑搜索，数据平台供查询数据的存储


统一查询引擎，为数据产品提供统一的查询接口


内容网关+数据网关+上报，打通产品到数据平台的入口。


分布式缓存体系(Redis) ，可支持推荐系统，数据网关等产品


初步的服务监控体系 (参看:https://code.csdn.net/allwefantasy/platform 的介绍)


推荐系统，支持相关内容推荐，用户个性化推荐，公共队列展示，底层完全基于Redis实现。这里有个给兄弟公司介绍的一个PPT(http://vdisk.weibo.com/s/HZFjdG-haPc)


配置与发布系统(运维相关)

#### digest


程序员再也不应该仅仅是写代码让服务跑起来或者设计一个架构做到良好的扩展性，这些工作本质上是重复性的工作，你很难做到和别人不一样，所以才会有码农，你只是垒代码。