#from cProfile import label
from tkinter import * # Package pour les fenetres
#from gpiozero import thermometre, pouls

"""
temp = thermometre(23)
freq = pouls()
def run_temp():
    temp.on()
def stop_temp():
    temp.off()
def run_freq():
    freq.on()
def stop_freq():
    freq.off()
"""

# Configuration de la fenetre
app=Tk()
app.title("Station de Santé Connecté")
app.geometry("{0}x{1}+0+0".format(app.winfo_screenwidth(), app.winfo_screenheight())) # Mettre en plein ecran
#root.overrideredirect(True) # Full plein ecran sans la barre du haut
app.resizable(width=FALSE, height=FALSE) # Emepeche la fenetre d'etre redimensionné
app.config(background='#AC9CDE') # Couleur du fond

# Ajouter le titre de l'application
label_title = Label(app, text="Station de Santé Connecté", font=("Courrier",40), bg='#AC9CDE', fg='white')
label_title.pack()

# Création des différents blocs
# TEMPERATURE
temperature = Frame(app, bg='#AC9CDE', bd=1, relief=SUNKEN) #enelever bd et relief c'est juste pour voir
temperature.pack()

label_subtitle = Label(temperature, text="Température", font=("Courrier",40), bg='#AC9CDE', fg='white')
label_subtitle.pack(padx=5,pady=5, side=TOP, fill = Y)

bouton_t = Button(temperature, text="Prendre sa température", font=("Courrier", 14), bg='white', fg='#AC9CDE') # Rajouter : command=run_temp
bouton_t.pack(padx=5,pady=5, expand=TRUE, side=RIGHT, fill = BOTH)

# FREQUENCE CARDIAQUE
frequence = Frame(app, bg='#AC9CDE',  bd=1, relief=SUNKEN)
frequence.pack()

label_subtitle = Label(frequence, text="Fréquence cardiaque", font=("Courrier",40), bg='#AC9CDE', fg='white') # Rajouter : command=run_freq
label_subtitle.pack(padx=5,pady=5)

bouton_f = Button(frequence, text="Prendre son pouls", font=("Courrier", 14), bg='white', fg='#AC9CDE')
bouton_f.pack(padx=5,pady=5)


# Afficher les blocs
temperature.pack(expand=YES)
frequence.pack(expand=YES)

# Affichge de la fenetre
app.mainloop() 