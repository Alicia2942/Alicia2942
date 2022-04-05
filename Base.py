import time
import datetime
from datetime import date
from time import strftime #afin de pouvoir changer l'ordre et l'afficher comme on veut
import board
import adafruit_dht
import psutil

# We first check if a libgpiod process is running. If yes, we kill it!
for proc in psutil.process_iter():
    if proc.name() == 'libgpiod_pulsein' or proc.name() == 'libgpiod_pulsei':
        proc.kill()
sensor = adafruit_dht.DHT22(board.D23)

while True:
    # ce que l'on va afficher si ca fonctionne
    try:
        temp = sensor.temperature
        humidity = sensor.humidity
        today = date.today().strftime('%d/%m/%Y')
        now = datetime.datetime.now().time().strftime('%H:%M')
        # Information au client
        # Date et heure
        print("Le {} à {}" .format(today, now))
        # Temperature et humidité
        print("Temperature: {}*C   Humidity: {}% ".format(temp, humidity))
        
    except RuntimeError as error:
        print(error.args[0])
        time.sleep(2.0)
        continue
    except Exception as error:
        sensor.exit()
        raise error
    time.sleep(2.0)

