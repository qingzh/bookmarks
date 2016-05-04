Shell 里实现字典

```
# 定义key
c="key"
# 定义value: 数组
d=(128 145)
# b[c] or b[$c]: both OK
b[c]=${d[*]}
# ${b[c]} or ${b[$c]}: both OK
echo ${b[c]}
echo ${b['key']}
# 反解析value
dd=(${b['key']})
echo ${f[1]}
```

执行过程如下：
```
$ sh -x sh_dict.sh
+ c=key
+ d=(128 145)
+ b[c]='128 145'
+ echo 128 145
128 145
+ echo 128 145
128 145
+ dd=(${b['key']})
+ echo
```
