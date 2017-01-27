from client import Client
import webrepl, time, network

IP = "172.16.34.150"
PORT = 12345


# Wait until ESP is connected to wifi
while network.WLAN(0).isconnected() == False:
    pass

print("Connected to wifi")
print("Starting webrepl")
webrepl.start()


print("Starting client")
cli = Client()
# Server ip
cli.start(IP,PORT)
