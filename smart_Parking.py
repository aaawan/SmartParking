import RPi.GPIO as GPIO
from gpiozero import Servo
import Adafruit_CharLCD as LCD
import time
import pymysql
import requests
import sys

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM) # set GPIO mode to board mode
GPIO.cleanup() # cleaning up GPIO pins


#variable declaration for IR sensor 
totalcar=0
car1=0
car2=0
car3=0
car4=0
car5=0
car6=0
car7=0
car8=0
#variable for serversite....
cursor=0
database=0

#database updating
def updatedatabase(atr,vl):
    global cursor
    global database
    cursor.execute("Update ParkingSlot set %s= %s"%(atr,vl))
    database.commit()
   
#servo motor pin declaration
myGPIO=2
servo = Servo(myGPIO)

#servo motor function
def ServoM():
    servo.mid()
    time.sleep(0.5)
    servo.max()
    time.sleep(2)
    servo.mid()

#LCD pin declaration
lcd_rs = 10
lcd_en = 9
lcd_d4 = 25
lcd_d5 = 11
lcd_d6 = 8
lcd_d7 = 7
lcd_backlight = 4

#lcd initialization
lcd_columns = 16
lcd_rows = 2
lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_backlight)

#LCD function
def LCDf() :
    # Define LCD column and row size for 16x2 LCD.
    
    lcd.clear()
    if totalcar==4:
    	lcd.message('NO empty slots')
    else :
    	lcd.message('empty slots : '+ str(5-totalcar))

	
#sonar pin declaration
TRIG=20
ECHO=21

# sonar sensor function
def Sonar():
    GPIO.setup(TRIG,GPIO.OUT)
    GPIO.setup(ECHO,GPIO.IN)
    GPIO.output(TRIG,False)
    time.sleep(2)
    GPIO.output(TRIG,True)
    time.sleep(0.00001)
    GPIO.output(TRIG,False)
	
    while GPIO.input(ECHO)==0:
    	pulse_start=time.time()
    while GPIO.input(ECHO)==1:
    	pulse_end=time.time()
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    distance = round(distance, 2)
    print ("Distance:",distance,"cm")
    if distance<=25 :
    	return True
    else :
    	return False

#IR sensor pin declaration
#  irsensor--->1
IRTrackingPin1 = 19
OutLedPin1 = 26

#  irsensor--->2
IRTrackingPin2 = 5
OutLedPin2 = 6

#  irsensor--->3
IRTrackingPin3 = 17
OutLedPin3 = 18

#  irsensor--->4
IRTrackingPin4 = 27
OutLedPin4 = 22

#  irsensor--->5
IRTrackingPin5 = 23
OutLedPin5 = 24

#irsensor---> 6
IRTrackingPin6 = 3
OutLedPin6 = 4

#irsensor---> 7
IRTrackingPin7 = 12
OutLedPin7 = 13

#irsensor---> 8
IRTrackingPin8 = 14
OutLedPin8 = 15

