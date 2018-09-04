from socket import socket,AF_INET,SOCK_STREAM
from threading import Thread

class Client:

    Login=False
    
    s=socket(AF_INET,SOCK_STREAM)
    
    def SendCmd(self):
        while True:
            cmd=input("")
            if "register" in cmd or self.Login: 
                self.s.send(bytes(cmd,'utf-8'))
            else:
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

Client=Client()
