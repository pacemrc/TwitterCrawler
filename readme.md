# 功能
下载单个推特用户的所有媒体数据并生成一份媒体数据表格
# 使用
## 安装依赖
```
pip install -r requirement.txt
```

## 修改内容

1. 替换Cookie
将Config.InitConfig.py文件的twitter_headers替换

2. 替换请求URL
将Config.InitConfig.py的`userInfoUrl`和`mediaInfoUrl`,这两个url推特服务端会定期更新
打开浏览器开发者工具Network过滤关键字`UserByScreenName`和`UserMedia`

3. 替换代理
Config.InitConfig.py的proxy

# 原理

