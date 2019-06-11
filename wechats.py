# -*- coding: utf-8 -*-
"""
命令行微信聊天多窗口 -- wechat_server

使用方法:
python wechat_server.py  --> 等待弹出二维码，扫描登陆
python wechat_client.py  --> 接收输入，配合tmux多窗口使用

1. 直接输入文本回车，即可发送消息给默认联系人
2. 发送消息给指定联系人， 用 | 分割联系人和文本消息  -->  测试群聊|你们在干嘛
3. 屏幕会打印所有联系人和指定群聊的消息
4. 打印出来的消息在昵称前面有序号排序，可以用序号便捷回复  -->  0|你们在干嘛
5. 文本消息为screen时，即可发送指定路径中最新的图片
6. 文本消息为!开头的将被os.system执行
7. 指定的群聊需要确认是否已保存到通讯录

Power By https://github.com/littlecodersh/ItChat
"""

import re
import os
import time
import rpyc
import itchat
import threading
from rpyc import Service
from rpyc import ThreadedServer


# 默认联系人, 备注或微信名 [需要修改]
nickname = "ie6"
# 允许接收消息的群聊 [需要修改]
GroupChat = ["°ο°°ο°°ο°", "活捉那个小涂"]
# 指定发送截图的路径 [需要修改]
Pictures = "C:\\Users\\lr\\Pictures"
# 联系人活群聊排序，序号回复 [无需修改]
NickList = []
# 允许接收的消息类型 [无需修改]
ContentType = ['Text', 'Map', 'Card', 'Sharing', 'Picture', 'Recording', 'Video', 'Friends']


def get_new_file(path):
    """
    按修改时间排序文件，返回最新只读二进制文件
    """
    files = [os.path.join(path,i) for i in os.listdir(path) if i and i[0] != "."]
    files.sort(key = lambda x:os.path.getmtime(x))
    return open(files[-1], "rb")


@itchat.msg_register(ContentType)
def text_reply_friend(msg):
    """
    处理私聊消息
    """
    global NickList
    ctime = time.ctime()[11:19]
    # 获取发送人的昵称
    temp_nickname = [i for i in itchat.get_friends() if i["UserName"]==msg["FromUserName"]][0]
    temp_nickname = temp_nickname["RemarkName"] if temp_nickname["RemarkName"] else temp_nickname["NickName"]
    # 联系人排序
    if not temp_nickname in NickList:
        NickList.append(temp_nickname)
    # 打印非文本消息类型
    if msg["MsgType"] != 1:
        msg.text = "[{}]".format(msg["Type"])

    text = "{} {}[{}]: {}".format(ctime, NickList.index(temp_nickname), temp_nickname, msg.text)
    print(text)


@itchat.msg_register(ContentType, isGroupChat=True)
def text_reply_groupchat(msg):
    """
    处理群聊消息
    """
    global NickList
    ctime = time.ctime()[11:19]
    if not msg["User"]["NickName"] in GroupChat:
        return
    temp_nickname = "{} - {}".format(msg["User"]["NickName"], msg["ActualNickName"])
    # 联系人排序
    if not msg["User"]["NickName"] in NickList:
        NickList.append(msg["User"]["NickName"])
    # 打印非文本消息类型
    if msg["MsgType"] != 1:
        msg.text = "[{}]".format(msg["Type"])

    text = "{} {}[{}]: {}".format(ctime, NickList.index(msg["User"]["NickName"]),  temp_nickname, msg.text)
    print(text)


def auto_login():
    """
    被抛弃的登陆线程
    """
    global itchat,username
    itchat.auto_login(hotReload=True)
    username = [i["UserName"] for i in itchat.get_friends() if i["NickName"]==nickname][0]
    itchat.run()


class Wechat(Service):
    def exposed_input(self, reply):
        global itchat
        if not reply:
            return
        # 指定联系人操作
        if "|" in reply:
            temp_nickname,reply = reply.split("|")
            # 从序号列表里取出联系人昵称
            if NickList and temp_nickname.isdigit():
                temp_nickname = NickList[int(temp_nickname)]
            # 获取群聊昵称username
            if temp_nickname in GroupChat:
                try:
                    temp_username = [i["UserName"] for i in itchat.get_chatrooms() if i["NickName"]==temp_nickname][0]
                except:
                    print("找不到指定群聊: {}".format(temp_nickname))
                    return
            # 获取私聊联系人昵称
            else:
                try:
                    temp_username = [i["UserName"] for i in itchat.get_friends() if temp_nickname in (i["NickName"], i["RemarkName"])][0]
                except:
                    print("找不到指定联系人: {}".format(temp_nickname))
                    return
        # 执行!开头文本命令
        elif "!" == reply[0]:
            os.system(reply.strip("!"))
            return
        # 默认联系人操作
        else:
            temp_nickname = nickname
            temp_username = username

        if reply == "screen":
            itchat.send_image(toUserName=temp_username, file_=get_new_file(Pictures))
        else:
            itchat.send_msg(reply, toUserName=temp_username)
        print("{} -> [{}]: {}".format(time.ctime()[11:19], temp_nickname, reply))



if __name__ == "__main__":
    threading._start_new_thread(auto_login, ())
    s = ThreadedServer(Wechat, port=50322, auto_register=False)
    s.start()
