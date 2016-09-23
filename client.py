import socket, machine

class Client():
    s = socket.socket()

    def __init__(self):
        self.servo = machine.PWM(machine.Pin(12))
        self.servo.freq(50)
        self.servo.duty(60)
        self.btn = machine.Pin(4, machine.Pin.IN, machine.Pin.PULL_UP)

    
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
        val = self.btn.value()
        while val == self.btn.value():
            pass
        
        return True
    
    def showFlag(self):
        print("Showing flag")
        self.servo.duty(105)

    def hideFlag(self):
        print("Hiding flag")
        self.servo.duty(60)
        



    

