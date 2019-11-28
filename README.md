# DataXWeb

DataXWeb基于DataX,DataX 是阿里巴巴集团内被广泛使用的离线数据同步工具/平台，实现包括 MySQL、Oracle、SqlServer、Postgre、HDFS、Hive、ADS、HBase、TableStore(OTS)、MaxCompute(ODPS)、DRDS 等各种异构数据源之间高效的数据同步功能


### 计划
1. 任务调度
2. 运行监控
3. 模板引擎
4. 实时日志
5. 多类型数据库支持
6. 定时任务(全量|增量)
7. 报警设置
8. 邮件配置
9. 用户管理
10. 权限管理
11. 使用文档说明
12. 数据库sql执行
13. 统计分析及报表
14. 智能AI
15. Http Server
16. 单机多线程运行
17. 单机多进程运行
18. 分布式运行
19. 混合模式运行（Yarn+多进程模式运行）
20. 自动伸缩运行
21. 负载均衡及任务锁机制
22. Mysql数据库存放应用数据
23. 网页端修改并持久化job配置的json到数据库
24. 网页端实时查看抽取日志，类似Jenkins的日志控制台输出功能
25. job运行记录展示，页面操作停止datax作业（开发中）
26. 网页端各种读写插件模板生成，可以在页面组装使用
27. 实现部分写插件支持自动建表功能

### 环境


### 安装


### 操作步骤

+ 启动
gunicorn -b 0.0.0.0:5001 -D run:app

### 举个栗子

```
admin/ [name='index']
admin/ login/ [name='login']
admin/ logout/ [name='logout']
admin/ password_change/ [name='password_change']
admin/ password_change/done/ [name='password_change_done']
admin/ jsi18n/ [name='jsi18n']
admin/ r/<int:content_type_id>/<path:object_id>/ [name='view_on_site']
admin/ auth/group/
admin/ backend/dataxuserprofile/
admin/ backend/dataxconfig/
admin/ backend/dataxnav/
admin/ admin/logentry/
admin/ backend/dataxjobscheduler/
admin/ backend/dataxtask/
admin/ ^(?P<app_label>auth|backend|admin)/$ [name='app_list']
```

```
增量同步实现
实现增量同步需要在表中增加一个时间戳字段，如update_time，在同步配置文件中，通过where条件，根据时间戳字段筛选当前时间向前一段时间内的增量数据。

json文件中，${start_time}和${end_time}为调用datax.py时传入的参数
datax/bin/datax.py ../../mysql2mysql.json -p "-Dstart_time=1546337137 -Dend_time=1546337237"

{
    "job": {
        "content": [
            {
                "reader": {
                    "name": "mysqlreader", 
                    "parameter": {
                        "column": [
                        "doc_id","title","file_path","approval_id","page_count","version"
                        ], 
                        "connection": [
                            {
                                "jdbcUrl": ["jdbc:mysql://192.168.81.1:3306/bootdo?useUnicode=true&characterEncoding=utf8"], 
                                "table": ["es_approval_doc"]
                            }
                        ], 
                        "password": "123456", 
                        "username": "root",
                        "where": "version > FROM_UNIXTIME(${start_time}) and version < FROM_UNIXTIME(${end_time})",
                    }
                }, 
                "writer": {
                    "name": "mysqlwriter", 
                    "parameter": {
                        "column": [
                        "doc_id","title","file_path","approval_id","page_count","version"
                        ], 
                        "writeMode":"update",
                        "connection": [
                            {
                                "jdbcUrl": "jdbc:mysql://192.168.81.1:3306/bootdo?useUnicode=true&characterEncoding=utf8", 
                                "table": ["es_approval_doc_copy"]
                            }
                        ], 
                        "password": "123456", 
                        "username": "root"
                    }
                }
            }
        ], 
        "setting": {
            "speed": {
                "channel": "1"
            }
        }
    }
}

定时同步实现
定时同步可以采用操作系统的定时任务+shell脚本实现。以下为在linux系统中的方案：

1、编写shell脚本，命名为syntask.sh：
#!/bin/bash
# source /etc/profile
# 截至时间设置为当前时间戳
end_time=$(date +%s)
# 开始时间设置为120s前时间戳
start_time=$(($end_time - 120))
# datax/bin/datax.py ../../mysql2mysql.json -p "-Dstart_time=$start_time -Dend_time=$end_time"
这里通过脚本获取用于筛选条件中的开始时间start_time和结束时间end_time，将两个时间作为参数传给datax.py。

2、在crontab中，添加任务计划：
$crontab -e
* */1 * * * /syntask.sh
DataX不适合实时数据同步或太频繁的定时同步，因为同步都需要去读取源表，频率过大对源表会造成压力。
此外，最好每次增量同步的时间段比定时任务时间间隔大一些，以保证所有时间产生的数据都被覆盖到。

异常情况下的补救措施：
如果某段时间内由于服务器、操作系统、网络等原因造成某个时间段内数据没有正常同步，那么可以通过手动执行同步的方式进行补救，执行同步时，将筛选的时间段加大大覆盖异常发生的整个时间段。


多表同步实现
通常我们的业务系统存在有多个表，表之间有外键关系。为实现多表的数据同步，我们需要理清外键依赖关系，为每个表分别编写json同步配置文件，并按外键依赖关系逐个调用datax.py。
如对于主表es_approval和子表es_approval_doc，可以对应写两个json配置文件：mysql2mysql-approval.json和mysql2mysql-approval-doc.json，在syntask.sh中先调用主表配置文件，再调用子表配置文件。

#!/bin/bash
source /etc/profile
# 截至时间设置为当前时间戳
end_time=$(date +%s)
# 开始时间设置为120s前时间戳
start_time=$(($end_time - 3600))
/datax/bin/datax.py /mysql2mysql-approval.json -p "-Dstart_time=$start_time -Dend_time=$end_time" 
/datax/bin/datax.py /mysql2mysql-approval-doc.json -p "-Dstart_time=$start_time -Dend_time=$end_time"


多级多路同步
要实现多级同步，可以在每两级之间搭建一个datax实例实现这两级之间的数据同步。
要实现多路同步，可以为同一个表编写多个配置文件，向多个目标库同步。
```

