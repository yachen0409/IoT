import adafruit_dht
import board
import time
import RPi.GPIO as GPIO
import urllib.request
import requests
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()
dht_device = adafruit_dht.DHT22(board.D18, use_pulseio = False) # DHT22 Initilization

GPIO.setwarnings(False)
GPIO.setup(26, GPIO.IN)         # PIR Initilization
GPIO.setup(23, GPIO.OUT, initial=GPIO.LOW)      # Fan initialization
GPIO.setup(21, GPIO.IN) # LDR initialization

def thingspeak_post_temphumd(t, h, m, r, l):
    URl='https://api.thingspeak.com/update?api_key='
    KEY='P2U9EJ5MPC39SESS'
    HEADER='&field1={}&field2={}&field3={}&field4={}&field5={}'.format(t, h, m, r, l)
    NEW_URL=URl+KEY+HEADER
    print(NEW_URL)
    data=urllib.request.urlopen(NEW_URL)
    print(data)
def read_data_fan():
    URL='https://api.thingspeak.com/channels/1625967/fields/1.json?api_key='
    KEY='FYJ6KK8XYZ7ZCQBV'
    HEADER='&results=1'
    NEW_URL=URL+KEY+HEADER
    get_data = requests.get(NEW_URL).json()
    print(get_data)
    return get_data['feeds'][0]['field1']
def ldr():
    count = 0
    GPIO.setup(21, GPIO.OUT)     #Output on the pin
    GPIO.output(21, GPIO.LOW)
    time.sleep(0.1)
    GPIO.setup(21, GPIO.IN)       #Change the pin back to input
    while (GPIO.input(21) == GPIO.LOW):     #Count until the pin goes high
        count += 1
    return count
def fan(data):
    if data == 1:
        GPIO.output(23, GPIO.LOW)
        return 1
    else:
        GPIO.output(23, GPIO.HIGH)
        return 0
def read():
    global humidity, temp
    try:
        humidity= dht_device.humidity
        temp = dht_device.temperature
    except(RuntimeError):
        print("no new data this loop!")
    return temp, humidity
def pir():              # Return PIR data
    i = GPIO.input(26)
    if i == 1:
        print("someone is here!!!")
        return i
    else:
        return i
def readrfid():
    readornot = 0
    id = reader.read_id_no_block()
    if id != None:
        readornot = 1
        print("rfid detected!!!")
        return readornot
    return readornot
while True:
    try:
        tem, hum = read()
        p = pir()
        rfid = readrfid()
        l = ldr()
        curf = read_data_fan()
        thingspeak_post_temphumd(tem, hum, p, rfid, l)
        fop = fan(float(curf))
        time.sleep(5)
        rfid = readrfid()
        time.sleep(5)

    except KeyboardInterrupt:
    # If there is a KeyboardInterrupt (when you press ctrl+c), exit the program and cleanu
        print("Cleaning up!")
        GPIO.output(23, GPIO.LOW)
        GPIO.cleanup()
        exit(1)