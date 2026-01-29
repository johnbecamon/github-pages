# fake_datapulse_stresser.py
# Purely cosmetic fake stresser interface (NO real attacks!)
# Inspired by premium panels like Datapulse.one

import os
import time
import random
import sys
from colorama import init, Fore, Style
from datetime import datetime

init(autoreset=True)

# Colors
R = Fore.RED
G = Fore.GREEN
C = Fore.CYAN
Y = Fore.YELLOW
M = Fore.MAGENTA
B = Fore.BLUE
W = Fore.WHITE
RESET = Style.RESET_ALL

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    clear()
    header = f"""
{R}╔════════════════════════════════════════════════════════════╗
{R}║                                                            ║
{R}║  {C}██████╗ ██████╗ ███████╗███████╗ ██████╗ ██████╗ ██╗   ██╗ {R}║
{R}║  {C}██╔══██╗██╔══██╗██╔════╝██╔════╝██╔═══██╗██╔══██╗██║   ██║ {R}║
{R}║  {C}██║  ██║██████╔╝███████╗█████╗  ██║   ██║██████╔╝██║   ██║ {R}║
{R}║  {C}██║  ██║██╔═══╝ ╚════██║██╔══╝  ██║   ██║██╔══██╗╚██╗ ██╔╝ {R}║
{R}║  {C}██████╔╝██║     ███████║███████╗╚██████╔╝██║  ██║ ╚████╔╝  {R}║
{R}║  {C}╚═════╝ ╚═╝     ╚══════╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝  ╚═══╝   {R}║
{R}║                                                            ║
{R}║          {M}D A T A P U L S E   S T R E S S E R   v3.1      {R}║
{R}║         {Y}Premium DDoS Panel • Layer 4 & Layer 7          {R}║
{R}║         {W}Status: {G}ONLINE {Y}• {C}Expiration: 2025-12-31        {R}║
{R}╚════════════════════════════════════════════════════════════╝{RESET}
"""
    print(header)

def print_menu():
    print(f"\n{C}╔════════════════════════════════════════════════════╗")
    print(f"{C}║ {W}1. {G}UDP Flood {Y}(High PPS)                            {C}║")
    print(f"{C}║ {W}2. {G}TCP SYN Flood {Y}(Spoofed)                         {C}║")
    print(f"{C}║ {W}3. {G}HTTP GET Flood {Y}(Bypass)                         {C}║")
    print(f"{C}║ {W}4. {G}HTTP POST Flood {Y}(Form Bomb)                     {C}║")
    print(f"{C}║ {W}5. {G}Slowloris {Y}(Connection Exhaust)                  {C}║")
    print(f"{C}║ {W}6. {G}AMP Attack {Y}(NTP/SSDP/DNS)                       {C}║")
    print(f"{C}║ {W}7. {G}Check Target Status                                {C}║")
    print(f"{C}║ {W}8. {R}Exit                                               {C}║")
    print(f"{C}╚════════════════════════════════════════════════════╝{RESET}")

def fake_loading_bar(text="Loading", duration=2.0):
    bar_length = 35
    for i in range(bar_length + 1):
        percent = (i / bar_length) * 100
        bar = f"{C}█" * i + f"{W}░" * (bar_length - i)
        sys.stdout.write(f"\r{G}[+] {W}{text}: {bar} {percent:.0f}%")
        sys.stdout.flush()
        time.sleep(duration / bar_length)
    print(f"\r{G}[+] {W}{text} completed!{RESET} " + " " * 60)

def fake_attack(method):
    print(f"\n{Y}[?] {W}Enter target (IP or domain): {G}", end="")
    target = input().strip() or "example.com"
    
    print(f"{Y}[?] {W}Port (default 80/443): {G}", end="")
    port = input().strip() or "80"
    
    print(f"{Y}[?] {W}Threads (max 5000): {G}", end="")
    threads = input().strip() or "2500"
    
    print(f"{Y}[?] {W}Duration (seconds): {G}", end="")
    duration = input().strip() or "300"
    
    clear()
    print(f"""
{R}┌────────────────────────────── ATTACK STARTED ──────────────────────────────┐
{R}│                                                                            │
{R}│   {Y}Method:{W} {method:<25} {Y}Target:{W} {target}:{port}                       
{R}│   {Y}Threads:{W} {threads:<25} {Y}Duration:{W} {duration}s                         
{R}│   {Y}Sent:{W} {random.randint(1500000, 5000000):,} PPS    {Y}Power:{W} {random.randint(150, 350)} Gbps 
{R}│                                                                            │
{R}└────────────────────────────────────────────────────────────────────────────┘{RESET}
""")
    
    fake_loading_bar("Attack initialized", 1.5)
    
    print(f"\n{G}[+] {W}Attack in progress... Press Ctrl+C to stop (simulation){RESET}\n")
    
    try:
        for i in range(15):
            time.sleep(0.7)
            print(f"{random.choice([G, Y, C])}[•] Sent {random.randint(500000, 2000000):,} packets | "
                  f"Bypass: {random.choice(['ON', 'ON', 'Bypassing...'])}")
    except KeyboardInterrupt:
        print(f"\n{R}[!] Attack stopped by user.{RESET}")
    
    print(f"{G}[+] {W}Attack finished. Total packets: {random.randint(150000000, 999999999):,}{RESET}")

def main():
    while True:
        print_header()
        print_menu()
        
        choice = input(f"\n{C}[?] {W}Select method (1-8): {G}")
        
        if choice == '1':
            fake_attack("UDP Flood")
        elif choice == '2':
            fake_attack("TCP SYN Flood")
        elif choice == '3':
            fake_attack("HTTP GET Flood")
        elif choice == '4':
            fake_attack("HTTP POST Flood")
        elif choice == '5':
            fake_attack("Slowloris")
        elif choice == '6':
            fake_attack("AMP Attack")
        elif choice == '7':
            print(f"\n{Y}[+] Checking target status...{RESET}")
            fake_loading_bar("Scanning", 2.0)
            print(f"{G}[+] Target is {random.choice(['ONLINE', 'ONLINE', 'DOWN', 'PROTECTED'])}")
            input(f"\n{W}Press Enter to continue...")
        elif choice == '8':
            print(f"\n{Y}Thank you for using Datapulse Stresser. Goodbye!{RESET}")
            time.sleep(1.5)
            break
        else:
            print(f"{R}[!] Invalid option.{RESET}")
            time.sleep(1.5)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{R}[!] Exiting Datapulse Stresser...{RESET}")