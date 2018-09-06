from socket import socket,AF_INET,SOCK_STREAM
from threading import Thread
from ast import literal_eval

class Server:

    HOST = '0.0.0.0'
    PORT = 8001
    s=socket(AF_INET,SOCK_STREAM)
    connections=[]
    def __init__(self):   
        self.s.bind((self.HOST, self.PORT))
        self.s.listen(5)   
        print ('Server start at: %s:%s' %(self.HOST, self.PORT))
        print ('wait for connection...')

    def getuserid(self,token):
        file=open("login.txt")
        logins=literal_eval(file.read())
        userid=logins[id]
        file.close()
        return userid

    def dictostr(self,d):
        s="{"
        for k,v in d.items():
            if not s=="{":
                s+=","
            if type(v)==list:
                s=s+"\""+k+"\":"+self.listtostr(v)
            elif type(v)==str:
                s=s+"\""+str(k)+"\""+":"+"\""+str(v)+"\""
        s+="}"
        return s

    def listtostr(self,l):
        s="["
        for i in l:
            if not s == "[":
                s+=","
            s=s+"\""+i+"\""
        s+="]"
        return s

    def register(self,connection,id,password):
        try:
            file=open("register.txt")
            r=file.read()
            regs=r.split(";")
            for reg in regs:    
                user=literal_eval(reg)
                if user["id"] ==id:
                    connection.send(bytes("{\"status\": 1,\"message:\" " + id + " is already used}",'utf-8'))
                    break
            if not r == "":
                r+=";"
            r=r+"{"+"\"id\":\""+id+"\",\"password\":\""+password+"\",\"friend\":[],\"invite\":[]}"
            file.write(r)
            connection.send(bytes("{\"status\": 0}",'utf-8'))
        finally:
            file.close()

    def delete(self,connection,id,password):
        try:
            userid=self.getuserid(id)
            file=open("register.txt")
            r=file.read()
            regs=r.split(";")
            for reg in regs:
                rdic=literal_eval(reg)
                if rdic["id"]==userid:
                    regs.remove(reg)
            s=""
            for i in regs:
                if not s=="":
                    s+=";"
                s+=i
            file.write(s)
        finally:
            file.close()

    def login(self,connection,id,password):
        print("")

    def logout(self,connection,id):
        file=open("login.txt")
        logins=literal_eval(file.read())
        del logins[id]
        s=self.dictostr(logins)
        file.write(s)
        file.close()
    
    def invite(self,connection,user,id):
        print("")
    def list_invite(self,connection,user):
        print("")
    def accept_invite(self,connection,user,id):
        print("")
    def list_friend(self,connection,user):
        print("")
    def post(self,connection,user,message):
        userid= self.getuserid(id)
        file=open("post.txt")
        posts=file.read()
        if not posts=="":
            posts+=";"
        posts=posts+"{\""+userid+"\":\""+message+"\"}"
        file.write(posts)
    def receive_post(self,connection,user):
        print("")

    def HandleCommand(self,connection,command):
        if command[0]=="register":
            self.register(connection,command[1],command[2])
        elif command[0]=="delete":
            self.delete(connection,command[1],command[2])
        elif command[0]=="login":
            self.login(connection,command[1],command[2])
        elif command[0]=="logout":
            self.logout(connection,command[1])
        elif command[0]=="invite":
            self.invite(connection,command[1],command[2])
        elif command[0]=="list_invite":
            self.list_invite(connection,command[1])
        elif command[0]=="accept_invite":
            self.accept_invite(connection,command[1],command[2])
        elif command[0]=="list_friend":
            self.list_friend(connection,command[1])
        elif command[0]=="post":
            self.post(connection,command[1]," ".join(command[2:]))
        elif command[0]=="receive_post":
            self.receive_post(connection,command[1])
     
    def handler(self,connection ,address):
        #global connections
        while True:
            data=connection.recv(1024)
            print(str(data,'utf-8'))
            self.HandleCommand(connection,str(data).split())
            """
            for conn in self.connections:
                conn.send(bytes("Hello",'utf-8'))
            if not data :
                self.connections.remove(connection)
                connection.close()
                break
            """

    def run(self):   
        while True:
            conn, addr = self.s.accept()
            sThread=Thread(target=self.handler,args=(conn,addr))
            sThread.daemon=True
            sThread.start()
            print ('Connected by ', addr)
            self.connections.append(conn)

Server=Server()
Server.run()