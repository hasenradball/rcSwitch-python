#!/usr/bin/python3
# -*- coding: utf-8 -*-

from rpi_rf import RFDevice

class RCS1000N:
    '''
    class for switching remote socket devices as:
    Brennenstuhl RCS 1000 N
    I calculated the corresponding send code in decimal value
    and uses the library rpi-rf to send the command via 433 MHz send device 
    '''
    
    def __init__(self, gpio_pin=17):
        '''
        Constructor for GPIO Pin and Configuration
        '''
        self.gpio = gpio_pin
        self.config = {'code': None, 'tx_proto': 1, 'tx_pulselength': 320, 'tx_length': 24}

    def prepareCodes(self, SystemCode_raw, ButtonCode_raw, status):
        '''
        this method prepares the codes and checks the imput format in case
        of different usecases
        '''
        button_list = ['a', 'A', 'b', 'B', 'c', 'C', 'd', 'D', 'e', 'E']
        button_mapping = {'A':16, 'B':8, 'C':4, 'D':2, 'E':1}
        # check if the input for the ButtonCode is in the Case 'A', 'B', etc...
        if ButtonCode_raw in button_list:
            ButtonCode_raw = ButtonCode_raw.upper()
            ButtonCode = button_mapping[ButtonCode_raw]
            ButtonCode = '{:05b}'.format(ButtonCode)
            #print("Buttoncode: ", ButtonCode, end='\n')
        
        # check if the ButtonCode is an integer like 1, 2, 3, etc...
        elif isinstance(ButtonCode_raw, int):
            #print("ButtonCode_raw is of type int")
            ButtonCode = '{:05b}'.format(ButtonCode_raw)
            #print("Buttoncode: ", ButtonCode, end='\n')
        
        # assume the code is in the way '01000' check the length (5)
        elif isinstance(ButtonCode_raw, str):
            #print("ButtonCode_raw is of type str")
            # check length of 5 
            if len(ButtonCode_raw) == 5:
                ButtonCode = ButtonCode_raw
                #print("Buttoncode: ", ButtonCode, ' - ', type(ButtonCode), end='\n')
            else:
                ButtonCode = None
                print("ERROR: wrong len of ButtonCode_raw!")
        
        # check now the lenght of the SystemCode
        if len(SystemCode_raw) == 5:
            SystemCode = SystemCode_raw
            #print("SystemCode: ", SystemCode, ' - ', type(SystemCode), end='\n')
        else:
            SystemCode = None
            print("ERROR: wrong len of SystemCode_raw")
        
        # check the status
        if isinstance(status, bool):
            if status:
                status = 1
            else:
                status = 0
        return (SystemCode, ButtonCode, status)


    def calcTristateCode(self, SystemCode, ButtonCode, status):
        '''
        calculate the corresponding Tristate Code in the same way as the library
        wiringPi does it in c-code
        return value is the TriState String Code
        '''
        code = ""
        for c in SystemCode:
            if c == '0':
                code += 'F'
            else:
                code += '0'
        
        for c in ButtonCode:
            if c == '0':
                code += 'F'
            else:
                code += '0'
        
        if status:
            code += '0F'
        else:
            code += 'F0'
        return code


    def calcBinaryCode(self, strCode):
        '''
        calculate the Binary Code of the switch command in the same way as th library
        wiringPi does it in c-code
        return value is then a decimal value of the switch command
        '''
        code = 0
        len = 0
        for c in strCode:
            code <<= 2
            #print(c, type(c))
            #print(bin(code))
            if c == '0':
                # bit pattern 00
                pass
            elif c == 'F':
                # bit pattern 01 
                code += 1
            elif c =='1':
                # bit pattern 11
                code += 3
            len += 2
        print("Length of code: ", len, end='\n')
        print ("code: ", int(code), end='\n')
        return code


    def calc_DecimalCode_python_style(self, SystemCode, ButtonCode, status):
        '''
        calculate the decimal Code in a python style
        this combines the methods:
        calcTristateCode + calcBinaryCode in on step
        '''
        code = str(SystemCode + ButtonCode)
        help = code.replace('0', 'F').replace('1', '0')
        if status:
            help += '0F'
        else:
            help += 'F0'
        print("Py - TriState code: ", help)
        code = help.replace('0','00').replace('F', '01')
        binstr = '0b' + code
        #print(binstr)
        return int(binstr, 2)

    def send(self, systemCode, btn_code, status):
        '''
        Method to prepare the codes and send it to the actuator
        '''
        try:
            rfdevice = RFDevice(17)
            rfdevice.enable_tx()
            rfdevice.tx_repeat = 10
            values = self.prepareCodes(systemCode, btn_code, status)
            send_code = self.calc_DecimalCode_python_style(*values)
            self.config['code'] = send_code
            rfdevice.tx_code(**self.config)

        finally:
            rfdevice.cleanup()