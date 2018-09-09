# 定義
import machine
from machine import Pin
from machine import PWM
import time

# PIN Define:
D0 = 16
D1 = 5  #PWM
D2 = 4  #PWM
D3 = 0  #PWM
D4 = 2  #PWM, #Led on board
D5 = 14 #PWM
D6 = 12 #PWM
D7 = 13 #PWM
D8 = 15 #PWM

#Setup PINS
led = machine.Pin(2, machine.Pin.OUT)
for i in range(5):
    led.value(not led.value())

# for motor sheilf
motor_a1 = machine.Pin(D1, machine.Pin.OUT) #A-, speed
motor_a2 = machine.Pin(D3, machine.Pin.OUT) #A+, dir
motor_b1 = machine.Pin(D2, machine.Pin.OUT) #B-, speed
motor_b2 = machine.Pin(D4, machine.Pin.OUT) #B+, dir
FWD = 1
REV = 0

def car_fwd():
    motor_a1.value(1)
    motor_a2.value(FWD)
    motor_b1.value(1)
    motor_b2.value(FWD)

def car_rev():
    motor_a1.value(1)
    motor_a2.value(REV)
    motor_b1.value(1)
    motor_b2.value(REV)

def car_stop():
    motor_a1.value(0)
    motor_a2.value(FWD)
    motor_b1.value(0)
    motor_b2.value(FWD)

def car_right():
    motor_a1.value(0)     #r
    #motor_a2.value(FWD)
    motor_b1.value(1)     #l
    motor_b2.value(FWD)

def car_left():
    motor_a1.value(1)
    motor_a2.value(FWD)
    motor_b1.value(0)
    #motor_b2.value(REV)

# 快速右轉
def car_right2():
    motor_a1.value(1)
    motor_a2.value(REV)
    motor_b1.value(1)
    motor_b2.value(FWD)    

# 快速左轉
def car_left2():
    motor_a1.value(1)
    motor_a2.value(FWD)
    motor_b1.value(1)
    motor_b2.value(REV)


def ping(trigPin, echoPin):
    '''
        return: distance (cm)
    '''
    trig=Pin(trigPin, Pin.OUT)
    echo=Pin(echoPin, Pin.IN)
    trig.value(1)
    time.sleep_us(10)
    trig.value(0)
    timeout=False
    tm_start=time.ticks_us() 
    while not echo.value(): #wait for HIGH, 3000us timeout
        if(time.ticks_diff(time.ticks_us(), tm_start)>3000):
            timeout=True
            break
    if timeout: #timeout return 0
        pass
    else: #got HIGH pulse:calculate duration
        tm_start=time.ticks_us()
        tm_delta = 0
        while echo.value(): #wait for LOW
            tm_delta = time.ticks_diff(time.ticks_us(), tm_start)
            if(tm_delta>3000):
                timeout=True
                break
        if timeout:
            pass
        else:
            tm_delta = time.ticks_diff(time.ticks_us(), tm_start)
            duration=tm_delta
    
    if timeout:
        return 999 #cm, for timeout
        
    return duration/58


len_f = None
distance_r = None
distance_l = None

# go~
car_fwd()
while(True):
    distance=ping(trigPin=D7,echoPin=D8)
    if distance>25:
        car_fwd()
    else:
        car_stop()
        time.sleep(0.5)
        car_right2()
        time.sleep(0.25)
        car_stop()
        time.sleep(0.5)
        distance_r = ping(trigPin=D7,echoPin=D8)
        print("distance_r = " + str(distance_r))
        time.sleep(0.1)

        car_left2()
        time.sleep(0.5)
        car_stop()
        time.sleep(0.5)
        distance_l = ping(trigPin=D7,echoPin=D8)
        print("distance_l = " + str(distance_l))
        time.sleep(0.1)
        
        car_right2()
        time.sleep(0.25)
        car_stop()
        time.sleep(0.5)
        distance = ping(trigPin=D7,echoPin=D8)
        print("distance = " + str(distance))
        time.sleep(0.5)
        
        if(distance_r>distance_l):
            car_right2()
        else:
            car_left2()
        time.sleep(0.25)

    time.sleep(0.1)