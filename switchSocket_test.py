#!/usr/bin/python3
# -*- coding: utf-8 -*-

import argparse
import cRcSocketSwitch
import time
import logging

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

logging.warning(args)

# set gpio pin
gpio_pin = 17

# values for on
values1 = (args.SystemCode, args.ButtonCode, args.status)

# values for off just for testing
values2 = (args.SystemCode, args.ButtonCode, not args.status)

if __name__ == '__main__':

    try:
        # create Brennenstuhl RCS1000N object 
        obj = cRcSocketSwitch.RCS1000N(gpio_pin)
    except Exception as err:
        logging.error("Error during instantiation of RCS1000N: ", err)
    else:
        # prepare and send values
        obj.send(*values1)
        time.sleep(5)
        obj.send(*values2)
    finally:
        pass
