import RPi.GPIO as GPIO
import time
 
#GPIO Mode (BOARD / BCM) ---> BCM
GPIO.setmode(GPIO.BCM)
 
#defenieren von GPIO Pins
GPIO_TRIGGER = 6
GPIO_ECHO = 5

#setzen der richtung der GPIO Pins (IN /OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
 
def distance():
    # setzen des Trigger Pins auf HIGH
    GPIO.output(GPIO_TRIGGER, True)

    #nach 0.01ms setzen des Trigger Pins wieder auf LOW 
    time.sleep(0.0001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # speichern von StartTime nach aussenden des Signals
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # speichern von Stop Time nach empfangen des Signals
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # berechnen der Zeitdifferenz zwischen start und stop
    TimeElapsed = StopTime - StartTime
    # multiplizieren mit der Schallgeschwindigkeit (34300 cm/s)
    # und durch 2 dividieren, weil der Schall hin und zurück kommt
    distance = (TimeElapsed * 34300) / 2

    return distance

