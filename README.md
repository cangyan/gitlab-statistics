# 简介
统计gitlab个人代码量

# 使用方法
## 构建镜像
```
docker build -t gitlab .
```

## 执行命令

```
export GIT_TOKEN=******** //你的access_token
export GIT_HOST=https://git.***.*** //你的对应git域名
export AUTHOR_EMAIL=***@email.com //多个逗号隔开
export START_TIME=2020-09-01T00:00:00Z
export END_TIME=2020-10-01T00:00:00Z
export GIT_PROJECT= //留空为拉取全部，指定项目名，多个逗号隔开
export GIT_BRANCH= //留空为拉取全部，指定分支名，多个逗号隔开
export LOCAL_OUTPUT=/tmp //本地保存路径

docker run -e token=$GIT_TOKEN \
-e host=$GIT_HOST \
-e author_email=$AUTHOR_EMAIL \
-e start_time=$START_TIME \
-e end_time=$END_TIME \
-e project=$GIT_PROJECT \
-e branch=$GIT_BRANCH \
-it \
--mount type=bind,source=$LOCAL_OUTPUT,target=/output gitlab
```