# oracle 执行分析

## 分析过程
- 执行解析计划
- 语法
```sql
explain plan for
${sql-body}
```
- 举例
```sql
explain plan for
select * from sys_user
```
- 查看解析计划
```sql
SELECT * 
FROM table(dbms_xplan.display)
```

