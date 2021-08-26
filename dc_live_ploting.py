#!/usr/bin/python
# -*- coding:utf-8 -*-


import time
import ads1263
import RPi.GPIO as GPIO
import numpy as np
import matplotlib.pyplot as plt
import math as m
import scipy.fftpack
import scipy
from matplotlib.animation import FuncAnimation
from itertools import count

REF=5.08
ADC = ads1263.ADS1263()
    
if (ADC.ADS1263_init() == -1):
    exit()

ADC.ADS1263_ConfigADC(0,0xF)

x_vals=[]
y_vals=[]
index=count()


def  animate(i):
    x_vals.append(next(index))
    value=ADC.ADS1263_GetChannalValue(1)*REF/0x77777777
    if value>10:
        y_vals.append(0)
    else:
        y_vals.append(value)
    plt.plot(x_vals,y_vals)



try:

    
    ani=FuncAnimation(plt.gcf(),animate,interval=1000)

    plt.tight_layout()
    plt.show()
        

except IOError as e:
    
    plt.plot(range(0,len(reg)),reg)
    plt.show()
    print(e)
   
except KeyboardInterrupt:
    e=time.time()
    ADC.ADS1263_Exit()
    


    plt.plot(x_vals,y_vals)
    plt.show()

    print("Sample amount:",len(reg))
    print("Time: ",e-s)
    print("ctrl + c:")
    print("Program end")
    
    exit()
   


