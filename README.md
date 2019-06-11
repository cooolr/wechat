# wechat
> Power By https://github.com/littlecodersh/ItChat

### 命令行微信聊天 -- wechat.py

使用方法:

python wechat.py  --> 等待弹出二维码，扫描登陆

1. 直接输入文本回车，即可发送消息给默认联系人
2. 发送消息给指定联系人， 用 | 分割联系人和文本消息  -->  测试群聊|你们在干嘛
3. 屏幕会打印所有联系人和指定群聊的消息
4. 打印出来的消息在昵称前面有序号排序，可以用序号便捷回复  -->  0|你们在干嘛
5. 文本消息为screen时，即可发送指定路径中最新的图片
6. 文本消息为!开头的将被os.system执行
7. 指定的群聊需要确认是否已保存到通讯录
8. 新消息的打印会打断正在输入的文本显示，盲打完回车发送即可




### 命令行微信聊天多窗口 -- wechats.py / wechatc.py

使用方法:
python wechats.py  --> 等待弹出二维码，扫描登陆

python wechatc.py  --> 接受文本输入

1. 直接输入文本回车，即可发送消息给默认联系人
2. 发送消息给指定联系人， 用 | 分割联系人和文本消息  -->  测试群聊|你们在干嘛
3. 屏幕会打印所有联系人和指定群聊的消息
4. 打印出来的消息在昵称前面有序号排序，可以用序号便捷回复  -->  0|你们在干嘛
5. 文本消息为screen时，即可发送指定路径中最新的图片
6. 文本消息为!开头的将被os.system执行
7. 指定的群聊需要确认是否已保存到通讯录

在linux下结合tmux使用多窗口效果最佳
```
sudo apt-get install zsh tmux
```

> vim ~/.tmux.conf
```
# 允许鼠标
set -g mouse on
set -g default-command /bin/zsh
```

第一次使用zsh需要命令行输入zsh，进行初始化动作

1. 输入tmux进入tmux模式
2. tmux上下分屏
```
ctrl + b + "
```
