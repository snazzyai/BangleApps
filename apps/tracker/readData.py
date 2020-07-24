import asyncio
import array
from bleak import discover
from bleak import *

address = "D0:10:36:B3:B8:D2"
UUID_NORDIC_TX = "6e400002-b5a3-f393-e0a9-e50e24dcca9e"
UUID_NORDIC_RX = "6e400003-b5a3-f393-e0a9-e50e24dcca9e"
#command = b"\x03\x10clearInterval()\n\x10setInterval(function() {require(\"Storage\").read(\"43815937\"),500)});\n"
#command = b"\x03\x10var f = require('Storage').open('walking','r')\n\x10print(f.read(10000))\n"
command = b"\x03\x10print(require('Storage').readJSON('track.d',true))\n"
#command = "\x03\x10var f = require('Storage')\n\x10 print(f.list())\n\x10print(f.readLine())\n"

def uart_data_received(sender, data):
    print(data.decode("utf-8"))

#You can scan for devices with:
async def run1():
    devices = await discover()
    for d in devices:
         print(d)

# print("Connecting...")
async def run(address, loop):
    # devices = await BleakScanner.discover()
    # for d in devices:
    #    print(d)
    async with BleakClient(address, loop=loop) as client:
        print("Connected")
        await client.start_notify(UUID_NORDIC_RX, uart_data_received)
        print("Writing command")
        c=command
        while len(c)>0:
          await client.write_gatt_char(UUID_NORDIC_TX, bytearray(c[0:20]), True)
          c = c[20:]
        print("Waiting for data")
        await asyncio.sleep(1.0, loop=loop) # wait for a response
        print("Done!")
        await client.disconnect()



#
loop = asyncio.get_event_loop()
loop.run_until_complete(run(address, loop))
#loop.run_until_complete(run())
