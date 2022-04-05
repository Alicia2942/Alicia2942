#from cProfile import label
from tkinter import * # Package pour les fenetres
import board # Board des gpio
import adafruit_dht # Capteur de temperature
from pulsesensor import Pulsesensor # Lancement de l'autre programme execution capteur pouls
#from gpiozero import sensor, pulsesensor

# Package date et heure
import time
import datetime as dt
from datetime import date
from time import strftime #afin de pouvoir changer l'ordre et l'afficher comme on veut
import psutil # Recupère info sur carte

# Package des graphes
import matplotlib.pyplot as plt # Pour afficher un graph
import matplotlib.animation as animation
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
# Importer script python du graph temperature

# Initialisation variable
# TEMPERATURE
fig1 = plt.figure(1, figsize=(4,3))
fig1.patch.set_facecolor('#D9BE94')
ax1 = fig1.add_subplot()
xs1 = []
ys1 = []


# Verification du branchement
for proc in psutil.process_iter():
    if proc.name() == 'libgpiod_pulsein' or proc.name() == 'libgpiod_pulsei':
        proc.kill()

sensor = adafruit_dht.DHT22(board.D23)


# POULS
p = Pulsesensor()
p.startAsyncBPM()

fig = plt.figure(2, figsize=(4,3))
fig.patch.set_facecolor('#D9BE94')


ax = fig.add_subplot()
xs = []
ys = []


# Fonctions lancement capteurs
# TEMPERATURE
def run_temp(j, xs1, ys1):
    
    # Execution du capteur 
    # ce que l'on va afficher si ca fonctionne
    try:
        now = dt.datetime.now().strftime('%H:%M')
        temp = sensor.temperature
        humidity = sensor.humidity
               
        # Temperature et humidité
        print("Temperature: {}*C   Humidity: {}% ".format(temp, humidity))
        label_date['text'] = "{}  {}".format(today, now)
        
        if temp > 36 and temp < 38 :
            labelt['text'] = "{}°C".format(temp)
            labelt.config(fg='green')
        else:
            labelt['text'] = "{}°C".format(temp)
            labelt.config(fg='red')

        
        xs1.append(dt.datetime.now().strftime('%H:%M:%S'))
        ys1.append(temp)
        
        xs1 = xs1[-20:]
        ys1 = ys1[-20:]
            
        ax1.clear()
        ax1.plot(xs1,ys1)
        ytmi = [36 for i in xs1]
        ytma = [38 for i in xs1]
        ax1.plot(xs1,ytmi, color='r')
        ax1.plot(xs1,ytma, color='r')
        ax1.patch.set_color('#D9BE94')
        ax1.set_xticklabels([])
       
        #ax1.plot(xs1, ytmi)
        #ax1.plot(xs1, ytma)
        #plt.axhline(y=36, color='red')
        #plt.axhline(y=38, color='red')

        # Ecriture dans un fichier txt
        heure = open("heure.txt","a")
        tempe = open("temp.txt","a")
        heure.write("{}\n" .format(now))
        tempe.write("{}\n" .format(temp))
        heure.close()
        tempe.close()
        
        plt.xticks(rotation=45, ha='right')
        plt.subplots_adjust(bottom=0.30)
        #plt.title('Température en fonction du temps')
        #plt.ylabel('Température en degré celcius')
        
        
    except RuntimeError as error:
        print(error.args[0])
        time.sleep(0.05)
    except Exception as error:
        sensor.exit()
        raise error
    time.sleep(0.05)

def animatet():
    ani1 = animation.FuncAnimation(fig1, run_temp, fargs=(xs1,ys1), interval=1000)
    canvas1.draw()
    canvas1.get_tk_widget().pack()


# POULS
def run_pouls(i, xs, ys):
    # Execution du capteur 
    # ce que l'on va afficher si ca fonctionne
    try:
    
        bpm = p.BPM
        bpm = int(bpm)
        if bpm > 0:
            print("BPM: %d" % bpm)
