# This script models the population dynamics of a herbivore (H) and a predator (P) after the Lotka-Volterra consumer-resource model.
# Secondly, the script uses the model data to generate a plot for illusttation
import pandas
import scipy
import scipy.integrate as spint
from plotnine import *
import numpy

#The following function is necessary for the integration of the population model. Given input of the state variables and parameters, the function returns the 
#instantaneous change in population size for H and P. 
def LVSim(y,t,a,b,e,s):
    H=y[0]
    P=y[1]
    dHdt = b*H - a*P*H #This line descripes how the Herbivore population changes in the Lotka-Volterra model
    dPdt = e*a*P*H - s*P #This line describes how the Predator population changes in the Lotka-Volterra model
    return [dHdt,dPdt]
    
#Here you can change the initial number of herbivores and predators present at the start of the simulation
H0 = 25 #H0 is the initial number of herbivores (25)
P0 = 5 #P0 is the inital number of predators (5)
initialConditions = [H0,P0] #H0, P0

#The following variables are parameters in the Lotka-Volterra model that affect the population dynamics. Change parameters here to see how they affect the dynmaics
a = 0.02 #(0.02)
b = 0.5 #(0.5)
e = 0.1 #(0.1)
s = 0.2 #(0.2)
parameters = (a, b, e, s)

#The variable times contains a list of times at which the state variables are evaluated. The spacing between the times corresponds to size of the integration steps
#the arguments to numpy.arrange are startTime, endTime, timeStep
times = numpy.arange(0, 50, 0.1)

#Here we integrate the model based on initial values of H and P and the chosen parameters
modelSim=spint.odeint(func=LVSim,y0=initialConditions,t=times,args=parameters)
#The resulting model data in stored in the DataFrame modelOutput
modelOutput=pandas.DataFrame({"time":times,"H":modelSim[:,0], "P":modelSim[:,1]})

#The model data is the plotted
g1=ggplot(modelOutput,aes(x="time",y="H",color="1"))+geom_line()+geom_line(aes(y="P",color="2"))+labs(x="Time",y="Population")

#Here we create the titel for the plot
Title = "Lotka-Volterra, H0 = " + str(H0) + ", P0 = " + str(P0) + "\n"
Title = Title + "a = " + str(a) + ", b = " + str(b) + ", e = " + str(e) + ", s = " + str(s)

#And finally the plot is displayed
g1+theme_classic()+ggtitle(Title) + labs(color = "H is purple \nP is yellow")


