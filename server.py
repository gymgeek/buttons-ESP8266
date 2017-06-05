import socket, random, time, sys, traceback, argparse



class Server():
    server_socket = socket.socket()
    clients = []

    STOPWATCH_ENABLED = True

    def __init__(self):
        self.running = False

        if self.STOPWATCH_ENABLED:
            self.stopwatch = StopWatch()




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


    def restart_sequence(self):
        for i in range(2):
            self.show_all_flags()
            time.sleep(0.8)
            self.hide_all_flags()
            time.sleep(0.8)


    def flush_all_data(self):
        for client_socket, ip in self.clients:
            try:
                while True:
                    client_socket.recv(1)
            except IOError:
                pass





    def playGame(self, number_of_rounds):
        last_button_pushes = []
        restart_button_count = 10
        last_button_push_time = time.time()

        rounds_left = number_of_rounds

        if (len(self.clients) < 2):
            print("At least 2 clients required to play!")
            return

        client_index = random.randint(0, len(self.clients) - 1)
        self.show_one_flag(client_index)

        while True:
            pushed_button = self.get_client_button_push()

            if pushed_button != None and time.time() - last_button_push_time > 0.2:
                last_button_push_time = time.time()
                # Restarts the game, if one button is pushed 4 times
                last_button_pushes.append(pushed_button)
                last_button_pushes = last_button_pushes[-restart_button_count:]
                first = last_button_pushes[0]
                print ("Pushed button", pushed_button)
                print("Last button pushes", last_button_pushes)

                if len(last_button_pushes) == restart_button_count and all(map(lambda x: x == first, last_button_pushes)):      # if one button was pressed 4 times consequently
                    print("Restart")

                    if self.STOPWATCH_ENABLED:
                        self.stopwatch.stopStopWatch()

                    self.restart_sequence()
                    self.flush_all_data()


                    return





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

            elif pushed_button == None and rounds_left == number_of_rounds:
                client_socket = self.clients[client_index][0]
                client_socket.send(b"m")
                time.sleep(0.2)
                client_socket.send(b"l")





        if self.STOPWATCH_ENABLED:
            self.stopwatch.stopStopWatch()
        finishTime = time.time() - startedTime
        print("Finished in %s seconds" % (finishTime))

        self.winning_sequence()

        self.flush_all_data()



    def get_client_button_push(self):
        timeout = 1.5
        start_time = time.time()
        while True:
            for client_index, c  in enumerate(self.clients):
                client_socket = c[0]
                try:
                    # If this doesn't raise exception, byte was received from client by server
                    client_socket.recv(1)
                    return client_index

                except IOError:
                    pass

            if time.time() - start_time > timeout:
                return None



def parse_cmd_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ip', help='IP of the server', default="localhost")
    parser.add_argument('--port', help='port on which server will listen', type=int, default="8080")
    parser.add_argument('--clients', help='Number of clients', type=int, default=3)
    parser.add_argument('--rounds', help='Number of rounds for one game', type=int, default=10)





    return parser.parse_args()



cmd_args = parse_cmd_arguments()

# if help message was printed, pygame was never initialized, which is what we want
from pygame_stopwatch import StopWatch

print("IP: ", cmd_args.ip + ":" + str(cmd_args.port))
print("Number of clients:", cmd_args.clients)
print("Number of round:", cmd_args.rounds)



srv = Server()
srv.startServer(ip=cmd_args.ip, port=cmd_args.port)


srv.connectClients(cmd_args.clients)

running = True
while running:

    try:

        srv.playGame(cmd_args.rounds)

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
