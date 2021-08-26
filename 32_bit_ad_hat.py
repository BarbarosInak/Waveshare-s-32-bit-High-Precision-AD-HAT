
#!/usr/bin/python
# -*- coding:utf-8 -*-

import time
import config
import ads1263
import RPi.GPIO as GPIO
import numpy as np
import matplotlib.pyplot as plt
import math as m
import scipy.fftpack
import scipy
from matplotlib.animation import FuncAnimation
from itertools import count
from matplotlib.widgets import RadioButtons, Slider

fs=4500
MAX=6.5
REF = 5.08

ADC=ads1263.ADS1263()
ADC.ADS1263_init()
ADC.ADS1263_ConfigADC(0,0xF)
ADC.ADS1263_SetChannal(1)
#ADC.ADS1263_SetMode(0)




fig=plt.figure(figsize=(12,10))

ax1 = fig.add_subplot(2,1,1)
ax2 = fig.add_subplot(2,1,2)

start=1500
num_sample=3000


def animate(_):
    ADC.ADS1263_WaitDRDY()
    #ADC.ADS1263_SetChannal(0)
    x1=[]
    x2=[]

    s=time.time()
    for j in range(3001):
        #ADC.ADS1263_Read_ADC_Data(reg)
        x1.append(ADC.ADS1263_Read_ADC_Data())
        #print(".")
        #time.sleep(2/10000000)

    e=time.time()
    y1=range(len(x1))
    
    fs=len(x1)/(e-s)
    
    
    x1=[each*REF/0x7fffffff if each*REF/0x7fffffff<8 else each*REF/0x7fffffff-10.154 for each in x1]
    

    #x1=[each-np.average(x1) for each in x1 ]
    
    
    x2=list(scipy.fftpack.fftshift(abs(scipy.fft(x1))*8/len(x1)))
    x2[1500]=x2[1500]/8
    
    y2=np.linspace(-fs/2,fs/2,len(x2))

    
    start=int(start_slider.val)+1500
    num_sample=int(sample_slider.val)
    

    ax1.clear()
    ax2.clear()
    ax1.set_xlabel("Örnek Sayısı")
    ax1.set_ylabel("Büyüklük(V)")
    ax1.plot(y1[:num_sample],x1[:num_sample])
    ax2.set_xlabel("Frekans(Hz)")
    ax2.set_ylabel("Büyüklük(V)")

    ax2.plot(y2[start:],x2[start:])
    plt.subplots_adjust(left=0.2,bottom=0.09)

    #fig.patch.set_facecolor("xkcd:aqua blue")

rax=plt.axes([0, 0.28, 0.12, 0.44])

radio= RadioButtons(rax, ("2d5SPS","5SPS","10SPS","16d6SPS","20SPS","50SPS","60SPS","100SPS","400SPS","1200SPS","2400SPS","4800SPS","7200SPS","14400SPS","19200SPS","38400SPS"),active=15)



for circle in radio.circles:
    circle.set_radius(0.018)

axslider=plt.axes([0.2, 0.03, 0.68, 0.0075])
ax2slider=plt.axes([0.2, 0.01, 0.68, 0.0075])
start_slider=Slider(ax=axslider,label="Frekans Başlangıç Noktası",valmin=0,valmax=1500,valinit=0)
sample_slider=Slider(ax=ax2slider,label="Örnek Sayısı",valmin=0,valmax=3000,valinit=3000)


def spsfunc(label):
    ADS1263_DRATE = {
    'ADS1263_38400SPS'  : 0xF, 
    'ADS1263_19200SPS'  : 0xE,
    'ADS1263_14400SPS'  : 0xD,
    'ADS1263_7200SPS'   : 0xC,
    'ADS1263_4800SPS'   : 0xB,
    'ADS1263_2400SPS'   : 0xA,
    'ADS1263_1200SPS'   : 0x9,
    'ADS1263_400SPS'    : 0x8,
    'ADS1263_100SPS'    : 0x7,
    'ADS1263_60SPS'     : 0x6,
    'ADS1263_50SPS'     : 0x5,
    'ADS1263_20SPS'     : 0x4,
    'ADS1263_16d6SPS'   : 0x3,
    'ADS1263_10SPS'     : 0x2,
    'ADS1263_5SPS'      : 0x1,
    'ADS1263_2d5SPS'    : 0x0,
    }

    ADC.ADS1263_ConfigADC(0,ADS1263_DRATE["ADS1263_"+str(label)])
    plt.draw()

radio.on_clicked(spsfunc)

def sliderfunc(index):
    start=int(index)
    #print(start)
    plt.draw()
    
start_slider.on_changed(sliderfunc)

def samplefunc(index):
    sample=int(index)
    plt.draw()

sample_slider.on_changed(samplefunc)

    
try:

    ani=FuncAnimation(fig,animate,1000)
    
    
    plt.tight_layout()
    plt.show()
    
    print("Finished")
    
    


except IOError as e:
    print(e)

except KeyboardInterrupt:
    
    print("Finished")
    ADC.ADS1263_Exit()
    exit()
