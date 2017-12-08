#The main purpose of this file is to generate a series of plots varying a single parameter.

import pandas
import scipy
import scipy.integrate as spint
from plotnine import *
import numpy

#Indicate here which parameter you wish to vary (a, b, e, s). The idea is that you dont have to change any values further down.
#Just run the script after you chose the parameter
parameterToBeVaried = 's'

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

#The following variables are parameters in the Lotka-Volterra model that affect the population dynamics. Change base parameters here to see how they affect the dynmaics
a = 0.02 #(0.02)
b = 0.5 #(0.5)
e = 0.1 #(0.1)
s = 0.2 #(0.2)


#The variable times contains a list of times at which the state variables are evaluated. The spacing between the times corresponds to size of the integration steps
#the arguments to numpy.arrange are startTime, endTime, timeStep
times = numpy.arange(0, 50, 0.1)

#DataFrame to hold the simulation data
modelOutput = pandas.DataFrame({"time":times})

#Here we create a list of the chosen parameter varied between a factor of four increased and decreased
#And we create the titel for the eventual plot
Title = "Lotka-Volterra\n"
varyingParameter = []
if parameterToBeVaried == 'a':
    varyingParameter = [0.25*a, 0.5*a, a, 2*a, 4*a]
    Title = Title + "Varying 'a' over "
if parameterToBeVaried == 'b':
    varyingParameter = [0.25*b, 0.5*b, b, 2*b, 4*b]
    Title = Title + "Varying 'b' over "
if parameterToBeVaried == 'e':
    varyingParameter = [0.25*e, 0.5*e, e, 2*e, 4*e]
    Title = Title + "Varying 'e' over "
if parameterToBeVaried == 's':
    varyingParameter = [0.25*s, 0.5*s, s, 2*s, 4*s]
    Title = Title + "Varying 's' over "

for i in range(len(varyingParameter)):
    Title = Title + str(varyingParameter[i]) + ', '

#This loop run the simulation for each value of the parameter
i = 0
for x in varyingParameter:
    i = i + 1
    parameters = ()
    if parameterToBeVaried == 'a':
        parameters = (x, b, e, s)
    if parameterToBeVaried == 'b':
        parameters = (a, x, e, s)
    if parameterToBeVaried == 'e':
        parameters = (a, b, x, s)
    if parameterToBeVaried == 's':
        parameters = (a, b, e, x)
    
    modelSim=spint.odeint(func=LVSim,y0=initialConditions,t=times,args=parameters)
    modelOutput['H' + str(i)] = modelSim[:,0]
    modelOutput['P' + str(i)] = modelSim[:,1]

#The model data is the plotted
g1=ggplot(modelOutput,aes(x="time",y="H1",color="1"))+geom_line()+geom_line(aes(y="P1",color="1"))+geom_line(aes(y="H2", color="2"))+geom_line(aes(y="P2",color="2"))+geom_line(aes(y="H3", color="3"))+geom_line(aes(y="P3",color="3"))+geom_line(aes(y="H4", color="4"))+geom_line(aes(y="P4",color="4"))+geom_line(aes(y="H5", color="5"))+geom_line(aes(y="P5",color="5"))+labs(x="Time",y="Population")


#And finally the plot is displayed
g1+theme_classic()+ggtitle(Title) 
