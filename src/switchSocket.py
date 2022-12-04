#!/usr/bin/python3
# -*- coding: utf-8 -*-

import argparse
import cRcSocketSwitch
from rpi_rf import RFDevice
import time

parser = argparse.ArgumentParser(
    prog = 'switchSocket',
    description = 'Switches an 433 MHz remote socket device',
    epilog = 'shows this help information')

parser.add_argument('SystemCode', metavar = 'SystemCode', type = str,
                    help="SystemCode of device")

parser.add_argument('ButtonCode', type = str,
                    help="Buttoncode of device")

parser.add_argument('status', type = int,
                    help="Status of device (on/off)")

args = parser.parse_args()

parser.parse_args()

print(args)

gpio_pin = 17
vals1 = (args.SystemCode, args.ButtonCode, args.status)
vals2 = (args.SystemCode, args.ButtonCode, not args.status)

if __name__ == '__main__':

    try:
        # set GPIO PIN -> 17
        rfdevice = RFDevice(17)
        rfdevice.enable_tx()
        rfdevice.tx_repeat = 10

        # calculate the sending code in decimal
        obj = cRcSocketSwitch.RCS1000N(gpio_pin)
        obj.send(*vals1)

        time.sleep(5)

        obj.send(*vals2)

    finally:
        pass
