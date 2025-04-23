#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author deeb


"""
MAC Address Spoofer Script
This script allows users to change the MAC address of a specified network interface. 
It provides options to set a specific MAC address, generate a random MAC address, 
restore the original MAC address, or check the current MAC address status.

Usage:
    Run the script with appropriate arguments to change, randomize, 
    restore, or check the status of the MAC address.
    Use the --help flag to see detailed usage instructions.

Examples:
    1. Change the MAC address of a network interface to a specific address:
       python3 macchanger.py -i <interface> -m 00:11:22:33:44:55

    2. Generate and set a random MAC address for a network interface:
       python3 macchanger.py -i <interface> --random

    3. Restore the original MAC address for a network interface:
       python3 macchanger.py -i <interface> --restore

    4. Check the current MAC address status of a network interface:
       python3 macchanger.py -i <interface> --status

Note:
    - The "ouis" file must be present in the same directory for random MAC generation.
    - The original MAC address is temporarily stored in "/tmp/.original_mac" for restoration.
    - The spoofed MAC address is temporary and will revert to the original MAC address after a system reboot.
"""


import argparse
import re
import signal
import subprocess
import sys
import os
import random
import uuid
from colorama import Fore, Style


def signal_handler(signal, frame):
    '''Handles SIGINT (Ctrl+C) signal to gracefully exit the script.'''

    print("\nExiting...")
    sys.exit(1)

signal.signal(signal.SIGINT, signal_handler)


def get_arguments():
    '''Parses and returns command-line arguments for the script.'''

    parser = argparse.ArgumentParser(description="MAC Address Changer")
    parser.add_argument("-i", "--interface", required=True, dest="interface", help="Network interface to change MAC address")
    parser.add_argument("-m", "--mac", required=False, dest="mac_address", help="New MAC address to set")
    parser.add_argument("--random", required=False, action="store_true", help="Generate a random MAC address")
    parser.add_argument("--restore", required=False, action="store_true", help="Restore the original MAC address")
    parser.add_argument("--status", required=False, action="store_true", help="Current MAC address status")

    return parser.parse_args()


def get_current_mac():
    '''Get the current MAC address of the system.'''

    return ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(0, 8*6, 8)][::-1])


def mac_address_status(interface):
    '''Displays the MAC address status of the specified network interface.'''

    if not os.path.isfile("/tmp/.original_mac"):
        original_mac = get_current_mac()
        print(f"\n{Fore.BLUE}Interface: {Style.RESET_ALL}{interface}")
        print(f"\n{Fore.BLUE}Original MAC Address:{Style.RESET_ALL}{original_mac}")
        
    else:
        with open("/tmp/.original_mac", "r") as file:
            original_mac = file.read().strip()
        current_mac = get_current_mac()

        if original_mac == current_mac:
            print(f"\n{Fore.BLUE}Interface:{Style.RESET_ALL} {interface}")
            print(f"\n{Fore.BLUE}Original MAC Address:{Style.RESET_ALL} {original_mac}")

        else:
            print(f"\n{Fore.BLUE}Interface:{Style.RESET_ALL} {interface}")
            print(f"\n{Fore.MAGENTA}Spoofed MAC Address:{Style.RESET_ALL} {current_mac}")
            print(f"{Fore.BLUE}Original MAC Address:{Style.RESET_ALL} {original_mac}")
        

def save_original_mac():
    '''Saves the original MAC address of the system to a temporary file.'''

    if not os.path.isfile("/tmp/.original_mac"):

        current_mac_address =  get_current_mac()
        with open("/tmp/.original_mac", "w") as file:

            file.write(current_mac_address)


def restore_original_mac():
    '''Restores the original MAC address from the saved temporary file.'''

    with open("/tmp/.original_mac", "r") as file:

        original_mac_address = file.read().strip()
        current_mac_address =  get_current_mac()
        
        if original_mac_address == current_mac_address:
            print(Fore.YELLOW + "\nThe MAC address is already the original one, no need to restore.")
            sys.exit(1)
        
        else:
            print(f"\n{Fore.BLUE}Restoring original MAC address")

    return original_mac_address
    

def random_oui():
    '''Generates a random Organizationally Unique Identifier (OUI) from a predefined list.'''

    random_number= random.randint(1, 19052)
    try:
        with open("ouis", "r") as file:
            for i, line in enumerate(file, start=1):

                if i == random_number:
                    parts = line.strip().split(" - ")
                    break
            return parts[0], parts[1]

    except FileNotFoundError:
        print(Fore.RED + "\nError: 'ouis' file not found. Please ensure it is in the same directory as the script.")
        sys.exit(1)
        


def random_nic():
    '''Generates a random Network Interface Controller (NIC) portion of a MAC address.'''

    hex_string = ""
    
    for i in range(3):

        par = ''.join(random.choice("0123456789abcdef") for _ in range(2))
        hex_string = hex_string + par + ":"
         
    hex_string = hex_string [:-1]

    return hex_string
   

def random_mac():
    '''Combines a random OUI and NIC to generate a complete random MAC address.'''

    data = random_oui()
    oui = data[0]
    vendor = data[1]
    nic = random_nic()
    mac = oui + ":" + nic
    print(f"\n{Fore.BLUE}Random MAC:{Style.RESET_ALL} {mac}")
    print(f"{Fore.BLUE}Vendor:{Style.RESET_ALL} {vendor}")

    return mac



def is_valid_mac(interface, mac_address):
    '''Validates the format of the provided network interface and MAC address.'''

    is_valid_interface = re.match(r'^[e][n|t][s|h]\d{1,2}$', interface)
    is_valid_mac_address = re.match(r'^([A-Fa-f0-9]{2}[:]){5}[A-Fa-f0-9]{02}$', mac_address)

    return is_valid_interface and is_valid_mac_address



def change_mac_address(interface, mac_address):
    '''Changes the MAC address of the specified network interface to the provided MAC address.'''

    if is_valid_mac(interface, mac_address):
        print(f"\n{Fore.BLUE}Changing MAC address of{Style.RESET_ALL} {interface} {Fore.BLUE}to{Style.RESET_ALL} {mac_address}")
        subprocess.run(["sudo", "ip", "link", "set", "dev", interface, "down"], check=True)
        subprocess.run(["sudo", "ip", "link", "set", "dev", interface, "address", mac_address], check=True)
        subprocess.run(["sudo", "ip", "link", "set", "dev", interface, "up"], check=True)
        print(Fore.GREEN + "\nMAC address changed successfully.")

    else:
        print(f"{Fore.RED}Invalid MAC address or interface format:{Style.RESET_ALL} {interface} {mac_address}")      
   

def main():
    '''Main function to handle the script's logic based on user-provided arguments.'''


    args = get_arguments()

    if not (args.mac_address or args.random or args.restore or args.status):
        print("\nInvalid arguments provided. Use --help for usage information.")
        sys.exit(1)

    save_original_mac()

    if args.mac_address:
        change_mac_address(args.interface, args.mac_address)

    elif args.random:
        random_mac_address = random_mac()
        change_mac_address(args.interface, random_mac_address)

    elif args.restore:
        original_mac_address = restore_original_mac()
        change_mac_address(args.interface, original_mac_address)

    elif args.status:
        mac_address_status(args.interface)


if __name__ == "__main__":
    main()