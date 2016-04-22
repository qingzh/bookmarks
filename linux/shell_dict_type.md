Shell 里实现字典

```
# 
c="cpc"
# 定义数组
d=(128 145)
b[c]=${d[*]}
echo ${b[c]}
echo ${b['cpc']}
# 反解析数组
dd=(${b['cpc']})
echo ${f[1]}
```