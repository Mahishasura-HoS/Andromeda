import os  # To interact with the file system (list files, create directories)
import sys  # To exit the script gracefully
from colorama import Fore, Style, init  # For colorful terminal output
import requests
from Modules.MENU.osint_menu import osint_menu
sys.path.append('Modules/TOOLS/Menu/OSINT')

# Initialize Colorama for cross-platform colored output.
#init(autoreset=True)

def ip_lookup():
    exit()

def ip():
    ip = input('type ip here : ')
    api_ip_connect = f"http://ip-api.com/json/{ip}"
    content = requests.get(api_ip_connect)
    data = content.json()
    try:
        query = data['query']
    except KeyError:
        query = 'None'
    try:
        country = data['country']
    except KeyError:
        contry = 'None'
    try:
        countryCode = data['countryCode']
    except KeyError:
        countryCode = 'None'
    try:
        region = data['region']
    except KeyError:
        region = 'None'
    try:
        regionName = data['regionName']
    except KeyError:
        regionName = 'None'
    try:
        city = data['city']
    except KeyError:
        city = 'None'
    try:
        timezone = data['timezone']
    except KeyError:
        timezone = 'None'
    try:
        isp = data['isp']
    except KeyError:
        isp = 'None'
    try:
        org = data['org']
    except KeyError:
        org = 'None'
    try:
        ias = data['ias']
    except KeyError:
        ias = 'None'
    try:
        zip = data['zip']
    except KeyError:
        zip = 'None'
    print('\r')
    print('----------------------------------')
    print('ip 	    : ' + query)
    print('----------------------------------')
    print('country	    : ' + country)
    print('----------------------------------')
    print('contryCode  : ' + countryCode)
    print('----------------------------------')
    print('region      : ' + region)
    print('----------------------------------')
    print('region name : ' + regionName)
    print('----------------------------------')
    print('city        : ' + city)
    print('----------------------------------')
    print('zip         : ' + zip)
    print('----------------------------------')
    print('timezone    : ' + timezone)
    print('----------------------------------')
    print('isp         : ' + isp)
    print('----------------------------------')
    print('organisation: ' + org)
    print('----------------------------------')
    print('association : ' + ias)
    print('----------------------------------')
    print('\r')

def ip_menu():
        print(Fore.WHITE + '------------------------------------------------------------------------------')
        print(Fore.WHITE + '                               IP MENU                               ')
        print(Fore.WHITE + '------------------------------------------------------------------------------')
        print(Fore.BLUE + '''
        [1] Get IP Information
        [2] Lookup IP Address
        [3] IP Range Scan

        [99] Back to OSINT Menu
        ''')
        print('\r')
        try:
            choice = input(
                Fore.RED + "ip_info" + Fore.LIGHTWHITE_EX + "@" + Fore.RED + "Andromeda" + Fore.RESET + "~$ ")
            print('\r')
            if choice == "1":
                print(Fore.BLUE +"  Retrieving IP information...")
                ip()
            elif choice == "2":
                ip_addr = input(Fore.CYAN + "  Enter IP address to lookup: " + Style.RESET_ALL)
                print(f"  Looking up details for IP: {ip_addr}...")
                # Add IP lookup logic here
                input('Press Enter to continue...')
                ip()
            elif choice == "3":
                ip_range = input(Fore.CYAN + "  Enter IP range (e.g., 192.168.1.0/24): " + Style.RESET_ALL)
                print(f"  Scanning IP range: {ip_range}...")
                # Add IP range scan logic here
                input('Press Enter to continue...')
                ip()
            elif choice == "99":
                osint_menu()
            else:
                print('  Incorrect choice. Please try again.')
                input('Press Enter to continue...')
                ip_menu()
        except KeyboardInterrupt:
            print('\n')

if __name__ == "__main__":
    # When this script is run directly, it will start the CAINE guidance menu.
    # To test: python caine_guidance.py
    print(Fore.GREEN + "Starting Andromeda IP Menu..." + Style.RESET_ALL)
    ip_menu()
