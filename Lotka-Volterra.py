import pandas
import scipy
import scipy.integrate as spint
from plotnine import *
import numpy

def LVSim(y,t0,a,b,e,s):
    H=y[0]
    P=y[1]
    dHdt = b*H-a*P*H
    dPdt = e*a*P*H-s*P
    return [dHdt,dPdt]
    
initialConditions = [25,5] #H0, P0
a = 0.02
b = 0.5
e = 0.1
s = 0.2
parameters = (a, b, e, s)
times = numpy.arange(0, 100, 0.1)

modelSim=spint.odeint(func=LVSim,y0=initialConditions,t=times,args=parameters)
modelOutput=pandas.DataFrame({"time":times,"H":modelSim[:,0], "P":modelSim[:,1]})

g1=ggplot(modelOutput,aes(x="time",y="H",color="10"))+geom_line()+geom_line(aes(y="P",color="15"))+labs(x="time",y="Population")


g1+theme_classic()


