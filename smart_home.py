 import time
from gpiozero import LED, AngularServo
import sqlite3
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from Adafruit_IO import Client, Feed, RequestError

reader = SimpleMFRC522()
led = LED(17)
ir = 13
servo = AngularServo(26, min_pulse_width=0.0006, max_pulse_width=0.0025)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(ir, GPIO.IN)

ADAFRUIT_IO_KEY = 'aio_EvyF48rKHxT1d1TJ3IWxaZFX0vyI'
ADAFRUIT_IO_USERNAME = 'Buu_1911'
# Create an instance of the REST client.
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

try: # if we have a 'digital' feed
    digital = aio.feeds('smart-home')                           
except RequestError: # create a digital feed
    feed = Feed(name="smart-home")
    digital = aio.create_feed(feed)

def updateData(door, led):
    conn = sqlite3.connect('Data.db')
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS Data (
                number INTEGER PRIMARY KEY NOT NULL, 
                door TEXT DEFAULT 'Doors', 
                doorStatus TEXT NOT NULL, 
                led TEXT DEFAULT 'Led', 
                ledStatus TEXT NOT NULL)""")
    cur.execute(""" INSERT INTO Data ( doorStatus, ledStatus ) VALUES (?,?)  """, (door, led))
    conn.commit()
    conn.close()

while True:
    # motion = GPIO.input(pir)
    print("place your card reader")
    # print(motion)
    
    # if (motion == '1' ):
    #     led.on()
    #     time.sleep(5)

    if (not GPIO.input(ir)):
        serial, text = reader.read()
        print(serial)
        if (serial == 324579780552 ):
            print("authorized")
            led.off()
            servo.angle = 90
            aio.send(digital.key, 0)
            updateData('open', 'off')
            time.sleep(5)
            servo.angle = 0
    if (GPIO.input(ir)):
        print('co nguoi dot nhap')
        aio.send(digital.key, 1)
        updateData('open', 'on')
        led.on()
    # if (not GPIO.input(ir)):
    #     led.off()
    time.sleep(1)
