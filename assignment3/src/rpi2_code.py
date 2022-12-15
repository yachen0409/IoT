import drivers
import requests
import sys
import time
import RPi.GPIO as GPIO
global display
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT, initial=GPIO.LOW)      #LED
GPIO.setup(27, GPIO.OUT, initial=GPIO.LOW)      #BUZZER
def read_data_led():
    URL='https://api.thingspeak.com/channels/1625967/fields/2.json?api_key='
    KEY='FYJ6KK8XYZ7ZCQBV'
    HEADER='&results=2'
    NEW_URL=URL+KEY+HEADER
    get_data = requests.get(NEW_URL).json()
    print(get_data)
    return get_data['feeds'][0]['field2']
def read_data_buzzer():
    URL='https://api.thingspeak.com/channels/1625967/fields/3.json?api_key='
    KEY='FYJ6KK8XYZ7ZCQBV'
    HEADER='&results=3'
    NEW_URL=URL+KEY+HEADER
    get_data = requests.get(NEW_URL).json()
    print(get_data)
    return get_data['feeds'][0]['field3']
def read_data_temp():
    URL='https://api.thingspeak.com/channels/1608288/fields/1.json?api_key='
    KEY='0SRDOB2ZRGWB47CB'
    HEADER='&results=1'
    NEW_URL=URL+KEY+HEADER
    get_data = requests.get(NEW_URL).json()
    print(get_data)
    return get_data['feeds'][0]['field1']
def read_data_humd():
    URL='https://api.thingspeak.com/channels/1608288/fields/2.json?api_key='
    KEY='0SRDOB2ZRGWB47CB'
    HEADER='&results=2'
    NEW_URL=URL+KEY+HEADER
    get_data = requests.get(NEW_URL).json()
    print(get_data)
    return get_data['feeds'][0]['field2']
def read_data_ldr():
    URL='https://api.thingspeak.com/channels/1625967/fields/4.json?api_key='
    KEY='FYJ6KK8XYZ7ZCQBV'
    HEADER='&results=4'
    NEW_URL=URL+KEY+HEADER
    get_data = requests.get(NEW_URL).json()
    print(get_data)
    return get_data['feeds'][0]['field4']
def displaystring(temp, humd, ldr):
    display.lcd_display_string("--------------------", 1)
    display.lcd_display_string("Temp="+temp+"*C", 2)
    display.lcd_display_string("Humidity="+humd+"%", 3)
    display.lcd_display_string("ldr="+ldr, 4)

def lcd(a):
    print("a=", a)
    if a=='1' :
        GPIO.output(17, GPIO.HIGH)
        print("rfid detect!!")
    else:
        GPIO.output(17, GPIO.LOW)
        print("no card yet.....")
def buzzer(b):
    print("b=", b)
    if b=='1':
        GPIO.output(27, GPIO.HIGH)
        print("buzzing!!!!")
        time.sleep(1)
    GPIO.output(27, GPIO.LOW)
try:
    display = drivers.Lcd()
    display.lcd_display_string("Hello from Cloud4RPI", 2)
    time.sleep(2)
    display.lcd_clear()
    while (True):
        t = read_data_temp()
        h = read_data_humd()
        ldr = read_data_ldr()
        lcd(read_data_led())
        buzzer(read_data_buzzer())
        displaystring(t, h, ldr)
        time.sleep(5)
except KeyboardInterrupt:
    print("Cleaning up!")
    GPIO.output(17,GPIO.LOW)
    GPIO.output(27,GPIO.LOW)
    display.lcd_clear()