#Set the GPIO pins as numbering with IR
def IRsetup():
    GPIO.setup(OutLedPin1, GPIO.OUT) # Set the OutLedPin's mode is output
    GPIO.setup(OutLedPin2, GPIO.OUT) 
    GPIO.setup(OutLedPin3, GPIO.OUT)
    GPIO.setup(OutLedPin4, GPIO.OUT)
    GPIO.setup(OutLedPin5, GPIO.OUT)
    GPIO.setup(OutLedPin6, GPIO.OUT)
    GPIO.setup(OutLedPin7, GPIO.OUT)
    GPIO.setup(OutLedPin8, GPIO.OUT)
    GPIO.setup(IRTrackingPin1, GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(IRTrackingPin2 , GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(IRTrackingPin3 , GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(IRTrackingPin4 , GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(IRTrackingPin5 , GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(IRTrackingPin6 , GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(IRTrackingPin7 , GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(IRTrackingPin8 , GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
    GPIO.output(OutLedPin1, GPIO.LOW) # Set the OutLedPin high(+3.3V) to off led
    GPIO.output(OutLedPin2, GPIO.LOW) 
    GPIO.output(OutLedPin3, GPIO.LOW)
    GPIO.output(OutLedPin4, GPIO.LOW)
    GPIO.output(OutLedPin5, GPIO.LOW)
    GPIO.output(OutLedPin6, GPIO.LOW)
    GPIO.output(OutLedPin7, GPIO.LOW)
    GPIO.output(OutLedPin8, GPIO.LOW)
    time.sleep(3)

#IR sensor function
def IR() :
    global totalcar
    global car1
    global car2
    global car3
    global car4
    global car5
	
    #for car 1
    LCDf()
    if GPIO.input(IRTrackingPin1) == GPIO.HIGH:
        GPIO.output(OutLedPin1, GPIO.HIGH)# Set the OutLedPin turn HIGH/ON
        updatedatabase('slot1',1)
        if car1==0:
            car1=1
            totalcar=totalcar+1
        time.sleep(3)
    else:
        GPIO.output(OutLedPin1, GPIO.LOW) # Set the OutLedPin turn LOW/OFF
        updatedatabase('slot1',0)
        if car1==1:
            car1=0
            totalcar=totalcar-1
        time.sleep(3)
	
	 #for car2   
    LCDf()
    if GPIO.input(IRTrackingPin2) == GPIO.HIGH:
        GPIO.output(OutLedPin2, GPIO.HIGH)# Set the OutLedPin turn HIGH/ON
        updatedatabase('slot2',1)
        if car2==0:
            car2=1
            totalcar=totalcar+1
        time.sleep(3)
    else:
        GPIO.output(OutLedPin2, GPIO.LOW) # Set the OutLedPin turn LOW/OFF
        updatedatabase('slot2',0)
        if car2==1:
            car2=0
            totalcar=totalcar-1
                
        time.sleep(3)
	
     #for car3   
    LCDf()
    if GPIO.input(IRTrackingPin3) == GPIO.HIGH:
        GPIO.output(OutLedPin3, GPIO.HIGH)# Set the OutLedPin turn HIGH/ON
        updatedatabase('slot3',1)
        if car3==0:
            car3=1
            totalcar=totalcar+1
        time.sleep(3)
    else:
        GPIO.output(OutLedPin3, GPIO.LOW) # Set the OutLedPin turn LOW/OFF
        updatedatabase('slot3',0)
        if car3==1:
            car3=0
            totalcar=totalcar-1
                
        time.sleep(3)
	
	 #for car4   
    LCDf()
    if GPIO.input(IRTrackingPin4) == GPIO.HIGH:
        GPIO.output(OutLedPin4, GPIO.HIGH)# Set the OutLedPin turn HIGH/ON
        updatedatabase('slot4',1)
        if car4==0:
            car4=1
            totalcar=totalcar+1
        time.sleep(3)
    else:
        GPIO.output(OutLedPin4, GPIO.LOW) # Set the OutLedPin turn LOW/OFF
        updatedatabase('slot4',0)
        if car4==1:
            car4=0
            totalcar=totalcar-1
                
        time.sleep(3)	
		
     #for car5   
    if GPIO.input(IRTrackingPin5) == GPIO.HIGH:
        GPIO.output(OutLedPin5, GPIO.HIGH)# Set the OutLedPin turn HIGH/ON
        updatedatabase('slot5',1)
        if car5==0:
            car5=1
            totalcar=totalcar+1
        time.sleep(3)
    else:
        GPIO.output(OutLedPin5, GPIO.LOW) # Set the OutLedPin turn LOW/OFF
        updatedatabase('slot5',0)
        if car5==1:
            car5=0
            totalcar=totalcar-1
                
        time.sleep(3)
        
     #for car6   
    if GPIO.input(IRTrackingPin6) == GPIO.HIGH:
        GPIO.output(OutLedPin6, GPIO.HIGH)# Set the OutLedPin turn HIGH/ON
        updatedatabase('slot6',1)
        if car6==0:
            car6=1
            totalcar=totalcar+1
        time.sleep(3)
    else:
        GPIO.output(OutLedPin6, GPIO.LOW) # Set the OutLedPin turn LOW/OFF
        updatedatabase('slot6',0)
        if car6==1:
            car6=0
            totalcar=totalcar-1
                
        time.sleep(3)
	
     #for car7   
    if GPIO.input(IRTrackingPin7) == GPIO.HIGH:
        GPIO.output(OutLedPin7, GPIO.HIGH)# Set the OutLedPin turn HIGH/ON
        updatedatabase('slot7',1)
        if car7==0:
            car7=1
            totalcar=totalcar+1
        time.sleep(3)
    else:
        GPIO.output(OutLedPin7, GPIO.LOW) # Set the OutLedPin turn LOW/OFF
        updatedatabase('slot7',0)
        if car7==1:
            car7=0
            totalcar=totalcar-1
                
        time.sleep(3)
        
     #for car8   
    if GPIO.input(IRTrackingPin8) == GPIO.HIGH:
        GPIO.output(OutLedPin8, GPIO.HIGH)# Set the OutLedPin turn HIGH/ON
        updatedatabase('slot8',1)
        if car8==0:
            car8=1
            totalcar=totalcar+1
        time.sleep(3)
    else:
        GPIO.output(OutLedPin8, GPIO.LOW) # Set the OutLedPin turn LOW/OFF
        updatedatabase('slot8',0)
        if car8==1:
            car8=0
            totalcar=totalcar-1
                
        time.sleep(3)
    print ("total car-----",totalcar)	
    return totalcar

# connecting the net...........
def Connectnet():
    import requests
    try:
        response = requests.get("http://www.google.com")
        return True
    except requests.ConnectionError:
        return False

#net connection check.............
def ConnectionCheck() :
    checknet=Connectnet()
    if checknet==True :
        print("Connection established")
    else :
        print("CAN'T CONNECT TO THE INTERENET")


# connecting to database......
def connectDatabase() :
    global cursor
    global database
    while True :
        try :
            ConnectionCheck() 
            database = pymysql.connect(host="digitoll.cu.ma",port=3306,user="digitoll_awan",passwd="awan_055",db="digitoll_smart_garaze")
            cursor=database.cursor()
            break
        except :
            print("trying to connect the database.......")
            break
         

#updating the database....

    
        

if __name__ == '__main__': # The Program will start from here
    IRsetup()	


try:
    connectDatabase() 
    while  True:
            TOTAL_CAR=IR()
            flag=Sonar()
            if flag :
                if TOTAL_CAR < 4 :
                    ServoM()
            #LCDf()
            time.sleep(2)
except KeyboardInterrupt:
    GPIO.cleanup()
    lcd.clear()
    database.close()
		
	
	
	
##ended the the hardware part of the project .........	
	
