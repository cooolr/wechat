import os
import rpyc

c=rpyc.connect("127.0.0.1", 50322)
while True:
    reply = input()
    c.root.input(reply)
    if reply and reply[0] == "!":
        os.system(reply.strip("!"))
c.close()