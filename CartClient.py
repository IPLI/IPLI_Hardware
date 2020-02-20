#!/usr/bin/env python
import RPi.GPIO as GPIO
import time
import socket
import threading
import os
import sys


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
trig=[2,5,7]
echo=[3,6,8]
result=[500,500,500]
DT=17
SCK=27
sample=0
pre_gram=0
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect(('172.20.10.8', 8080))
def get_weight():
    i=0
    Count=0
    GPIO.setup(DT,GPIO.OUT)
    GPIO.output(DT,1)
    GPIO.output(SCK,0)
    GPIO.setup(DT,GPIO.IN)
    while GPIO.input(DT)==1:
        i=0
    for i in range(24):
        GPIO.output(SCK,1)
        Count=Count<<1
        GPIO.output(SCK,0)
        if GPIO.input(DT)==0:
            Count=Count+1
    GPIO.output(SCK,1)
    Count=Count^0x800000
    GPIO.output(SCK,0)
    
    return Count

def send_weight():
    global pre_gram    
    w=0
    result_gram=0
    count=[]
    plus=[]
    minus=[]
    equal=[]
    for each in range(3):
        count.append(get_weight())
        time.sleep(0.5)
    
    cntArr={"+":0, "-":0, "=":0}
    
    for i in range(len(count)):
        w=((sample-count[i])/106)
    
#        print('round gram',round(w))
        gram=max(0,round(w))
#        print('gram[',i+1,']',gram,'g')
        count[i] = gram
        result_gram=gram-pre_gram
#        print('gram[',i+1,']',result_gram,'error g')
        if result_gram>80:
            cntArr['+'] += 1
            plus.append(count[i])
        elif result_gram<-80:
            cntArr['-'] += 1
            minus.append(count[i])
        else:
            cntArr['='] += 1
            equal.append(count[i])
    
    Max = cntArr["+"]
    MaxK = "+"
    for (eachK,eachV) in cntArr.items():
        if eachV > Max:
            Max = eachV
            MaxK = eachK
            

    if MaxK=="+": #plus min
        pre_gram = min(plus)
    elif MaxK =="-":# minus max
        pre_gram = max(minus)
    else:#equal min
        pre_gram = min(equal)
    print(MaxK)
    return MaxK
def setup():
    GPIO.setup(SCK,GPIO.OUT)
    for i in range(0,3):
        GPIO.setup(trig[i],GPIO.OUT)
        GPIO.setup(echo[i],GPIO.IN)
        GPIO.output(trig[i],GPIO.LOW)
        
        
def get_ip_address():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect(('8.8.8.8',80))
    get_ip=sock.getsockname()[0]
    
    return get_ip

def runStream():
    print("runStream called")
    os.system('sh mjpg.sh')
def killStream():
    time.sleep(7)
    os.system('killall -9 mjpg_streamer')
    os.system('killall -9 sh')
    s.send(send_weight().encode())

def send_server():
    print('send_start')
    tmpStr = 'darknet.exe detector demo data/obj.data data/yolo-obj.cfg yolo-obj_last.weights http://'+my_ip+':8091/?action=stream'
    s.send(tmpStr.encode())
    print('send_end')    
    
def dis(num):
       
    GPIO.output(trig[num],False)
    time.sleep(0.01)
    
    GPIO.output(trig[num],True)
    time.sleep(0.00001)
    
    GPIO.output(trig[num],False)
    
    while GPIO.input(echo[num])==0:
        pulse_start=time.time()
        
        
    while GPIO.input(echo[num])==1:
        pulse_end=time.time()

    pulse_duration=pulse_end-pulse_start
    distance=pulse_duration*17000
    distance=round(distance,2)
    
    return distance


try:
    #time.sleep(5)
    my_ip=get_ip_address()
    print(my_ip)

    setup()
    sample=get_weight()
    while True:
        for i in range(0,3):
            result[i]=dis(i)
                        
            if result[i]<50 and result[i] >=3:
                print("distance",i+1 ,": ",result[i],"cm")
                t = threading.Thread(target=runStream)
                t2 = threading.Thread(target=send_server)
                t.start()
                t2.start()
                killStream()
                #print("load:",send_weight())
            
            
except :
        GPIO.cleanup()
        


