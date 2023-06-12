import RPi.GPIO as GPIO
import time


# GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
TRIG = 18 #Trigger activates the sensor which is the GPIO.OUT Pin
ECHO = 24 #ECHO returns the signal which must be read by the GPIO.IN Pin
LED_PIN = 6
RGB_PIN = 16
Motion=12
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.setup(RGB_PIN, GPIO.OUT)
GPIO.setup(17, GPIO.OUT)
GPIO.setup(12, GPIO.IN)


# Function to measure distance
def distance():
    # Set trigger to high
    GPIO.output(TRIG, True)
   
    # Wait for 0.01ms
    time.sleep(0.00001)
   
    # Set trigger to low
    GPIO.output(TRIG, False)
   
    start_time = time.time()
    stop_time = time.time()
   
    # Save the start time
    while GPIO.input(ECHO) == 0:
        start_time = time.time()
   
    # Save the time of arrival
    while GPIO.input(ECHO) == 1:
        stop_time = time.time()
       
    # Time difference between start and arrival
    time_elapsed = stop_time - start_time
   
    # Calculate distance for the ultrasonic distance sensor
    distance = (time_elapsed * 34300) / 2
   
    return distance

def motion():
    x=False
    if GPIO.input(12)==True:
        x=True
    else:
        x=False
    return x

def Check_Dist(input):
    if input < 7:
        GPIO.output(LED_PIN, GPIO.HIGH)
        for i in range (3):
            GPIO.output(17, GPIO.HIGH)
            time.sleep(.80)
            GPIO.output(17, GPIO.LOW)
            time.sleep(.20)
    else:
        GPIO.output(LED_PIN, GPIO.LOW)
        GPIO.output(17, GPIO.LOW)
        GPIO.output(16, GPIO.HIGH)
   
def Check_Motion(input):
   
    if input == True:
        GPIO.output(LED_PIN, GPIO.HIGH)
        for i in range (3):
            GPIO.output(17, GPIO.HIGH)
            time.sleep(.80)
            GPIO.output(17, GPIO.LOW)
            time.sleep(.20)
    else:
        GPIO.output(LED_PIN, GPIO.LOW)
        GPIO.output(17, GPIO.LOW)
        GPIO.output(16, GPIO.HIGH)
   

if __name__ == '__main__':
    try:
        GPIO.output(LED_PIN,GPIO.HIGH)
        while True:
            dist = distance()
            print("Distance: {:.2f} cm".format(dist))
            mot=motion()
           
            # If the distance is less than 100 cm then turn on the LED
           
            Check_Dist(dist)
            Check_Motion(mot)
 
               
            time.sleep(1)
           
    except KeyboardInterrupt:
        GPIO.output(16,False)
        GPIO.output(17,False)
        GPIO.cleanup()
