from socket import socket,AF_INET,SOCK_STREAM
from threading import Thread
import sys
from ast import literal_eval

class Client:
    Token=""
    login=False
    
    s=socket(AF_INET,SOCK_STREAM)
    
    def SendCmd(self):
        while True:
            cmd=input("")
            if "register" in cmd or "login" in cmd : 
                self.s.send(bytes(cmd,'utf-8'))
            elif "exit" in cmd.lower():
                print("Exit")
                sys.exit()
            else:
                if self.login :    
                    if "delete" in cmd :
                        self.Token=""
                        self.login=False
                    
                else :
                    print("Not log in yet")    
    
    def __init__(self):
        #HOST = input('Enter host: ')
        #PORT = input('Enter port: ')
        #if not PORT:
        #    PORT = 8001  # Default value.
        #else:
        #    PORT = int(PORT)
        HOST = '0.0.0.0'
        PORT = 8001
        self.s.connect((HOST, PORT))
        cThread=Thread(target=self.SendCmd)
        cThread.daemon=True
        cThread.start()
        while True:
            data = self.s.recv(1024)
            if not data:
                break
            print(str(data,'utf-8'))
            d=literal_eval(str(data,'utf-8'))
            if d["status"] == 1 :
                print (d["message"])
            else:
                if "token" in d:
                    self.login=True
                    self.token=d["token"]
                if "invite" in d:
                    inv=d["invite"]
                    print(*inv , sep=",")
                if "friend" in d:
                    fri=d["friend"]
                    print(*fri , sep=",")
                if "post" in d:
                    post=d["post"]
                    p=""
                    for i in post:
                        p+=post["id"]
                        p+=" : "
                        p+=post["message"]
                        p+="\n"
                    print(i)

Client=Client()
