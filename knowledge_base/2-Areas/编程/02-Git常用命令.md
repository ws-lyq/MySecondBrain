# Git 常用命令速查

## 基础操作
```bash
git init                    # 初始化仓库
git add .                   # 暂存所有文件
git commit -m "消息"        # 提交
git status                  # 查看状态
git log --oneline           # 查看提交历史
```

## 分支管理
```bash
git branch                  # 查看分支
git branch <name>           # 创建分支
git checkout <name>         # 切换分支
git merge <name>            # 合并分支
git branch -d <name>        # 删除分支
```

## 远程操作
```bash
git remote -v               # 查看远程仓库
git push origin master      # 推送到远程
git pull                    # 拉取远程更新
git fetch                   # 获取远程变更（不合并）
```

## 撤销与回退
```bash
git restore <file>          # 撤销工作区修改
git restore --staged <file> # 取消暂存
git reset --soft HEAD~1     # 撤销最近一次提交（保留修改）
git reset --hard HEAD~1     # 彻底回退（丢弃修改）
```

## 历史重写（谨慎使用）
```bash
git commit --amend          # 修改最近一次提交
git rebase -i HEAD~3        # 交互式变基
git push --force-with-lease # 强制推送（安全模式）
```
