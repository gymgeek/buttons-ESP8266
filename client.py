import socket, machine, time

<<<<<<< HEAD
=======
# Bytes meanings
flag_up_lights_on = b"u"    # u - Flag up and lights on
flag_down_lights_off = b"d"   # d - Flag down and lights off
flag_up = b"f"              # f - Flag up
flag_down = b"c"            # c - Flag down
lights_on = b"l"            # l - lights on
lights_off = b"m"           # m - lights off



>>>>>>> 0435b292dbc1e6f7248aef92569fe13641fd4262

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
<<<<<<< HEAD
                    recieve = str(self.server_socket.recv(1), "utf8")
=======
                    recieve = self.server_socket.recv(1)
>>>>>>> 0435b292dbc1e6f7248aef92569fe13641fd4262

                except:
                    # Nothing was received
                    pass

<<<<<<< HEAD
                if recieve == "u":
                    self.showFlag()


                elif recieve == "d":
                    self.hideFlag()

=======
                if recieve:
                    print(recieve)

                if recieve == flag_up_lights_on:
                    self.showFlag()
                    self.switch_lights_on()

                elif recieve == flag_down_lights_off:
                    self.hideFlag()
                    self.switch_lights_off()

                elif recieve == flag_up:
                    self.showFlag()

                elif recieve == flag_down:
                    self.hideFlag()

                elif recieve == lights_on:
                    self.switch_lights_on()

                elif recieve == lights_off:
                    self.switch_lights_off()

>>>>>>> 0435b292dbc1e6f7248aef92569fe13641fd4262

                # If button state has changed, sent info to server
                new_button_value = self.button_pin.value()
                if last_button_value != new_button_value:
                    last_button_value = new_button_value
                    self.server_socket.send(b"p")
                    print("Button pressed")




        except KeyboardInterrupt:
            print("Terminating")


    def showFlag(self):
<<<<<<< HEAD
        print("Showing flag")
        self.servo_pin.duty(105)
        self.led_pin.value(0)

    def hideFlag(self):
        print("Hiding flag")
        self.servo_pin.duty(60)
        self.led_pin.value(1)


=======
        self.servo_pin.duty(105)

    def switch_lights_on(self):
        self.led_pin.value(0)

    def hideFlag(self):
        self.servo_pin.duty(60)

    def switch_lights_off(self):
        self.led_pin.value(1)



>>>>>>> 0435b292dbc1e6f7248aef92569fe13641fd4262




