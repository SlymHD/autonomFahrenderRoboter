import RPi.GPIO as GPIO
from time import sleep

#GPIO Mode (BOARD / BCM) ---> BCM
GPIO.setmode(GPIO.BCM)

#ausschalten von Warnungen
GPIO.setwarnings(False)
 
class Motor():
    def __init__(self,EnaA,In1A,In2A,EnaB,In1B,In2B):
        #definieren von veriablen EnaA, In1A, In2A jewils für 2 Motoren
        self.EnaA = EnaA
        self.In1A = In1A
        self.In2A = In2A
        self.EnaB = EnaB
        self.In1B = In1B
        self.In2B = In2B

        #alle definierten GPIO Pins auf OUT setzen
        GPIO.setup(self.EnaA,GPIO.OUT)
        GPIO.setup(self.In1A,GPIO.OUT)
        GPIO.setup(self.In2A,GPIO.OUT)
        GPIO.setup(self.EnaB,GPIO.OUT)
        GPIO.setup(self.In1B,GPIO.OUT)
        GPIO.setup(self.In2B,GPIO.OUT)

        #starten von einem PWM (Pulse Width Modulation für beide Motoren)
        self.pwmA = GPIO.PWM(self.EnaA, 100)
        self.pwmA.start(0)
        self.pwmB = GPIO.PWM(self.EnaB, 100)
        self.pwmB.start(0)
 
    def move(self,speed=0.5,turn=0,t=0):
        #multiplizieren von turn und speed mit 100 damit sie im PWM bereich liegen
        speed *=100
        turn *=100

        #damit sich der Roboter ggf. dreht wird je nach eingang die turn Variable von speed subtrahiert damit sich die Motoren
        #unterschiedlich drehen und der Roboter dreht 
        leftSpeed = speed - turn
        rightSpeed = speed + turn

        #wenn leftspeed oder rightspeed ausserhalb des PWM bereiches befinden, werden sie auf wieder in den bereich gebracht
        if leftSpeed>100: 
            leftSpeed=100

        elif leftSpeed<-100: 
            leftSpeed= -100

        if rightSpeed>100: 
            rightSpeed=100

        elif rightSpeed<-100: 
            rightSpeed= -100

        #einsetzen der Werte in den PWM
        self.pwmA.ChangeDutyCycle(abs(leftSpeed))
        self.pwmB.ChangeDutyCycle(abs(rightSpeed))

        #damit sich die motoren drehen werden die Variablen auf HIGH und LOW gesetzt je nach dem wohin der Roboter fahren wird
        #leftspeed und rightspeed sind die jeweiligen motoren
        if leftSpeed>0:
            GPIO.output(self.In1A,GPIO.HIGH)

        else:
            GPIO.output(self.In1A,GPIO.LOW)
            GPIO.output(self.In2A,GPIO.HIGH)
 
        if rightSpeed>0:
            GPIO.output(self.In1B,GPIO.HIGH)
            GPIO.output(self.In2B,GPIO.LOW)
        else:
            GPIO.output(self.In1B,GPIO.LOW)
            GPIO.output(self.In2B,GPIO.HIGH)
 
        sleep(t)
    #fuktion Stop beendet den PWM und schaltet die Motoren ab    
    def stop(self,t=0):
        self.pwmA.ChangeDutyCycle(0)
        self.pwmB.ChangeDutyCycle(0)
        sleep(t)

