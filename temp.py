import time
import datetime as dt
from datetime import date
from time import strftime #afin de pouvoir changer l'ordre et l'afficher comme on veut
import board
import adafruit_dht
import psutil
from matplotlib import pyplot as plt # Pour afficher un graph
import matplotlib.animation as animation

for proc in psutil.process_iter():
    if proc.name() == 'libgpiod_pulsein' or proc.name() == 'libgpiod_pulsei':
        proc.kill()
sensor = adafruit_dht.DHT22(board.D23)

fig = plt.figure()
ax = fig.add_subplot(1,1,1)
nbligne = 0
x = []
y = []

def animate(i, x, y):
    
    try:
    
        temp = sensor.temperature
        humidity = sensor.humidity
        today = date.today().strftime('%d/%m/%Y')
        now = dt.datetime.now().strftime('%H:%M:%S')
        # Information au client
        #on limite a 20
        x = x[-20:]
        y = y[-20:]

        #Graph 
        ax.clear()
        ax.plot(x,y)
        
        # Ecriture dans un fichier txt
        heure = open("heure.txt","a")
        tempe = open("temp.txt","a")
        heure.write("{}\n" .format(now))
        tempe.write("{}\n" .format(temp))
        heure.close()
        tempe.close()

        # Date et heure
        print("Le {} à {}" .format(today, now))
        
        # Temperature et humidité
        print("Temperature: {}*C   Humidity: {}% ".format(temp, humidity))
        
        # Mettre sous forme de graph
        heure = open("heure.txt","r")
        tempe = open("temp.txt","r")
        lineh = heure.readline()
        linet = tempe.readline()
        while lineh :
            x.append(lineh)
            print(lineh)
            lineh = heure.readline()
        while linet :
            y.append(linet)
            print(linet)
            linet = tempe.readline()
        
#         plt.plot(x,y)
#         plt.show()
        # Penser a fermer les fichier
        heure.close()
        tempe.close()    
        
    except RuntimeError as error:
        print(error.args[0])
        time.sleep(2.0)
    except Exception as error:
        sensor.exit()
        raise error
        time.sleep(2.0)
    
    
# 	temp_c = round(sensor.read_temp(),2) #permet de lire la température 
# 	#humidity = sensor.humidity (penser a rajouter après)
# 	
# 	#ajout des x et y
# 	xs.append(dt.datetime.now().strftime('%H:%M:%S.%f'))
# 	ys.append(temp_c)

# 	
# 	#Format plot
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)
    plt.title('Température en fonction du temps')
    plt.ylabel('Température en degré celcius')


	
#on plot pour appeler periodiquement la fonction animate
ani = animation.FuncAnimation(fig, animate, fargs=(x,y), interval=1000)
plt.show()

