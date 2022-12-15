import drivers
from time import sleep
import adafruit_dht
import board
import time
import RPi.GPIO as GPIO

# Load the driver and set it to "display"
# If you use something from the driver library use the "display." prefix first
display = drivers.Lcd()

dht_device = adafruit_dht.DHT22(board.D18, use_pulseio = False)

GPIO.setwarnings(False)

GPIO.setup(26, GPIO.IN)         #Read output from PIR motion sensor
GPIO.setup(22, GPIO.OUT, initial=GPIO.LOW)
    
# Main body of code
try:
    while True:
        GPIO.output(22, GPIO.LOW)
        # Remember that your sentences can only be 16 characters long!
        i=GPIO.input(26)
        print("Writing to display")
        try:
            humidity= dht_device.humidity
            temperature = dht_device.temperature
        except(RuntimeError):
            print("no new data this loop!")

        if humidity is not None and temperature is not None:
            display.lcd_display_string("Temp={0:0.2f}*C".format(temperature), 1)
            display.lcd_display_string("Humidity="+str(humidity)+"%", 2)
        else:
            print("Failed to retrieve data from HDT22 sensor")
        if i==0:                 #When output from motion sensor is LOW
            display.lcd_display_string ("No intruders " +str(i), 3)
            GPIO.output(22, GPIO.LOW)  #Turn OFF LED
        elif i==1:               #When output from motion sensor is HIGH
            display.lcd_display_string ("Intruders detected! " +str(i), 3)
            GPIO.output(22, GPIO.HIGH)  #Turn ON LED
        # display.lcd_display_string("Demo Pi Guy code", 3)  # Write line of text to second line of display
        display.lcd_display_string("I am a display!", 4)   # Refresh the first line of display with a different message  
        sleep(1) 
        GPIO.output(22,GPIO.LOW)                                 # Give time for the message to be read
        display.lcd_clear()
        sleep(2)                                           # Give time for the message to be read
except KeyboardInterrupt:
    # If there is a KeyboardInterrupt (when you press ctrl+c), exit the program and cleanup
    print("Cleaning up!")
    GPIO.output(22,GPIO.LOW)
    display.lcd_clear()



