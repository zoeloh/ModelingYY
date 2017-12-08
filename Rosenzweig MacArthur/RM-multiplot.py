# This script models the population dynamics of a herbivore (H) and a predator (P) after the Rosenzweig-MacArthur consumer-resource model.
# The main purpose of this script is to generate a plot with multiple simulations for variations of a single parameter
import pandas
import scipy
import scipy.integrate as spint
from plotnine import *
import numpy

#Indicate here which parameter you wish to vary (a, b, d, e, s, w). The idea is that you dont have to change any values further down.
#Just run the script after you chose the parameter
parameterToBeVaried = 'a'

#The following function is necessary for the integration of the population model. Given input of the state variables and parameters, the function returns the 
#instantaneous change in population size for H and P. 
def RMSim(y,t,a,b,d,e,s,w):
    H=y[0]
    P=y[1]
    dHdt = b*H*(1 - a*H) - w*P*H/(d + H) #This line descripes how the Herbivore population changes in the Rosenzweig-MacArthur model
    dPdt = e*w*H*P/(d + H) - s*P #This line describes how the Predator population changes in the Rosenzweig-MacArthur model
    return [dHdt,dPdt]
    
#Here you can change the initial number of herbivores and predators present at the start of the simulation
H0 = 500 #H0 is the initial number of herbivores (500)
P0 = 120 #P0 is the inital number of predators (120)
initialConditions = [H0,P0]

#The following variables are parameters in the Rosenzweig-MacArthur model that affect the population dynamics. Change parameters here to see how they affect the dynmaics
a = 0.001 #(0.001)
b = 0.8 #(0.8)
d = 400 #(400)
e = 0.07 #(0.07)
s = 0.2 #(0.2)
w = 5 #(5)
parameters = (a, b, d, e, s, w)

#The variable times contains a list of times at which the state variables are evaluated. The spacing between the times corresponds to size of the integration steps
#the arguments to numpy.arrange are startTime, endTime, timeStep
times = numpy.arange(0, 50, 0.1)

#Here we create a list of the chosen parameter varied between a factor of four increased and decreased
#And we create the titel for the eventual plot
Title = "Rosenzweig-MacArthur\n"
varyingParameter = []
if parameterToBeVaried == 'a':
    varyingParameter = [0.25*a, 0.5*a, a, 2*a, 4*a]
    Title = Title + "Varying 'a' over "
if parameterToBeVaried == 'b':
    varyingParameter = [0.25*b, 0.5*b, b, 2*b, 4*b]
    Title = Title + "Varying 'b' over "
if parameterToBeVaried == 'd':
    varyingParameter = [0.25*d, 0.5*d, b, 2*d, 4*d]
    Title = Title + "Varying 'd' over "
if parameterToBeVaried == 'e':
    varyingParameter = [0.25*e, 0.5*e, e, 2*e, 4*e]
    Title = Title + "Varying 'e' over "
if parameterToBeVaried == 's':
    varyingParameter = [0.25*s, 0.5*s, s, 2*s, 4*s]
    Title = Title + "Varying 's' over "
if parameterToBeVaried == 'w':
    varyingParameter = [0.25*w, 0.5*w, w, 2*w, 4*w]
    Title = Title + "Varying 'w' over "

for i in range(len(varyingParameter)):
    Title = Title + str(varyingParameter[i]) + ', '

#This loop run the simulation for each value of the parameter
i = 0
for x in varyingParameter:
    i = i + 1
    parameters = ()
    if parameterToBeVaried == 'a':
        parameters = (x, b, d, e, s, w)
    if parameterToBeVaried == 'b':
        parameters = (a, x, d, e, s, w)
    if parameterToBeVaried == 'd':
        parameters = (a, b, x, e, s, w)
    if parameterToBeVaried == 'e':
        parameters = (a, b, d, x, s, w)
    if parameterToBeVaried == 's':
        parameters = (a, b, d, e, x, w)
    if parameterToBeVaried == 'w':
        parameters = (a, b, d, e, s, x)
    
    modelSim=spint.odeint(func=RMSim,y0=initialConditions,t=times,args=parameters)
    modelOutput['H' + str(i)] = modelSim[:,0]
    modelOutput['P' + str(i)] = modelSim[:,1]

#The model data is the plotted
g1=ggplot(modelOutput,aes(x="time",y="H1",color=str(varyingParameter[0])))+geom_line()+geom_line(aes(y="P1",color=str(varyingParameter[0])))+geom_line(aes(y="H2", color=str(varyingParameter[1])))+geom_line(aes(y="P2",color=str(varyingParameter[1])))+geom_line(aes(y="H3", color=str(varyingParameter[2])))+geom_line(aes(y="P3",color=str(varyingParameter[2])))+geom_line(aes(y="H4", color=str(varyingParameter[3])))+geom_line(aes(y="P4",color=str(varyingParameter[3])))+geom_line(aes(y="H5", color=str(varyingParameter[4])))+geom_line(aes(y="P5",color=str(varyingParameter[4])))+labs(x="Time",y="Population")


#And finally the plot is displayed
g1+theme_classic()+ggtitle(Title) 

