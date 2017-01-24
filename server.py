import socket, random, time, sys, traceback
from pygame_stopwatch import StopWatch


class Server():
    s = socket.socket()
    clients = []

    STOPWATCH_ENABLED = True

    def __init__(self):
        self.running = False

        if self.STOPWATCH_ENABLED:
            self.stopwatch = StopWatch()


    def startServer(self,ip,port):
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
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

    def playGame(self,difficulty,timeout=40):
        self.running = True

        clients = self.clients
        if(len(clients) < 2):
            print("At least 2 clients required to play!")
            return
        #raw_input("Press enter to start")
        lastClient = None
        clientIndex = 0

        if self.STOPWATCH_ENABLED:
            self.stopwatch.startStopWatch()


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

        if self.STOPWATCH_ENABLED:
            self.stopwatch.stopStopWatch()
        finishTime = time.time() - startedTime
        print("Finished in %s seconds" %(finishTime))
        time.sleep(3)

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



if len(sys.argv) >= 2:
    number_of_clients = int(sys.argv[1])    # First commandline parameter is number of clients
else:
    number_of_clients = 3

if len(sys.argv) >= 3:
    number_of_rounds = int(sys.argv[2])      # Second commandline parameter is number of rounds
else:
    number_of_rounds = 20

print ("%s clients, %s rounds" % (str(number_of_clients), str(number_of_rounds)))


srv = Server()
srv.startServer("172.16.34.74",12345)
srv.connectClients(number_of_clients)

srv.running = True
while srv.running:

    try:

        srv.playGame(number_of_rounds)


    except:
        srv.running = False
        srv.s.close()
        print("closing connections")

        if srv.STOPWATCH_ENABLED:
            srv.stopwatch.stopStopWatch()

    """
    except KeyboardInterrupt:
        answer = input("Do you wanna play again?")

        if answer:
            # Starts new game

            if srv.STOPWATCH_ENABLED:
                srv.stopwatch.stopStopWatch()


        else:

            srv.stopwatch.stopStopWatch()
            srv.running = False
            srv.s.close()
            print("closing connections")

    """









