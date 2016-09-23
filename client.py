import socket, machine, time

class Client():
    s = socket.socket()

    def __init__(self):
        self.servo = machine.PWM(machine.Pin(12))
        self.servo.freq(50)
        self.servo.duty(60)
        self.btn = machine.Pin(4, machine.Pin.IN, machine.Pin.PULL_UP)
        self.led = machine.Pin(2, machine.Pin.OUT)
        self.led.value(1)

    
    def start(self,ip,port,timeout=30):
        self.timeout = timeout
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
                if not self.waitForPress():
                    self.hideFlag()
                    continue
                self.hideFlag()
                s.send(bytes("p","utf8"))
        except KeyboardInterrupt:
            print("Terminating")

    def waitForPress(self):
        val = self.btn.value()
        begin = time.time()
        while val == self.btn.value():
            if begin + self.timeout < time.time():
                return False
            pass
        
        return True
    
    def showFlag(self):
        print("Showing flag")
        self.servo.duty(105)
        self.led.value(0)

    def hideFlag(self):
        print("Hiding flag")
        self.servo.duty(60)
        self.led.value(1)
        



    