#         else:
#             print("No Heartbeat found")


            if bpm > 50 and bpm < 90 :
                labelf['text'] = "{} BPM".format(bpm)
                labelf.config(fg='green')
            else:
                labelf['text'] = "{} BPM".format(bpm)
                labelf.config(fg='red')
            
            
            now = dt.datetime.now().strftime('%H:%M:%S:%f')
            xs.append(dt.datetime.now().strftime('%H:%M:%S:%f'))
            ys.append(p.BPM)
               
            xs = xs[-100:]
            ys = ys[-100:] 

            ax.clear()
            ax.plot(xs,ys)
            yfmi = [50 for i in xs]
            yfma = [90 for i in xs]
            ax.plot(xs,yfmi, color='r')
            ax.plot(xs,yfma, color='r')
            ax.patch.set_color('#D9BE94')
            ax.set_xticklabels([])
            
            
            # Ecriture dans un fichier txt
            heure = open("heure.txt","a")
            pouls = open("pouls.txt","a")
            heure.write("{}\n" .format(now))
            pouls.write("{}\n" .format(bpm))
            heure.close()
            pouls.close()
            
            plt.xticks(rotation=45, ha='right')
            plt.subplots_adjust(bottom=0.0030)
            #plt.title('Pouls en fonction du temps')
            #plt.ylabel('BPM')
            
        time.sleep(0.003)
        
    except:
        p.stopAsyncBPM()

def animatep():
    ani = animation.FuncAnimation(fig, run_pouls, fargs=(xs,ys), interval=1000)
    canvas.draw()
    canvas.get_tk_widget().pack()

# Configuration de la fenetre
app=Tk()
app.title("Station de Santé Connecté")
w, h = app.winfo_screenwidth(), app.winfo_screenheight()
app.geometry("%dx%d" % (w,h)) # Mettre en plein ecran
app.overrideredirect(True) # Full plein ecran sans la barre du haut
app.resizable(width=FALSE, height=FALSE) # Emepeche la fenetre d'etre redimensionné
app.config(background='#D9BE94') # Couleur du fond

# Ajouter le titre de l'application
# Date et heure
today = date.today().strftime('%d/%m/%Y')
now = dt.datetime.now().time().strftime('%H:%M')
label_title = Label(app, text="Station de Santé Connecté", font=("Courrier",20), bg='#D9BE94', fg='white')
label_date = Label(app, text="{}  {}".format(today, now), font=("Courrier",10), bg='#D9BE94', fg='white')
label_title.pack()
label_date.pack()

# Création des différents blocs
# TEMPERATURE
temperature = Frame(app, width=100, height=100, bg='#D9BE94')
temperature.pack(side=LEFT, fill=Y)

label_subtitle = Label(temperature, text="Température", font=("Courrier",20), bg='#D9BE94', fg='white')
label_subtitle.pack(padx=5,pady=5, side=TOP, fill = Y)
labelt = Label(temperature, text="-.-°C", font=("Courrier",25), bg='#D9BE94', fg='white')
labelt.pack(padx=5,pady=5, side=TOP, fill = Y)

bouton_t = Button(temperature, text="Prendre sa température", font=("Courrier", 10), command=lambda: [animatet()], bg='white', fg='#D9BE94') 
bouton_t.pack()

# FREQUENCE CARDIAQUE
frequence = Frame(app, width=100, height=100, bg='#D9BE94')
frequence.pack(side=LEFT, fill=Y)

label_subtitle = Label(frequence, text="Fréquence cardiaque", font=("Courrier",20), bg='#D9BE94', fg='white')
label_subtitle.pack(padx=5,pady=5)
labelf = Label(frequence, text="-- BPM", font=("Courrier",25), bg='#D9BE94', fg='white')
labelf.pack(padx=5,pady=5, side=TOP, fill = Y)

bouton_f = Button(frequence, text="Prendre son pouls", font=("Courrier", 10), command=lambda: [animatep()], bg='white', fg='#D9BE94')
bouton_f.pack()

# Canvas
canvas1 = FigureCanvasTkAgg(fig1, master=temperature)
canvas = FigureCanvasTkAgg(fig, master=frequence)


#canvas1.draw()

# AFFICHAGE
# Afficher les blocs
temperature.pack(expand=YES)
frequence.pack(expand=YES)
# Affichge de la fenetre
app.mainloop() 