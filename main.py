from client import Client
import webrepl, time, network
while network.WLAN(0).isconnected() == False:
    pass
webrepl.start()
time.sleep(5)
cli = Client()
cli.start("192.168.0.104",12345)
