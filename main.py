import machine
import struct
import time
import pycom
import socket
import ubinascii
from pycoproc_1 import Pycoproc
#from LIS2HH12 import LIS2HH12
from SI7006A20 import SI7006A20
#from LTR329ALS01 import LTR329ALS01
#from MPL3115A2 import MPL3115A2,ALTITUDE,PRESSURE
from network import LoRa

pycom.heartbeat(False)
pycom.rgbled(0x0A0A08) # white
py = Pycoproc(Pycoproc.PYSENSE)
si = SI7006A20(py)

# Initialise LoRa in LORAWAN mode.
# Please pick the region that matches where you are using the device:
# Asia = LoRa.AS923
# Australia = LoRa.AU915
# Europe = LoRa.EU868
# United States = LoRa.US915
lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.US915)

# create an OTAA authentication parameters, change them to the provided credentials
app_eui = ubinascii.unhexlify('0000000000000000')
app_key = ubinascii.unhexlify('B6BE795FEF32A6C574F40583BE3A9997')
#uncomment to use LoRaWAN application provided dev_eui
dev_eui = ubinascii.unhexlify('70B3D5499C0219DF')

# Uncomment for US915 / AU915 & Pygate
# for i in range(0,8):
#     lora.remove_channel(i)
for i in range(16,65):
    lora.remove_channel(i)
for i in range(66,72):
    lora.remove_channel(i)

# join a network using OTAA (Over the Air Activation)
#uncomment below to use LoRaWAN application provided dev_eui
lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0)
#lora.join(activation=LoRa.OTAA, auth=(dev_eui, app_eui, app_key), timeout=0)

# wait until the module has joined the network
while not lora.has_joined():
    time.sleep(2.5)
    print('Not yet joined...')

print('Joined')
# create a LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

# set the LoRaWAN data rate
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)

while True:
    # make the socket blocking
    # (waits for the data to be sent and for the 2 receive windows to expire)
    s.setblocking(True)
    temperature = si.temp()
    humidity = si.humidity()
    # Convert to byte array for transmission
    payload = struct.pack(">ff", temperature,humidity)
    s.send(payload)
    print("Bytes sent, sleeping for 10 secs")
    time.sleep(10)
    # make the socket non-blocking
    # (because if there's no data received it will block forever...)
    s.setblocking(False)
    # get any data received (if any...)
    data = s.recv(64)
    print(data)    
    
# send some data
#s.send(bytes([0x01, 0x02, 0x03]))


