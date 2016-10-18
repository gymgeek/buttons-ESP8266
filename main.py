from client import Client
import webrepl, time, network
while network.WLAN(0).isconnected() == False:
    pass
webrepl.start()

cli = Client()
cli.start("192.168.0.110",12345)
