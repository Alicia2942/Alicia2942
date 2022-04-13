import numpy as np
from scipy import stats

#linregress() renvoie plusieurs variables de retour
slope,intercept, r_value, p_value, std_err = stats.linregress(Xl,Yl)

x_entrer = np.array(([38, 60], [36, 60], [37.9,60], [36.1,60], [37.2,60], [36.9,60], [36.4,100], [37.2,100], [36.4,50], [37.2,50], [32,60], [37.8,60]),dtype=float)
y = np.array(([1],[1], [0], [0], [0], [0], [1], [1], [1], [1], [1]),dtype = float) #donnée de sortie : 1 = malade, 0 = sain 

x_entrer = x_entrer/np.amax(x_entrer, axis = 0)

X = np.split(x_entrer, [11])[0]
xPrediction = np.split(x_entrer, [11])[1]

class Neural_Network(object):
    def __init__(self):
        self.inputSize = 2
        self.outputSize = 1
        self.hiddenSize = 3

        self.W1 = np.random.randn(self.inputSize, self.hiddenSize) #générer poids dans une matrice entre synapse d'entree et celles cachée; matrice 2x3
        self.W2 = np.random.randn(self.hiddenSize, self.outputSize) #Matrice 3x1

    def forward(self,X):

        self.z = np.dot(X, self.W1)
        self.z2 = self.sigmoid(self.z)
        self.z3 = np.dot(self.z2,self.W2)
        o = self.sigmoid(self.z3)
        return o 

    def sigmoid(self,s):
        return 1/(1+np.exp(-s))

    def sigmoidPrime(self,s):
        return s * (1-s)

    def backward(self,X,y,o):

        self.o_error = y - o
        self.o_delta = self.o_error * self.sigmoidPrime(o)

        self.z2_error = self.o_delta.dot(self.W2.T)
        self.z2_delta = self.z2_error * self.sigmoidPrime(self.z2)

        self.W1 += X.T.dot(self.z2_delta)
        self.W2 += self.z2.T.dot(self.o_delta)

    def train(self,X,y):
        o = self.forward(X)
        self.backward(X,y,o)

    def predict(self):
        print("Donnée prédites après entrainement: ")
        print("Entrée : \n" + str(xPrediction))
        print("Sortie : \n" + str(self.forward(xPrediction)))

        if(self.forward(xPrediction) < 0.5):
            print("Le patient est en bonne santé \n")
        else 
            print("Le patient est malade \n")

class Regr_Lin(object):
    def predictlin(x_entrer):
        return slope * x_entrer + intercept
        

fitLine = predict(Xl)
plt.plot(Xl, fitLine, c='r')

NN = Neural_Network()

for i in range(3000):
    print("# " + str(i) + "\n")
    print("Valeurs d'entrees: \n" + str(X))
    print("Sortie actuelle: \n" + str(y))
    print("sortie prédite: \n" + str(np.matrix.round(NN.forward(X),2)))
    print("\n")
    NN.train(X,y)

NN.predict()
