Klient:
Do ESP8266 se nakopírují soubory main.py a client.py (např. pomocí skriptu upload_to_esp.sh přes webrepl)
V main.py se případně upraví IP a port serveru (cli.start(IP,port)), kam se klienti připojují.
Až bude server připraven na připojení klientů (viz níže), restartujeme ESP8266 (stačí i soft reset přes Ctrl+D)
Pokud je klient serverem vybrán, vykoná metodu showFlag(). Následně zavolá waitForPress(), která vrátí True po zmáčknutí tlačítka. Následně klient vykoná metodu hideFlag() a oznámí serveru zmáčkknutí.

Server:
server.py spustíme na počítači(měl by být plně kompatibilní s micropythonem), který se bude chovat jako server. Je potřeba ve zdrojovém kódu upravit IP. (startServer(ip,port))
Server se pouští příkazem python server.py <pocet_klientu> <pocet_kol>, např. příkazem python server.py 2 20 by se pustil server pro 2 ESP na 20 kol.
Pokud chceme server pustit bez led_displaye, kde běží časomíra, je třeba nastavit proměnou server.STOPWATCH_ENABLED na False.
Po spuštění serveru příkazem connectClients(počet) připravíme server na připojení klientů (nyní restartujeme ESP8266 s nahraným clientem). Připojení klienti se postupně vypíšou. 
Pokud nedojde k připojení zadaného počtu klientů, lze pomocí Ctrl+C připojování přerušit. Pokud byli připojeni alespoň dva, stačí to na hru.
Příkazem playGame(difficulty, timeout=60) spustíme hru. Parametr difficulty udává, kolik kol (přeběhnutí k jinému stanovišti) bude třeba k dokončení hry.
Parametr timout udává čas v sekundách, který má hráč pro přeběhnutí k dalšímu tlačítku a zmáčknutí. Výchozí hodnota je 60s. 

Timeout:
Pro případ, kdy dojde k přerušení hry (ať už neaktivitou hráče či restartu serveru) má funkce playGame() na serveru a start() na clientu parametr timeout.
Bere čas v sekundách. Pokud po zvednutí vlajky u klienta nedojde v definované době ke zmáčknutí tlačítka, nebo server nedostane odpověď od klienta, hra se přeruší.