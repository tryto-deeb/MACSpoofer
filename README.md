# MACSpoofer

It is a simple Python script that allows users to change the MAC address of a specified network interface. The script provides options to set a specific MAC address, generate a random MAC address, restore the original MAC address, or check the current MAC address status.

## Common Hacking Techniques Where It Is Used
This script is commonly used in the following hacking and security testing techniques:

- **Network Access Evasion:** Changing the MAC address to bypass network restrictions based on MAC filtering.
- **Anonymity in Public Networks:** Generating a random MAC address to hide the device's identity when connecting to public networks.
- **MAC Spoofing:** Imitating another device's MAC address to gain access to restricted networks or perform identity spoofing.

## Requirements
The script requires Python 3 and the `colorama` library to function properly.

## Installation Instructions

### If `colorama` is not installed:
Follow these steps to set up the environment and install the required dependencies:

1. **Create a virtual environment using `venv`:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. **Install `colorama` using `pip`:**
   ```bash
   pip install colorama
   ```

3. **Alternatively, install dependencies using the provided `requirements.txt`:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage
Run the script with the appropriate arguments to change, randomize, restore, or check the status of the MAC address. Use the `--help` flag to see detailed usage instructions.

### Examples:
1. **Change the MAC address of a network interface to a specific address:**
   ```bash
   python3 macspoofer.py -i <interface> -m 00:11:22:33:44:55
   ```

2. **Generate and set a random MAC address for a network interface:**
   ```bash
   python3 macspoofer.py -i <interface> --random
   ```

3. **Restore the original MAC address for a network interface:**
   ```bash
   python3 macspoofer.py -i <interface> --restore
   ```

4. **Check the current MAC address status of a network interface:**
   ```bash
   python3 macspoofer.py -i <interface> --status
   ```

## Notes
- The "ouis" file must be present in the same directory for random MAC generation.
- The original MAC address is temporarily stored in `/tmp/.original_mac` for restoration.
- The spoofed MAC address is temporary and will revert to the original MAC address after a system reboot.

   
   
  
   
