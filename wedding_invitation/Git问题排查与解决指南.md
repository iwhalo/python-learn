# Git问题排查与解决指南

## 问题描述

在执行Git操作过程中遇到以下问题：

1. **推送被拒绝**：远程分支比本地分支更新，导致非快速前进（non-fast-forward）冲突
2. **文件权限问题**：无法删除日志文件（database.log和django.log），显示"Invalid argument"错误
3. **合并失败**：由于日志文件无法删除，导致merge操作失败

## 错误日志分析

```
error: failed to push some refs to 'https://github.com/iwhalo/python-learn.git'
To https://github.com/iwhalo/python-learn.git
 !	refs/heads/master:refs/heads/master	[rejected] (non-fast-forward)

hint: Updates were rejected because the tip of your current branch is behind
hint: its remote counterpart. If you want to integrate the remote changes,
hint: use 'git pull' before pushing again.

error: unable to unlink old 'wedding_invitation/logs/database.log': Invalid argument
error: unable to unlink old 'wedding_invitation/logs/django.log': Invalid argument
Merge with strategy ort failed.
```

## 解决方案

### 方案一：常规解决步骤

#### 1. 处理本地日志文件冲突

```bash
# 删除有问题的日志文件
del wedding_invitation\logs\database.log
del wedding_invitation\logs\django.log

# 如果目录为空，也删除目录
rmdir wedding_invitation\logs
```

#### 2. 同步远程更改

```bash
# 从远程获取最新更改
git fetch origin
git pull origin master
```

#### 3. 提交并推送更改

```bash
# 如果有冲突，解决后提交
git add .
git commit -m "resolve conflicts after pulling remote changes"

# 最后推送更改
git push origin master
```

### 方案二：从Git历史中完全移除日志文件

#### 1. 停止跟踪日志文件

```bash
# 从Git中移除已被跟踪的日志文件
git rm --cached wedding_invitation/logs/database.log
git rm --cached wedding_invitation/logs/django.log

# 如果整个logs目录都被跟踪了，也需要移除
git rm -r --cached wedding_invitation/logs/
```

#### 2. 确保 .gitignore 配置正确

确认 `.gitignore` 文件中包含以下内容：

```
# 日志文件
**/logs/
**/logs/*.log
*.log

# Django 相关
db.sqlite3
local_settings.py

# Python 相关
__pycache__/
*.py[cod]
*$py.class
*.so
.Python

# 其他临时文件
.DS_Store
Thumbs.db
```

#### 3. 提交并推送更改

```bash
git add .gitignore
git commit -m "移除日志文件并更新.gitignore"
git push origin master
```

### 方案三：彻底清理Git历史（谨慎使用）

如果日志文件仍存在于远程仓库的历史中，可使用此方法：

```bash
# 使用filter-branch从整个历史记录中删除这些文件
git filter-branch --force --index-filter \
"git rm --cached -r --ignore-unmatch wedding_invitation/logs/*" \
--prune-empty --tag-name-filter cat -- --all

# 清理并回收空间
git for-each-ref --format="delete %(refname)" refs/original | git update-ref --stdin

# 推送清理后的历史到远程仓库
git push origin --force --all
git push origin --force --tags
```

> **警告**：使用 `filter-branch` 会重写历史记录，这会影响其他协作者，所以只在必要时使用，并提前通知团队成员。

## 预防措施

1. **确保 .gitignore 配置正确**：在项目开始时就正确配置 `.gitignore` 文件
2. **定期检查**：使用 `git status` 检查是否有不应该被跟踪的文件
3. **使用 `git rm --cached`**：对于意外被跟踪的文件，使用此命令从Git中移除但保留本地文件

## 参考信息

- 项目使用 `.gitignore` 配置忽略日志文件
- 已将 `wedding_invitation/logs/` 目录下的日志文件（如 `database.log`、`django.log`）添加到忽略列表
- 防止被Git追踪，避免类似问题再次发生