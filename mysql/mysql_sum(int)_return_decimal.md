在 mysql 中 sum(int) 返回的是浮点类型, 参考 mysql 官方文档:
[12.16.1 GROUP BY (Aggregate) Function Descriptions](http://dev.mysql.com/doc/refman/5.0/en/group-by-functions.html)

如果需要返回整型，需要使用 CAST
```sql
SELECT CAST(SUM(n) AS SIGNED) n FROM table;
```