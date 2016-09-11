import socket

class Client():
    s = socket.socket()
    
    def start(self,ip,port):
        if not self.connect(ip,port):
            print("Unable to connect...")
            return
        print("Connected")
        self.gameLoop()

    def connect(self,ip,port):
        try:
            self.s.connect((ip,port))
        except:
            return False
        return True
    
    def gameLoop(self):
        print("Starting game")
        s = self.s
        s.setblocking(0)
        try:
            while 1:
                try:
                    rec = str(s.recv(1),"utf8")
                except:
                    continue
                if rec == "q":
                    print("Terminating...")
                    break
                self.showFlag()
                self.waitForPress()
                self.hideFlag()
                s.send(bytes("p","utf8"))
        except KeyboardInterrupt:
            print("Terminating")

    def waitForPress(self):
        input()
        return True
    
    def showFlag(self):
        print("Showing flag")

    def hideFlag(self):
        print("Hiding flag")
        

cli = Client()
cli.start("192.168.5.101",12345)

    

