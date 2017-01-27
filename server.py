import socket, random, time, sys, traceback, pickle
from pygame_stopwatch import StopWatch


IP = "172.16.34.150"
PORT = 12345
HIGHSCORE_FILENAME = "highscore.dat"

class Server():
    server_socket = socket.socket()
    clients = []

    STOPWATCH_ENABLED = True

    def __init__(self):
        self.running = False

        if self.STOPWATCH_ENABLED:
            self.stopwatch = StopWatch()


        #self.highscore = pickle.load()

    def startServer(self, ip, port):
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((ip, port))

    def connectClients(self, count):
        self.server_socket.listen(5)
        self.server_socket.setblocking(0)
        print("Waiting for " + str(count) + " clients to connect")
        self.clients = []
        try:
            while len(self.clients) < count:
                try:
                    client_socket, addr = self.server_socket.accept()
                    client_socket.setblocking(0)
                    self.clients.append((client_socket, addr))
                    print("Connected client #%s at address %s" % (len(self.clients), addr))
                except IOError:
                    pass

        except KeyboardInterrupt:
            self.server_socket.setblocking(1)
            print("Canceled, currently connected %s clients" % (len(self.clients)))
        self.server_socket.listen(0)


    def hide_all_flags(self):
        for socket, addr in self.clients:
            socket.send(b"d")


    def show_all_flags(self):
        for socket, addr in self.clients:
            socket.send(b"u")


    def show_one_flag(self, client_index):
        if client_index >= len(self.clients):
            print("Wrong client index...")

        for index, c  in enumerate(self.clients):
            socket = c[0]
            if index == client_index:
                socket.send(b"u")
            else:
                socket.send(b"d")

    def get_random_client_index(self, last_client_index):
        while True:
            r = random.randint(0, len(self.clients) - 1)
            if r != last_client_index:
                return r


    def winning_sequence(self):
        for i in range(5):
            self.show_all_flags()
            time.sleep(0.3)
            self.hide_all_flags()
            time.sleep(0.3)


    def flush_all_data(self):
        for client_socket, ip in self.clients:
            try:
                client_socket.recv(10)
            except IOError:
                pass





    def playGame(self, number_of_rounds):
        number_of_rounds += 1  # First button push is for starting the game
        rounds_left = number_of_rounds

        if (len(self.clients) < 2):
            print("At least 2 clients required to play!")
            return

        client_index = random.randint(0, len(self.clients) - 1)
        self.show_one_flag(client_index)

        while True:
            pushed_button = self.get_client_button_push()
            print("pushed button " + str(pushed_button))

            if pushed_button == client_index:
                if rounds_left == number_of_rounds:     # First button push, starts stopwatch
                    self.hide_all_flags()
                    if self.STOPWATCH_ENABLED:
                        self.stopwatch.startStopWatch()

                    startedTime = time.time()
                    rounds_left -= 1

                else:
                    rounds_left -= 1
                    print("Rounds left %s, client #%s" % (rounds_left, client_index + 1))



                if rounds_left == 0:
                    # Game finished, ending
                    break

                # Get new client index
                client_index = self.get_random_client_index(client_index)
                self.show_one_flag(client_index)



        if self.STOPWATCH_ENABLED:
            self.stopwatch.stopStopWatch()
        finishTime = time.time() - startedTime
        print("Finished in %s seconds" % (finishTime))

        self.winning_sequence()

        self.flush_all_data()



    def get_client_button_push(self):
        while True:
            for client_index, c  in enumerate(self.clients):
                client_socket = c[0]
                try:
                    # If this doesn't raise exception, byte was received from client by server
                    client_socket.recv(1)
                    print("button push " + str(client_index))
                    return client_index

                except IOError:
                    pass



def parse_cmd_arguments(args):
    if len(sys.argv) >= 2:
        number_of_clients = int(sys.argv[1])  # First commandline parameter is number of clients
    else:
        number_of_clients = 3

    if len(sys.argv) >= 3:
        number_of_rounds = int(sys.argv[2])  # Second commandline parameter is number of rounds
    else:
        number_of_rounds = 20

    return number_of_clients, number_of_rounds





srv = Server()
srv.startServer(IP, PORT)

number_of_clients, number_of_rounds = parse_cmd_arguments(sys.argv)

srv.connectClients(number_of_clients)

running = True
while running:

    try:

        srv.playGame(number_of_rounds)

    except KeyboardInterrupt:
        traceback.print_exc()

        srv.server_socket.close()
        running = False

        print("closing connections")

        if srv.STOPWATCH_ENABLED:
            srv.stopwatch.stopStopWatch()



    except Exception as e:
        traceback.print_exc()

        srv.server_socket.close()
        running = False

        print("closing connections")

        if srv.STOPWATCH_ENABLED:
            srv.stopwatch.stopStopWatch()
