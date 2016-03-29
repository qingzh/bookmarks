##### 需求

轮询 ERROR 日志文件，如果发现最近5分钟内有新的 ERROR 信息，则发出邮件提醒

##### 实现

查看最近5分钟更新的 ERROR 日志:
```bash
find *.ERROR -mmin -5
```

日志格式如下:
```
2016-03-29 14:02:18,629 ERROR [http-bio-18002-exec-129] ReqUserFilter:74 requserfilter error
com.test.exception.AuthException: 内部错误: user has not logged in
    at com.***.INTERNAL(***.java:114)
    at com.***.preHandle(***.java:85)
    at com.***.doFilter(***.java:64)
```

获取最后一条 Exception 内容长信息：
```bash
(find *.ERROR -mmin -5 | xargs -I{} tac {} | grep -m1 -B1000 '^[0-9]' | tac) 2>/dev/null 
```

获取最后一条 Exception 内容短信息：
```bash
(find *.ERROR -mmin -5 | xargs -I{} tac {} | grep -m1 '^[0-9]' | cut -d']' -f2) 2>/dev/null 
```

去掉前后空格以及空行, 类似 trim():
```bash
echo -e '  test \n test \n\n ' | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//' -e '/^[[:space:]]*$/d'
```

简单的轮询和发送报警脚本:
```bash
data=`(find *.ERROR -mmin -5 | xargs -I{} tac {} | grep -m1 -B1000 '^[0-9]' | tac | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//'  -e '/^[[:space:]]*$/d') 2>/dev/null`
if [ ${#data} -gt 0 ]; then
      url="http://localhost:9970/m/alarm/send?alarmType=1"
      curl -v -G --data-urlencode "message=$data" --data-urlencode "receiver=$receiver" "$url"
fi
```
这里的 "/m/alarm/send" 接口会发送邮件到指定邮箱