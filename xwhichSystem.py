#!/usr/bin/python3
#coding: utf-8

import threading
from queue import Queue
import time

from netaddr import IPNetwork
import re, sys, subprocess

# python3 wichSystem.py 10.10.10.188

if len(sys.argv) != 2:
    print("\n[!] Uso: python3 " + sys.argv[0] + " <direccion-ip>\n")
    sys.exit(1)

def scanner(ip):

    def get_ttl(ip):

        proc = subprocess.Popen(["/bin/ping -c 1 %s" % ip, ""], stdout=subprocess.PIPE, shell=True)
        (out,err) = proc.communicate()

        out = out.split()
        out = out[12].decode('utf-8')

        ttl_value = re.findall(r"\d{1,3}", out)[0]

        return ttl_value

    def get_os(ttl):

        ttl = int(ttl)

        if ttl >=40  and ttl <= 64:
            return "Linux"
        elif ttl >= 65 and ttl <= 125:
            return "VoIP,impresora,COMAP,etc.."
        elif ttl >=126 and ttl <=128:
            return "Windows"
        elif ttl >= 240 and ttl <= 255:
            return "Unix (Switch,impresora,telefono,etc...)"
        else:
            return "Not Found"

    if __name__ == '__main__':

        ip_address = sys.argv[1]

        ttl = get_ttl(ip)

        os_name = get_os(ttl)
        if os_name != "Not Found":
            print("\n%s (ttl -> %s): %s" % (ip, ttl, os_name))

#mostar = scanner('ip','ttl')
#mostar

threads = []
for ips in IPNetwork(sys.argv[1]):
    t = threading.Thread(target=scanner,args=(ips,))
    threads.append(t)
    t.start()
