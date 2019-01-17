## 这是干什么用的

爬取电影的**在线免费观看**地址以及概述

## DEMO

![21793-0jhq4kiswmwj.png](https://overfit-photo-1257758577.cos.ap-guangzhou.myqcloud.com/2019/01/17/1547656352.png)

## 实现原理

爬取[疯狂影院](http://overfit.ml/index.php/go/aHR0cDovL3d3dy5pZmtkeS5jb20v)的电影资源，如下

![12035-j5nxexiqr8a.png](https://overfit-photo-1257758577.cos.ap-guangzhou.myqcloud.com/2019/01/17/1547656537.png)

## IO

- i: 电影名字
- o: mission config + result

```bush
Mission Config
------------------------
Movie Name: 2001
Total Movie: 174
Succeed Catch:  133
Failed Catch: 41
------------------------
```

## 架构

```bush
仅供参考
|---User Connfig
|---Initialize
|---Get input
|---Main Program
         |---Main Loop
                 |---Sub Loop
|---Memorize
```

<center>☀更多信息请访问我的博客 [OverFit Blog ](http://overfit.ml) ☀</center>

