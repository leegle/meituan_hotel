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