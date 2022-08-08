# Sense Hat CPU LED Matrix monitor 
# author M. Manojlovic synchromatik@gmail.com
# TODO: Per Core Switch Monitor

from sense_hat import SenseHat
from scipy.interpolate import interp1d
import time
import psutil
import numpy as np 
from itertools import chain
sense = SenseHat()

#Set orientation as needed
#sense.set_rotation(180)

#make array from cpu load 
def constructArray(cpuLoad):
    my_array_initial = np.arange(start=1, stop=cpuLoad+1)
    if my_array_initial.size == 0:
        my_array_final = np.zeros(8)
    else:
        diff = 8 - my_array_initial.size
        my_array_final = np.append(my_array_initial, [[0]*diff])
    return my_array_final


#convert array to collors
def arrayToCollor(arr):
    colors = [chr(number + 96) for number in arr]
    colors2 = list(map(lambda x: x.replace('`', 'none'), colors))
    return colors2

#define colors here
#a=low
#h=hight
colors = {
    "a" : (60, 180, 75), #G
    "b" : (60, 180, 75), #G
    "c" : (255, 255, 0), #Y
    "d" : (255, 255, 0), #Y
    "e" : (255, 140, 0), #O
    "f" : (255, 140, 0), #O
    "g" : (255, 0, 0), #R
    "h" : (255, 0, 0), #R
    "none" : (0, 0, 0)
}
#initial array
load = []
loadfinal = []
print('Script runing, check leds')

#update array in realtime cpu load
#display to the led
while True:
    #Repeating 8 times, for 8 rows total on LED Matrix
    #updatedArray = constructArray(interp1d([0, 100], [0, 8])(psutil.cpu_percent()).round(0)).tolist() * 8
    #float list to int list
    #final = list(map(int, updatedArray))
    #to char list along conversion of corresponding load to letter for coloring purpose
    #led = arrayToCollor(final)
    percore = psutil.cpu_percent(percpu=True)
    percorelinear = interp1d([0, 100], [0, 8])(percore).round(0).tolist() 
    output = [constructArray(i) for i in percorelinear] 
    for e in output:
        a = arrayToCollor(list(map(int, e))) * 2
        load.insert(0, a)
    load = list(chain.from_iterable(load))
    for e in load:
        x = colors[e]
        loadfinal.insert(0, x)
    print(loadfinal)
    sense.set_pixels(loadfinal)
    time.sleep(1)
    load.clear()
    loadfinal.clear()
    # print(load)

    # time.sleep(5)
    # loadfinal.clear()
    

