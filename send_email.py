from ObjectDetectionModule import *
import cv2
import picamera
from tkinter import *
import os
import smtplib
from tkinter.messagebox import *
from time import sleep
from datetime import datetime
import datetime
from email.message import EmailMessage
import ssl
import imghdr
from subprocess import call
import time
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
TRIG = 18  # Trigger activates the sensor which is the GPIO.OUT Pin
ECHO = 24  # ECHO returns the signal which must be read by the GPIO.IN Pin
LED_PIN = 6
RGB_PIN = 16

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.setup(RGB_PIN, GPIO.OUT)
GPIO.setup(4, GPIO.OUT)

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)



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

def Check_Dist(input):
    if input < 7:
        GPIO.output(LED_PIN, GPIO.HIGH)
        for i in range (3):
            GPIO.output(4, GPIO.HIGH)
            time.sleep(.80)
            GPIO.output(4, GPIO.LOW)
            time.sleep(.20)
    else:
        GPIO.output(LED_PIN, GPIO.LOW)
        GPIO.output(4, GPIO.LOW)
        GPIO.output(16, GPIO.HIGH)

try:
    
    while True:
        success, img = cap.read()
        results, objectInfo = getObjects(img, objects=['person'])
        
        # determine what the camera sees using objectInfo
        print(objectInfo)
        
        cv2.imshow("Object Detection Module", img)
        cv2.waitKey(2)
        
        if any('person' in info for info in objectInfo):
            print("PERSON SEEN")
            # Take a picture and save it with the current date and time
            now = datetime.datetime.now()
            timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
            pic_name = f"{timestamp}.jpg" # define the filename with the current date and time
            cv2.imwrite(pic_name, img)
            print("Picture saved as:", pic_name)
            
            cap.release()
            cv2.destroyAllWindows()
            
            email_sender = 'cmpt.2200.001@gmail.com'
            email_password = 'ztbwirvvkoljmqnr'
            email_receiver = 'minerezacraft@gmail.com'
            subject = "Alert: Camera Detected a Potential Threat"
            body = "Hello Reza, our monitoring system detected a potential threat around your property. Stay vigilant."
            
            em = EmailMessage()
            em['From'] = email_sender
            em['To'] = email_receiver
            em['Subject'] = subject
            em.set_content(body)
            
            context = ssl.create_default_context()
            
            with open(pic_name, 'rb') as f:
                file_data = f.read()
                file_type = imghdr.what(f.name)
                file_name = f.name
            
            em.add_attachment(file_data, maintype='image', subtype=file_type, filename=file_name)
            
            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                smtp.login(email_sender, email_password)
                smtp.sendmail(email_sender, email_receiver, em.as_string())
        
        # measure the distance
        dist = distance()
        print("Distance: {:.2f} cm".format(dist))
        
        # if the distance is less than 7cm, turn on
        if any('person' in info for info in objectInfo):
            print("PERSON SEEN")
            # Take a picture and save it with the current date and time
            now = datetime.datetime.now()
            timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
            pic_name = f"{timestamp}.jpg" # define the filename with the current date and time
            cv2.imwrite(pic_name, img)
            print("Picture saved as:", pic_name)

            # Send an email with the picture attachment
            email_sender = 'cmpt.2200.001@gmail.com'
            email_password = 'ztbwirvvkoljmqnr'
            email_receiver = 'minerezacraft@gmail.com'
            subject = "Alert: Camera Detected a Potential Threat "
            body = "Hello Reza, our monitoring system detected a potential threat around your property. Stay vigilant."  
            
            em = EmailMessage()
            em['From'] = email_sender
            em['To'] = email_receiver
            em['Subject'] = subject
            em.set_content(body)

            context = ssl.create_default_context()

            with open(pic_name, 'rb') as f:
                file_data = f.read()
                file_type = imghdr.what(f.name)
                file_name = f.name
                
            em.add_attachment(file_data, maintype='image', subtype=file_type, filename=file_name)
            
            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                smtp.login(email_sender, email_password)
                smtp.sendmail(email_sender, email_receiver, em.as_string())
        
        dist = distance()
        print("Distance: {:.2f} cm".format(dist))
        Check_Dist(dist)
        
        cv2.imshow("Object Detection Module", img)
        cv2.waitKey(15)


except KeyboardInterrupt:
    GPIO.output(16,False)
    GPIO.output(17,False)
    GPIO.cleanup()
    cap.release()
    cv2.destroyAllWindows()