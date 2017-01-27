import socket, machine, time


class Client():
    server_socket = socket.socket()

    def __init__(self):
        # Servo setup
        self.servo_pin = machine.PWM(machine.Pin(12))
        self.servo_pin.freq(50)
        self.servo_pin.duty(60)

        # Button setup
        self.button_pin = machine.Pin(4, machine.Pin.IN, machine.Pin.PULL_UP)

        # Led pin setup
        self.led_pin = machine.Pin(2, machine.Pin.OUT)
        self.led_pin.value(1)

    def start(self, ip, port):

        if not self.connect(ip, port):
            print("Unable to connect...")
            print("Exiting game!")
            return

        print("Connected")
        self.gameLoop()

    def connect(self, ip, port):
        # Returns true, if connected properly

        try:
            self.server_socket.connect((ip, port))
        except:
            return False
        return True


    def gameLoop(self):
        print("Starting game")
        self.server_socket.setblocking(0)

        last_button_value = self.button_pin.value()
        try:
            while True:
                recieve = None
                # Recieve instructions from server
                try:
                    recieve = str(self.server_socket.recv(1), "utf8")

                except:
                    # Nothing was received
                    pass

                if recieve == "u":
                    self.showFlag()


                elif recieve == "d":
                    self.hideFlag()


                # If button state has changed, sent info to server
                new_button_value = self.button_pin.value()
                if last_button_value != new_button_value:
                    last_button_value = new_button_value
                    self.server_socket.send(b"p")
                    print("Button pressed")




        except KeyboardInterrupt:
            print("Terminating")


    def showFlag(self):
        print("Showing flag")
        self.servo_pin.duty(105)
        self.led_pin.value(0)

    def hideFlag(self):
        print("Hiding flag")
        self.servo_pin.duty(60)
        self.led_pin.value(1)






