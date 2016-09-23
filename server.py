import socket, random, time

class Server():
    s = socket.socket()
    clients = []

    def startServer(self,ip,port):
        self.s.bind((ip,port))
    
    def connectClients(self,count):
        self.s.listen(5)
        self.s.setblocking(0)
        print("Waiting for "+str(count)+" clients to connect")
        self.clients = []
        try:
            while len(self.clients) < count:
                try:
                    client,addr = self.s.accept()
                    self.clients.append((client,addr))
                    print("Connected client #%s at address %s" %(len(self.clients),addr))
                except:
                    pass
                
        except KeyboardInterrupt:
            self.s.setblocking(1)
            print("Canceled, currently connected %s clients"%(len(self.clients)))
        self.s.listen(0)

    def playGame(self,difficulty,timeout=60):
        clients = self.clients
        if(len(clients) < 2):
            print("At least 2 clients required to play!")
            return
        
        lastClient = None
        clientIndex = 0
        startedTime = time.time()
        for i in range(difficulty):            
            if lastClient != None:
                while 1:
                    clientIndex = random.randint(0,len(clients)-1)
                    if clientIndex != lastClient:                        
                        break
            lastClient = clientIndex
            print("Round %s, client #%s"%(i,clientIndex))
            c = clients[clientIndex][0]
            c.send(b"p")
            if not self.waitForClient(c,timeout):
                print("Too slow!")
                break
        finishTime = time.time() - startedTime
        print("Finished in %s seconds" %(finishTime))

    def waitForClient(self,c,timeout):     
        c.setblocking(0)
        sendedTime = time.time()
        while sendedTime > time.time() - timeout:
            try:
                c.recv(1)
                c.setblocking(1)
                return True
            except:
                pass
        return False
                  
        
        
        
srv = Server()
srv.startServer("192.168.0.104",12345)
srv.connectClients(3)
srv.playGame(5)
