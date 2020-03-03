#!/usr/bin/python3

import binascii
import base64
import re

__author__ = "Eduardo Pérez-Malumbres Cervera."
__copyright__ = "Copyright 2020, GuadalPING SL"
__credits__ = ["Ismael Joyera Aguilera", "Diego Gamaza", "Alejandro Santamery"]
__license__ = "GNU/GPLv3"
__version__ = "1.0.0"
__email__ = "guadalping@gmail.com"

class Mac2IPv6:
    def __init__(self):
        self.mac = ""
        self.mac2 = ""
        self.mac_2list = []
        self.last = 0
        
    def addfffe(self, mac):
        self.mac = mac[0:8] + ":fffe" + mac[8:]

    def replace7bit(self):
        self.mac_2 = bin(int(self.mac[0:2], 16))[2:].zfill(8)
        for str1 in self.mac_2:  # to list second chr bin
            self.mac_2list += str1
        if self.mac_2list[-2] == "1":  # invert 7 bit
            self.mac_2list[-2] = "0"
        else:
            self.mac_2list[-2] = "1"
             
        self.mac_2 = ''.join(str(v) for v in self.mac_2list)  # to str

        self.mac_2list = []  # clear list

        for i in self.mac:
            self.mac_2list += i  # mac to list ( for adding inverted 7 bit chr )
        
        self.mac_2list[0], self.mac_2list[1] = list(hex(int(self.mac_2, 2))[2:])
    
    def addfe89(self):
        self.final = "fe80::" + ''.join(str(v) for v in self.mac_2list)
        
    def parse(self):
        self.final = self.final.replace(":","")
        self.mac =""
        for i in range(4,24,4):
            if self.last == 0:
                self.mac += self.final[self.last:i] + "::"
            elif self.last == 16:
                self.mac += self.final[self.last:i] + "/64"
            else:
                self.mac += self.final[self.last:i] + ":"
            self.last = i

class convertipv4:
    def __init__(self):
        self.ip = ""
        
    def iptohex(self, ip):
        self.ip = ip
        self.ip = self.ip.split(".")
        self.ip = '{:02X}{:02X}{:02X}{:02X}'.format(*map(int, self.ip))
        
    def parse(self):
        self.ip = self.ip[0:4] + ":" + self.ip[4:]
        
    def add2002(self):
        self.ip = "2002:" + self.ip
    
    def finalformat(self):
        self.ip += "::1/64"

def converttoipv6():
    convert = Mac2IPv6()
        
    mac = input("\nInsert MAC: ")
    
    if "-" in mac:
        mac = mac.replace("-",":").upper()
        
    pattern = re.compile("([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})")
    if not pattern.match(mac):
        print("MAC not valid!\n")
        return 0
        
    # convert to ipv6 step by step
    convert.addfffe(mac)
    convert.replace7bit()
    convert.addfe89()
    convert.parse()
    print("-> \"\033[94m" + convert.mac + "\033[0m\"\n")

def ipv4to6():
    changeip = convertipv4()
    
    ipv4 = input("\nInsert IPv4: ")
    pattern = re.compile("^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
    if not pattern.match(ipv4):
        print("IP not valid!\n")
        return 0
        
    changeip.iptohex(ipv4)
    changeip.parse()
    changeip.add2002()
    changeip.finalformat()
    print("-> \"\033[94m" + changeip.ip + "\033[0m\"\n")

def main():
    print("""\033[1m
                       _       _       _             
                      | |     | |     (_)            
  __ _ _   _  __ _  __| | __ _| |_ __  _ _ __   __ _ 
 / _` | | | |/ _` |/ _` |/ _` | | '_ \| | '_ \ / _` |
| (_| | |_| | (_| | (_| | (_| | | |_) | | | | | (_| |
 \__, |\__,_|\__,_|\__,_|\__,_|_| .__/|_|_| |_|\__, |
  __/ |                         | |             __/ |
 |___/                          |_|            |___/ 

\033[0m""")
    a = ""
    
    while a is not "q":
        print("Select an option ['q' to exit]")
        print("1) Convert from MAC to IPv6")
        print("2) Convert IPv4 to IPv6")
        a = input(">>> ")

        if a == "1":
            converttoipv6()
        if a == "2":
            ipv4to6()
            
if __name__ == "__main__":
    main()
