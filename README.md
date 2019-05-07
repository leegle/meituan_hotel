## 2019-05-07更新:

数据库新增加一张表，实现这张表同页面同步

另一张表作为历史记录不动

新增加一个写入时间字段

稍微修改一部分逻辑

-

info:
    
最近接的一个私活

采集美团酒店后台的实时订单数据

美团的反爬虫主要体现在:

1. 对ip的限制

2. _token

3. 对cookie的处理-出发滑动验证

##

该程序解决两个问题:

web端: 

查看最近log，已经输入更新后的cookie

爬虫端:

根据cookie，算_token 拿数据，存入mysql里
但凡 cookie一旦失效，向指定用户发短信

### 如何使用

1. 打开web服务

    nohup python3 meituan_web.py &

2. 启动爬虫

    nohup python3 run.py &

