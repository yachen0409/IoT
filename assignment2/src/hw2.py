import sys
import time
from time import sleep
import drivers
import adafruit_dht
import board
import RPi.GPIO as GPIO
import cloud4rpi

TOKEN = '2uWbHQwirKEgNggcTiazPiBAn'     # Cloud4RPI Initialization
DATA_SENDING_INTERVAL = 10              # Set data sending interval
POOL_INTERVAL = 0.5                     # Counter for timeout

dht_device = adafruit_dht.DHT22(board.D18, use_pulseio = False)     # DHT22 Initilization
GPIO.setwarnings(False)                 

GPIO.setup(26, GPIO.IN)                 # PIR Initialization
GPIO.setup(22, GPIO.OUT, initial=GPIO.LOW)  # Buzzer Initialization
def read():     # Read DHT22 Data 
    global humidity, temp
    try:
        humidity= dht_device.humidity
        temp = dht_device.temperature
    except(RuntimeError):               
        print("no new data this loop!")
def humidity():     # Return humidity data
    try:
        read()
        return round(humidity, 2) if humidity is not None else None
    except(TypeError):
        pass
def temp():     # Return temparature data
    try:
        read()
        return round(temp, 2) if temp is not None else None
    except(TypeError):
        pass
def pir():      # Return PIR data
    i = GPIO.input(26)
    if i == 1:
        print("someone is here!!!")
        return True
    else:
        return False
def buzzer_control(value):  # Control Buzzer
    signal = GPIO.LOW
    if value == True:
        signal = GPIO.HIGH
    GPIO.output(22, signal)
    sleep(2)
    return
def lcd():      # Control Display while input = true
    global display
    display = drivers.Lcd()
    display.lcd_display_string("Hello from Cloud4RPI !!!", 2)
    sleep(2)
    display.lcd_clear()
def wait():     # Control Display while input = false
    global display
    display = drivers.Lcd()
    display.lcd_display_string("waiting for signal......", 2)
    sleep(2)

def display(value):     # Control Display
    if value == True:
        lcd()
    else:
        wait()

try:
    # Sending Data to Cloud
    while True:
        variables = {       # Declaring Variables
            'Room Temp':{
                'type': 'numeric',
                'bind': temp
            },
            'Room Humidity':{
                'type': 'numeric',
		        'bind': humidity
            },
            'PIR Sense':{
                'type': 'bool',
                'bind': pir
            },
            'Buzzer On':{
                'type': 'bool',
                'value': False,
                'bind': buzzer_control
            },
            'Display Say Hello':{
                'type':'bool',
                'value':False,
                'bind':display
            },
        }
        device = cloud4rpi.connect(TOKEN)
        try:
            device.declare(variables)
            device.publish_config()
            sleep(1)
            data_timer = 0
            while True:
                if data_timer <= 0:
                    print("send data")
 		            device.publish_data()
                    data_timer = DATA_SENDING_INTERVAL
                    sleep(POOL_INTERVAL)
                data_timer -= POOL_INTERVAL
        except Exception as e:
            error = cloud4rpi.get_error_message(e)
            cloud4rpi.log.exception("ERROR! %s %s", error, sys.exc_info()[0])
        finally:
            sys.exit(0)
except KeyboardInterrupt:
    # If there is a KeyboardInterrupt (when you press ctrl+c), exit the program and cleanup
    print("Cleaning up!")
    GPIO.output(22,GPIO.LOW)
    display.lcd_clear()