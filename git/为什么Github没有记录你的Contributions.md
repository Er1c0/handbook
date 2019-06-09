[为什么Github没有记录你的Contributions
](https://segmentfault.com/a/1190000004318632)
[why-are-my-contributions-not-showing-up-on-my-profile](https://help.github.com/en/articles/why-are-my-contributions-not-showing-up-on-my-profile)

# 强制更新Git历史

[Changing author info](https://help.github.com/en/articles/changing-author-info)

1. 复制粘贴脚本，并根据你的信息修改以下变量：旧的Email地址，正确的用户名，正确的邮件地址
```
#!/bin/bash
git filter-branch --env-filter '

OLD_EMAIL="li.changzhen@163.com"
CORRECT_NAME="perfectstorm88"
CORRECT_EMAIL="perfectstorm88@163.com"

if [ "$GIT_COMMITTER_EMAIL" = "$OLD_EMAIL" ]
then
    export GIT_COMMITTER_NAME="$CORRECT_NAME"
    export GIT_COMMITTER_EMAIL="$CORRECT_EMAIL"
fi
if [ "$GIT_AUTHOR_EMAIL" = "$OLD_EMAIL" ]
then
    export GIT_AUTHOR_NAME="$CORRECT_NAME"
    export GIT_AUTHOR_EMAIL="$CORRECT_EMAIL"
fi
' --tag-name-filter cat -- --branches --tags
```
2. 执行文件
3. 用git log命令看看新 Git 历史有没有错误
4. 把正确历史 push 到 Github
```
git push --force --tags origin 'refs/heads/*'
```