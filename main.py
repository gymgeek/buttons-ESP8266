from client import Client
import webrepl, time, network
while network.WLAN(0).isconnected() == False:
    pass
webrepl.start()

cli = Client()

# Server ip
cli.start("172.16.34.74",12345)
