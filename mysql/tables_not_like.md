以下这条语句:
```sql
show tables not like "%stat%"
```
MySql会抛出语法错误 syntax error

要实现类似请求，需要使用：
```sql
SELECT table_name FROM information_schema.tables WHERE table_schema = 'dbname' AND table_name NOT LIKE "%stat%";
```
