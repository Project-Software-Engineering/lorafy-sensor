import time
import pycom
import socket
from pycoproc_1 import Pycoproc
import machine
from network import LoRa
import ubinascii
import micropython


from LIS2HH12 import LIS2HH12
from SI7006A20 import SI7006A20
from LTR329ALS01 import LTR329ALS01
from MPL3115A2 import MPL3115A2,ALTITUDE,PRESSURE

lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)


app_eui = ubinascii.unhexlify('ADA4DAE3AC12676B')
dev_eui = ubinascii.unhexlify('70B3D549968D088F')
app_key = ubinascii.unhexlify('90D4D7362AAABE722949837195D8AC3D')

lora.init(mode=LoRa.LORAWAN, adr=True, public=True)

lora.join(activation=LoRa.OTAA, auth=(dev_eui, app_eui, app_key), dr=0, timeout=0)
while not lora.has_joined():
    print('Not yet joined...')
    time.sleep(3)

print("Joined network")

py = Pycoproc(Pycoproc.PYSENSE)

pressure_sensor = MPL3115A2(py,mode=PRESSURE)
pressure= pressure_sensor.pressure();
print("Pressure: " + str(pressure))
temperature_sensor = SI7006A20(py)
temperature= temperature_sensor.temperature()
light_sensor = LTR329ALS01(py)
light= light_sensor.light()

while True:
     s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
     s.setsockopt(socket.SOL_LORA, socket.SO_DR, 0)
     s.setblocking(True)
     s.send(str(temperature))
     s.send(str(light))
     s.send(str(pressure))
     time.sleep(180)
