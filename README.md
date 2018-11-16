# faker-flask 框架
[![Build Status](https://travis-ci.org/lai-bluejay/faker_flask.svg?branch=master)](https://travis-ci.org/lai-bluejay/faker_flask)



## 概述

  主要用于快速各类型的线上服务。
  
  主要特色功能：
   - MVC开发架构拆分。（没C，由于都是remote function方式的调用)
   - 配合wizard进行开发和日志记录
   - DB操作的约束。mysql推荐使用records。
   - 日志记录分离
   
  TODO——list
  - 常用Utils类的封装
  - logging规范化，
  - 单元测试范例，
  - 项目日志
  - 本地部署测试 (fabric+supervisor)
  
  整个项目将模拟一个分单场景，通过开发staff和order对象，完成order和staff的匹配和分单。
  
  要做新的开发的时候，可以在参照此场景的用例，进行改进。其中model，dao，objects, 以及外部的test 是开发人员主要的工作量，其他每次的变动并不是很大，基本Bug只会出现在红色区域
  
  
   
## 代码结构

```    
    README.rst
    LICENSE
    setup.py
    requirements.txt
    faker   --- 项目名称
      /conf  配置文件
      /config  配置类
      /dao   数据获取层
      /data   数据
      /dbhelper  数据库对象
      /models   业务逻辑核心
      /objects  业务对象
      /servers   接口代码
      /utils
    docs --- 文档
      /conf.py
      /index.rst
    tests   ---测试用例
      /test_basic.py
      /test_advanced.py
```




## 代码包说明
    项目包
        servers 控制path、接口的返回结果。根据wizard的设定，接口地址和server类名相同，指定remote-function进行调用。 --后续可能转为函数计算。
                
        models 模型层代码，主要是根据输入数据，进行数据库操作和进一步的加工处理，给出返回值到 调用的 server 层
        
        dao 数据访问层，将数据访问的操作封装在这里，最理想的情况，model 层没有SQL语句出现
        
        objects 模型映射代码，主要是将业务逻辑抽象出一些实体对象，将对对象的操作和数据填充写到这里。数据来源可以是 Mongo, Mysql 或者是 HTTP 请求
        
        dbhelper 数据库操作代码，分为 MySQL 和 Mongo 两种进行封装，只封装进行最简单的操作，由dao层调用，注意Mongo 和 MySQL 的数据库连接最好都是 连接池的形式。
        PyMongo自带连接池功能，而MySQL当前通过 records(SQLalchemy) 管理连接池
        
        utils 工具包，主要放一些不依赖于数据库，不依赖于业务的一些工具类。
    
    test 单元测试代码包。里面的各个代码主要是在代码写好之后，写的测试用例，保证代码的基本情况可用
    
    启动：gunicorn  -w1 -b0.0.0.0:12345 nvwa_order_grade_server:app --reload


## 新功能开发流程

   如果要开发一个新的接口，请按照以下建议步骤来做，
   
   重要的事情说三遍，***先从Dao层开始***，***先从Dao层开始***，***先从Dao层开始***，***Git每天提交***，***Git每天提交***，***Git每天提交***
   
   * 前置：建立Git代码库，在完成重要功能或者结束一天工作之后，提交代码，写好PR，最好每天都有提交
   
   * 确认自己开发项目相关的数据库，以及查询量，配置开发库和生产库。（当前可以通过配置文件区分）
   
   * 确定日志的配置，如果是新的server，在log.conf中，增加新的section，并在configuration.py出初始化logger。所有的调试信息都写到logger中。
   
   * 编写 dao层 中 对应数据库的数据对象的代码，例如 dao/*.py 中的程序代码。完成数据获取的操作
   
   * 然后针对Dao层中的返回的数据，抽象出要处理的对象，构建Objects
   层的内容，定义对象的属性和操作。比如针对我们的业务逻辑，抽象为订单、催收员、通讯录、分单器等，定义不同的属性和方法，在后续需要对订单难度、
   通讯录排序等进行分单的时候，各个对象就能在model层有所联动。需要思考清楚，我们的对象是某一个催收员，还是催收团队，对应会有不同的属性和操作。
   
   * 添加测试用例tests/*.py 中的测试代码
   
   * 写实现业务的 model 层，并且对关键逻辑添加单元测试, 例如 models/nvwa_order_grade.py 
   
   * 指定对应的请求处理的server，并且将 model 添加进入 server 的处理流程. 
   
   * 编写一个调用对应接口的单元测试，检查其是否能够顺利运行，例如 test/services/test_service.py
   
   * 如果有新添加的工具类，添加到utils文件夹
   
   * 补充测试用例，运行其他所有的测试用例，看是否能够运行
   
   * 大量调用接口进行压力测试，看是否会报错
   
   * 上传Git的分支，标记版本（打Tag），完善 readme 文档，部分重要的业务逻辑除了接口文档还要写逻辑文档。
   
   * 有必要的情况注意记录changelog, #TODO, #FIX。如果有#TODO和#FIX的tag，上线前尽量grep检查一下。
   
   
## 注意事项

   * 从Mysql 或者 Mongo 中读取出的中文字符一般是 unicode 格式的，是否需要进行转码需要看实际情况
   * 新建的单元测试的主要思路是先想一个 story 再一步一步 assert
   * 整个代码开发，测试代码的要边写主代码，边写测试代码（一个一个小故事），代码写完之后，要整体运行一遍所有测试用例
   * 压力测试另外创建文件夹或者是写在其他项目中
   * 每个服务需要做到日志分离

## TODO

## Q&A
   

