# 分布式与云计算

## 授课老师

丁菁

## 课程介绍

讲解分布式系统和云计算。

## 实验

两个实验二选一

- 本地虚拟机Hadoop
- 阿里PaaS_云计算

老师会提供实验文档，跟着指导做完实验。

## 资料

学长做的非常齐全的笔记

https://keyanjie.net/studynote-of-distributed-system/

一位同学做的笔记

https://www.yuque.com/mamudechengxuyuan/tbytf5

## 考试

只有期末考试，闭卷

全英题目，老师会使用很多国外卷子的题目

50分选择题

50分简答题

## 资料

CMU试卷例题

```C
(d) A scheme for implementing at-most-once reliable message delivery usessynchronized clocks to reject duplicate messages.Processes place their local clock value(a timestamp) in the messages they send.Each receiver keeps a table giving,
for each sending process,the largest message timestamp it has seen.Assume that clocks are synchronized to within 100ms, and that messages can arrive at most 50ms after transmission(15pts)
(i) When may a process ignore a message bearing a timestamp T, if it has recordedthe last message received from that process as having timestamp T?(5pts)
If T≤T' then the message must be a repeat.
(ii) When may a receiver remove a timestamp 175,000(ms) from its table?(Hint：use the receiver's local clock value.) (5pts)
The earliest message timestamp that could stil arrive when the receiver's clock is r is r-100-50.If this is to beat least 175,000(so that we can not mistakenly receive a duplicate) ,we need r-150=175,000， i.e.r=175,150.
(iii) Should the clocks be internally synchronized or externally synchronized ?(5pts)
Internal synchronization will suffice， since only tie differences are relevant.
```

## 复习方法

看PPT和笔记

重点内容

- 同步
- 一致性
- 容错
- GFS和MapReduce

---

以上内容为铖哥口述由小铭撰写

感谢黑兄提供的博客网址

