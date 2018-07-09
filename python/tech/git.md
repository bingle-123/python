# git笔记
#### 修改提交说明
git commit --amend 可以直接修改上一次commit的消息
#### 提交数据中不小心提交了不该提交的文件
git rm --cached filename  
git commit --amend
#### 差异比较
git diff --word-diff 可以逐子比较  
git add 之后的文件需要通过 git diff --cached 才能看到差异
#### 进度保存
git stash 可以保存和回复工作进度  
在切换工作分支之前执行git stash可以保存工作进度
git stash  
git checkout new_branch  
切回来时用git stash pop
git chekcout old_branch
git stash pop  

## Engine Start
### 别名 
git config --system alias.st status  
git config --system alias.ci commit  
git config --global alias.st status   
### 颜色显示
git config --global color.ui true
### 搜索文件
搜索目录下所有文件  
git grep '匹配的文字'  
#### 提交日志
git log --pretty=fuller   
查看文件详情   
git log -p [filename]   

## 暂存区
git ls-tree -l HEAD 查看暂存区文件  

### git diff
工作区和暂存区  
git diff   
暂存区和HEAD  
git diff --cached  
工作区和HEAD  
git diff HEAD  
## 重置
git reset --hard HEAD^ 重置到上一次提交
### git reset
git reset 会将暂存区清空，工作区不搜影响  
git reset -- filename 将文件改动撤出暂存区，暂存区其它文件不受影响，相当于git add 反向操作  
git reset --soft HEAD^ 不会改变暂存区和工作区，只是改变引用，相当于git commit --amend  
git reset HEAD^  工作区不变，暂存区退回，引用也退回  
git reset --hard HEAD^ 都退回  
### git checkout
git checkout branch 切换分支  
git checkout 汇总显示工作区，暂存区和HEAD差异  
git checkout -- filename用暂存区文件覆盖工作区文件(危险操作)  
git checkout branch -- filename 用branch分支上filename替换工作区，和暂存区对应文件。  
## 恢复进度
git stash 保存暂存区和工作区  
git stash list 显示进度列表  
git stash pop 恢复最新进度  
git stash save 'message' 进度说明
git stash drop 删除一个进度，默认最新进度
git stash clear 删除所有进度  
## 基本操作
### 删除文件
rm filename可以删除工作区文件，但是不会影响暂存区文件，可以使用git checkout filename 从暂存区把文件恢复到工作区。  
git rm 则把工作区和暂存区都删除，但是之前commit中还是可以看到该文件的，git ls-files --with-tree=HEAD^;
### 恢复删除的文件
git cat-file -p HEAD^:filename > filename 或者   
git show HEAD^:filename > filename 或者   
git checkout HEAD^ -- filename   
### 移动文件
git mv oldfile newfile

## git库管理




