#!/usr/bin/env python

import subprocess
import optparse
import re

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change its MAC ADRESS")
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC adress")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] please specify an interface, use --help for more info.")
    elif not options.new_mac:
        parser.error("[-] please specify an new MAC, use --help for more info.")
    return options

def change_mac(interface, new_mac):
    print("[+] CHANGING MAC adress FOR: " + interface + " to " + new_mac)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])



def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    print(ifconfig_result)

    mac_adress_searche_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig_result))

    if mac_adress_searche_result:
        return mac_adress_searche_result.group(0)

    else:
        print("Could not read MAC adress. ")


options = get_arguments()

current_mac = get_current_mac(options.interface)
print("Current MAC = " + str(current_mac))


change_mac(options.interface, options.new_mac)

current_mac = get_current_mac(options.interface)

if current_mac == options.new_mac:
    print("[+] MAC adress was sucessfuly changed to: " + str(current_mac))

else:
    print("[-] MAC adress did not get changed. ")