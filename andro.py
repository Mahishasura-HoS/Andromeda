from colorama import Fore, Style
import sys
sys.path.append('Modules/TOOLS')
sys.path.append('Modules/DATABASE')
import os
import sys
import json
from colorama import Fore, Style
import getpass
import time


# --- Configuration for User Data File and Session File ---
USER_DATA_FILE = 'Configuration files/users.json'  # Stores user credentials
SESSION_FILE = 'andromeda_session.json' # Stores login state (e.g., a simple flag)

# --- Global User Database (Loaded from/Saved to JSON) ---
USERS = {}
print(Fore.GREEN +'''Modules loaded successfully!''')
time.sleep(3)
print(Fore.RED +'''Please wait, Andromeda will launch !''')
time.sleep(2)

print(Fore.RED + '''
██╗    ██╗███████╗██╗      ██████╗ ██████╗ ███╗   ███╗███████╗
██║    ██║██╔════╝██║     ██╔════╝██╔═══██╗████╗ ████║██╔════╝
██║ █╗ ██║█████╗  ██║     ██║     ██║   ██║██╔████╔██║█████╗  
██║███╗██║██╔══╝  ██║     ██║     ██║   ██║██║╚██╔╝██║██╔══╝  
╚███╔███╔╝███████╗███████╗╚██████╗╚██████╔╝██║ ╚═╝ ██║███████╗
 ╚══╝╚══╝ ╚══════╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚══════╝ TO
''')

def load_users():
    """Loads user data from the JSON file."""
    global USERS
    if os.path.exists(USER_DATA_FILE):
        try:
            with open(USER_DATA_FILE, 'r') as f:
                USERS = json.load(f)
        except json.JSONDecodeError:
            print(Fore.RED + f"  Error decoding JSON from '{USER_DATA_FILE}'. Starting with empty users." + Style.RESET_ALL)
            USERS = {}
        except Exception as e:
            print(Fore.RED + f"  An unexpected error occurred loading '{USER_DATA_FILE}': {e}" + Style.RESET_ALL)
            USERS = {}
    else:
        print(Fore.YELLOW + f"  '{USER_DATA_FILE}' not found. A new file will be created on save." + Style.RESET_ALL)

def save_users():
    """Saves current user data to the JSON file."""
    try:
        with open(USER_DATA_FILE, 'w') as f:
            json.dump(USERS, f, indent=4)
        print(Fore.GREEN + f"  Successfully saved user data to '{USER_DATA_FILE}'." + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"  Error saving user data to '{USER_DATA_FILE}': {e}" + Style.RESET_ALL)

# --- Functions to Handle Session State ---
def save_session():
    """Creates the session file to indicate a logged-in state."""
    try:
        with open(SESSION_FILE, 'w') as f:
            f.write('logged_in') # A simple indicator
        print(Fore.GREEN + "  Session saved. Auto-login next time." + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"  Error saving session: {e}" + Style.RESET_ALL)

def clear_session():
    """Deletes the session file to clear the logged-in state."""
    if os.path.exists(SESSION_FILE):
        try:
            os.remove(SESSION_FILE)
            print(Fore.YELLOW + "  Session cleared. Will require login next time." + Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED + f"  Error clearing session: {e}" + Style.RESET_ALL)

def check_session():
    """Checks if a session file exists, indicating a previous login."""
    return os.path.exists(SESSION_FILE)
os.system('cls' if os.name == 'nt' else 'clear')
time.sleep(2)

def andro_menu():
    print(Fore.RED + "    _    _   _ ____  ____   ___  __  __ _____ ____    _    ")
    print(Fore.RED + "   / \\  | \\ | |  _ \\|  _ \\ / _ \\|  \\/  | ____|  _ \\  / \\   ")
    print(Fore.RED + "  / _ \\ |  \\| | | | | |_) | | | | |\\/| |  _| | | | |/ _ \\  ")
    print(Fore.BLUE + " / ___ \\| |\\  | |_| |  _ <| |_| | |  | | |___| |_| / ___ \\ ")
    print(Fore.BLUE + "/_/   \\_\\_| \\_|____/|_| \\_\\\\___/|_|  |_|_____|____/_/   \\_\\ Framework v0a" + Style.RESET_ALL)
    print(Fore.WHITE + '------------------------------------------------------------------------------')
    print(Fore.WHITE + '                                 MENU                                           ')
    print(Fore.WHITE + '------------------------------------------------------------------------------')
    print(Fore.BLUE + '''
       [1] Osint                     [5] Steganography           
       [2] Forensic                  [6] Misc
       [3] Cracking                  [7] Reverse 
       [4] Scripting                 [8] Web 
       
       [99] Save                     [00] Exit
       
        ''')
    print(Fore.WHITE)
    print('------------------------------------------------------------------------------')
    print(Fore.LIGHTBLACK_EX + '''                 Make by TheBloodredEagle - DRF ~ ''' + Fore.WHITE)
    print('------------------------------------------------------------------------------')
    try:
        choice = input(Fore.RED + f'{load_users()}' + Fore.LIGHTWHITE_EX + "@" + Fore.RED + "Andromeda" + Fore.RESET + "~$ ")
        print('\r')
        if choice == "1":
            menu_osint()
            input('enter to main menu ...')
            andro_menu()
        elif choice == "2":
            menu_forensic()
            input('enter to main menu ...')
            andro_menu()
        elif choice == "3":
            menu_cracking()
            input('enter to main menu')
            andro_menu()
        elif choice == "4":
            menu_scripting()
            input('enter to main menu')
            andro_menu()
        elif choice == "5":
            menu_stega()
            input('enter to main menu')
            andro_menu()
        elif choice == "6":
            menu_misc()
            input('enter to main menu')
            andro_menu()
        elif choice == "7":
            menu_reverse()
            input('enter to main menu')
            andro_menu()
        elif choice == "8":
            menu_web()
            input('enter to main menu')
            andro_menu()
        elif choice == "99":
            backup_database()
            input('  Press Enter to return to main menu...')
            andro_menu()  # Call andro_menu to redraw it after backup
        elif choice == "00":
            print(Fore.YELLOW +'Exit Andromeda')
        else:
            print('  incorrect choice ')
            print('\r')
            input('enter to main menu ...')
            andro_menu()
    except KeyboardInterrupt:
        print('\n')
        sys.exit()


## Menu settings
# OSINT menu

def menu_osint():
    print(Fore.WHITE + '------------------------------------------------------------------------------')
    print(Fore.WHITE + '                                    OSINT                                                ')
    print(Fore.WHITE + '------------------------------------------------------------------------------')
    print(Fore.BLUE + '''
    [1] Name Searching            [4] Email Searching  --OFF--
    [2] Phone Directory           [5] Web Analyzer     --OFF--
    [3] IP Information            [6] Meta-data Analyzer --OFF--     

    [90] Save 
    [99] Main menu      
     ''')
    print('\r')
    try:
        choice = input(Fore.RED + "osint" + Fore.LIGHTWHITE_EX + "@" + Fore.RED + "Andromeda" + Fore.RESET + "~$ ")
        print('\r')
        if choice == "1":
            name_search()
            input('enter to main menu ...')
            menu_osint()
        elif choice == "2":
            phone()
            input('enter to main menu ...')
            menu_osint()
        elif choice == "3":
            ip()
            input('enter to main menu')
            menu_osint()
        elif choice == "4":
            email_harper()
            input('enter to main menu')
            menu_osint()
        elif choice == "5":
            web_scrap()
            input('enter to main menu')
            menu_osint()
        elif choice == "6":
            meta_scan()
            input('enter to main menu')
        elif choice == "90":
            save_data()
            input('enter to main menu')
            menu_osint()
        elif choice == "99":
            return andro_menu()
        else:
            print('  incorrect choice ')
            print('\r')
            input('enter to main menu ...')
            andro_menu()
    except KeyboardInterrupt:
        print('\n')
        sys.exit()


# --- Name Searching Sub-Menu ---
def name_search():
    print(Fore.WHITE + '------------------------------------------------------------------------------')
    print(Fore.WHITE + '                              Name Searching                                 ')
    print(Fore.WHITE + '------------------------------------------------------------------------------')
    print(Fore.BLUE + '''
    [1] Search Public Records
    [2] Search Social Media
    [3] Search Professional Networks
    [4] Custom Name Search Query

    [99] Back to OSINT Menu
    ''')
    print('\r')
    try:
        choice = input(
            Fore.RED + "name_search" + Fore.LIGHTWHITE_EX + "@" + Fore.RED + "Andromeda" + Fore.RESET + "~$ ")
        print('\r')
        if choice == "1":
            print("  Performing Public Records Search...")
            # Add your public records search logic here
            input('Press Enter to continue...')
            name_search()
        elif choice == "2":
            print("  Performing Social Media Search...")
            # Add your social media search logic here
            input('Press Enter to continue...')
            name_search()
        elif choice == "3":
            print("  Performing Professional Networks Search...")
            # Add your professional networks search logic here
            input('Press Enter to continue...')
            name_search()
        elif choice == "4":
            query = input(Fore.CYAN + "  Enter custom name search query: " + Style.RESET_ALL)
            print(f"  Searching for: {query}...")
            # Add your custom name search logic here
            input('Press Enter to continue...')
            name_search()
        elif choice == "99":
            return menu_osint()
        else:
            print('  Incorrect choice. Please try again.')
            input('Press Enter to continue...')
            name_search()
    except KeyboardInterrupt:
        print('\n')
        sys.exit()


# --- Phone Directory Sub-Menu ---
def phone():
    print(Fore.WHITE + '------------------------------------------------------------------------------')
    print(Fore.WHITE + '                             Phone Directory                                 ')
    print(Fore.WHITE + '------------------------------------------------------------------------------')
    print(Fore.BLUE + '''
    [1] Reverse Phone Lookup
    [2] Phone Number Information (Carrier, Location)
    [3] Search for Phone Numbers by Name/Address

    [99] Back to OSINT Menu
    ''')
    print('\r')
    try:
        choice = input(Fore.RED + "phone_dir" + Fore.LIGHTWHITE_EX + "@" + Fore.RED + "Andromeda" + Fore.RESET + "~$ ")
        print('\r')
        if choice == "1":
            phone_num = input(Fore.CYAN + "  Enter phone number for reverse lookup: " + Style.RESET_ALL)
            print(f"  Performing reverse lookup for {phone_num}...")
            # Add your reverse phone lookup logic here
            input('Press Enter to continue...')
            phone()
        elif choice == "2":
            phone_num = input(Fore.CYAN + "  Enter phone number for information: " + Style.RESET_ALL)
            print(f"  Retrieving info for {phone_num}...")
            # Add your phone info logic here
            input('Press Enter to continue...')
            phone()
        elif choice == "3":
            name_addr = input(Fore.CYAN + "  Enter name/address to search for phone numbers: " + Style.RESET_ALL)
            print(f"  Searching for phone numbers related to {name_addr}...")
            # Add your phone number search by name/address logic here
            input('Press Enter to continue...')
            phone()
        elif choice == "99":
            return menu_osint()
        else:
            print('  Incorrect choice. Please try again.')
            input('Press Enter to continue...')
            phone()
    except KeyboardInterrupt:
        print('\n')
        sys.exit()


# --- IP Information Sub-Menu ---
def ip():
    print(Fore.WHITE + '------------------------------------------------------------------------------')
    print(Fore.WHITE + '                               IP Information                                ')
    print(Fore.WHITE + '------------------------------------------------------------------------------')
    print(Fore.BLUE + '''
    [1] Get My IP Information
    [2] Lookup IP Address Details
    [3] IP Range Scan

    [99] Back to OSINT Menu
    ''')
    print('\r')
    try:
        choice = input(Fore.RED + "ip_info" + Fore.LIGHTWHITE_EX + "@" + Fore.RED + "Andromeda" + Fore.RESET + "~$ ")
        print('\r')
        if choice == "1":
            print("  Retrieving your IP information...")
            # Add logic to get your own IP details
            input('Press Enter to continue...')
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
            return menu_osint()
        else:
            print('  Incorrect choice. Please try again.')
            input('Press Enter to continue...')
            ip()
    except KeyboardInterrupt:
        print('\n')
        sys.exit()


# --- Email Searching Sub-Menu ---
def email_harper():  # Renamed to avoid conflict if you have a general 'email' function
    print(Fore.WHITE + '------------------------------------------------------------------------------')
    print(Fore.WHITE + '                             Email Searching                                 ')
    print(Fore.WHITE + '------------------------------------------------------------------------------')
    print(
        Fore.YELLOW + '         Note: This feature is currently OFF/Under Development.             ' + Style.RESET_ALL)
    print(Fore.BLUE + '''
    [1] Search for Emails by Name/Domain (OFF)
    [2] Validate Email Address (OFF)
    [3] Breach Data Search by Email (OFF)

    [99] Back to OSINT Menu
    ''')
    print('\r')
    try:
        choice = input(
            Fore.RED + "email_search" + Fore.LIGHTWHITE_EX + "@" + Fore.RED + "Andromeda" + Fore.RESET + "~$ ")
        print('\r')
        if choice in ["1", "2", "3"]:
            print(Fore.YELLOW + "  This feature is currently OFF. Please wait for future updates." + Style.RESET_ALL)
            input('Press Enter to continue...')
            email_harper()
        elif choice == "99":
            return menu_osint()
        else:
            print('  Incorrect choice. Please try again.')
            input('Press Enter to continue...')
            email_harper()
    except KeyboardInterrupt:
        print('\n')
        sys.exit()


# --- Web Analyzer Sub-Menu ---
def web_scrap():
    print(Fore.WHITE + '------------------------------------------------------------------------------')
    print(Fore.WHITE + '                               Web Analyzer                                  ')
    print(Fore.WHITE + '------------------------------------------------------------------------------')
    print(
        Fore.YELLOW + '         Note: This feature is currently OFF/Under Development.             ' + Style.RESET_ALL)
    print(Fore.BLUE + '''
    [1] Website Information (Whois, Technologies) (OFF)
    [2] Web Scraper (Custom Rules) (OFF)
    [3] Broken Link Checker (OFF)

    [99] Back to OSINT Menu
    ''')
    print('\r')
    try:
        choice = input(
            Fore.RED + "web_analyzer" + Fore.LIGHTWHITE_EX + "@" + Fore.RED + "Andromeda" + Fore.RESET + "~$ ")
        print('\r')
        if choice in ["1", "2", "3"]:
            print(Fore.YELLOW + "  This feature is currently OFF. Please wait for future updates." + Style.RESET_ALL)
            input('Press Enter to continue...')
            web_scrap()
        elif choice == "99":
            return menu_osint()
        else:
            print('  Incorrect choice. Please try again.')
            input('Press Enter to continue...')
            web_scrap()
    except KeyboardInterrupt:
        print('\n')
        sys.exit()


# --- Meta-data Analyzer Sub-Menu ---
def meta_scan():
    print(Fore.WHITE + '------------------------------------------------------------------------------')
    print(Fore.WHITE + '                           Meta-data Analyzer                                ')
    print(Fore.WHITE + '------------------------------------------------------------------------------')
    print(
        Fore.YELLOW + '         Note: This feature is currently OFF/Under Development.             ' + Style.RESET_ALL)
    print(Fore.BLUE + '''
    [1] Analyze File Meta-data (EXIF, PDF, DOCX) (OFF)
    [2] Extract Meta-data from URL/Image (OFF)

    [99] Back to OSINT Menu
    ''')
    print('\r')
    try:
        choice = input(
            Fore.RED + "meta_analyzer" + Fore.LIGHTWHITE_EX + "@" + Fore.RED + "Andromeda" + Fore.RESET + "~$ ")
        print('\r')
        if choice in ["1", "2"]:
            print(Fore.YELLOW + "  This feature is currently OFF. Please wait for future updates." + Style.RESET_ALL)
            input('Press Enter to continue...')
            meta_scan()
        elif choice == "99":
            return menu_osint()
        else:
            print('  Incorrect choice. Please try again.')
            input('Press Enter to continue...')
            meta_scan()
    except KeyboardInterrupt:
        print('\n')
        sys.exit()


# Forensic menu settings

def menu_forensic():
    print(Fore.WHITE + '------------------------------------------------------------------------------')
    print(Fore.WHITE + '                                  FORENSIC                                                ')
    print(Fore.WHITE + '------------------------------------------------------------------------------')
    print(Fore.BLUE + '''
            [1] MIG                       [4] TSK (The Sleuth Kit)
            [2] GRR                       [5] Caine
            [3] Volatility                [6] Bulk Extractor


            [99] Main menu
     ''')
    print('\r')
    try:
        choice = input(Fore.RED + "forensic" + Fore.LIGHTWHITE_EX + "@" + Fore.RED + "Andromeda" + Fore.RESET + "~$ ")
        print('\r')
        if choice == "1":
            mig()
            input('enter to main menu ...')
            menu_forensic()
        elif choice == "2":
            grr()
            input('enter to main menu ...')
            menu_forensic()
        elif choice == "3":
            vol()
            input('enter to main menu')
            menu_forensic()
        elif choice == "99":
            return andro_menu()
        else:
            print('  incorrect choice ')
            print('\r')
            input('enter to main menu ...')
            andro_menu()
    except KeyboardInterrupt:
        print('\n')
        sys.exit()


# Crypto menu
def menu_cracking():
    while True:
        print(Fore.WHITE + '------------------------------------------------------------------------------')
        print(
            Fore.WHITE + '                                    Cracking                                               ')
        print(Fore.WHITE + '------------------------------------------------------------------------------')

        print(Fore.BLUE + '''
        [1] Password                  [4] System
        [2] Software                  [5] Web
        [3] Network                   [6] Cryptography

        [99] Main menu
         ''')

        print('\r')
        try:
            choice = input(
                Fore.RED + "cracking" + Fore.LIGHTWHITE_EX + "@" + Fore.RED + "Andromeda" + Fore.RESET + "~$ ")
            print('\r')
            if choice == "1":
                password_submenu()  # Call password cracking submenu
            elif choice == "2":
                software_submenu()  # Call software cracking submenu
            elif choice == "3":
                network_submenu()  # Call network cracking submenu
            elif choice == "4":
                system_submenu()
            elif choice == "5":
                web_submenu()
            elif choice == "6":
                crypto_submenu()
            elif choice == "99":
                return andro_menu()
            else:
                print(Fore.YELLOW + '  Incorrect choice. Please try again.' + Style.RESET_ALL)
                input('Press Enter to return to Cracking menu...')
        except KeyboardInterrupt:
            sys.exit()
        except ValueError:
            print(Fore.YELLOW + "Invalid input. Please enter a number." + Style.RESET_ALL)
            input('Press Enter to return to cracking menu...')


# Submenu definitions
def password_submenu():
    while True:
        print(Fore.BLUE + '''
        [1] Dictionary                [2] Brute force
        [3] Rainbow table           

        [99] Back
        ''')
        choice = input("Choice: ")
        if choice == "1":
            print("Dictionary cracking...")
        elif choice == "2":
            print("Brute force cracking...")
        elif choice == "3":
            print("Rainbow table cracking...")
        elif choice == "99":
            return menu_cracking()
        else:
            print("Invalid choice.")


def software_submenu():
    while True:
        print(Fore.BLUE + '''
        [1] Keygen                    [2] Patching
        [3] Reverse engineering       

        [99] Back
        ''')
        choice = input("Choice: ")
        if choice == "1":
            print("Key generation...")
        elif choice == "2":
            print("Patching...")
        elif choice == "3":
            print("Reverse engineering...")
        elif choice == "99":
            return menu_cracking()
        else:
            print("Invalid choice.")


def network_submenu():
    while True:
        print(Fore.BLUE + '''
        [1] Sniffing                  [2] Spoofing
        [3] DoS attack                

        [99] Back
        ''')
        choice = input("Choice: ")
        if choice == "1":
            print("Network sniffing...")
        elif choice == "2":
            print("Address spoofing...")
        elif choice == "3":
            print("Denial of service attack...")
        elif choice == "99":
            return menu_cracking()
        else:
            print("Invalid choice.")


def system_submenu():
    while True:
        print(Fore.BLUE + '''
        [1] Vuln exploit                 [2] Rooting
        [3] Privilege escalation      

        [99] Back
        ''')
        choice = input("Choice: ")
        if choice == "1":
            print("Vulnerability exploitation...")
        elif choice == "2":
            print("Rooting...")
        elif choice == "3":
            print("Privilege escalation...")
        elif choice == "99":
            return menu_cracking()
        else:
            print("Invalid choice.")


def web_submenu():
    while True:
        print(Fore.BLUE + '''
        [1] SQL Injection               [2] XSS
        [3] CSRF                        

        [99] Back
        ''')
        choice = input("Choice: ")
        if choice == "1":
            print("SQL injection...")
        elif choice == "2":
            print("XSS...")
        elif choice == "3":
            print("CSRF...")
        elif choice == "99":
            return menu_cracking()
        else:
            print("Invalid choice.")


def crypto_submenu():
    while True:
        print(Fore.BLUE + '''
        [1] Private key theft           [2] 51% attack
        [3] Phishing                  

        [99] Back
        ''')
        choice = input("Choice: ")
        if choice == "1":
            print("Private key theft...")
        elif choice == "2":
            print("51% attack...")
        elif choice == "3":
            print("Phishing...")
        elif choice == "99":
            return menu_cracking()
        else:
            print("Invalid choice.")


## Scripting menu settings
def menu_scripting():
    while True:
        print(Fore.WHITE + '------------------------------------------------------------------------------')
        print(Fore.WHITE + '                                   Scripting                                              ')
        print(Fore.WHITE + '------------------------------------------------------------------------------')
        print(Fore.BLUE + '''
        [1] System            [5] Security
        [2] Web               [6] Game
        [3] Network           [7] Data     
        [4] Automation        [8] Application

        [99] Main menu      
         ''')
        print('\r')
        try:
            choice = input(
                Fore.RED + "scripting" + Fore.LIGHTWHITE_EX + "@" + Fore.RED + "Andromeda" + Fore.RESET + "~$ ")
            print('\r')
            if choice == "1":
                system_scripting_submenu()
            elif choice == "2":
                web_scripting_submenu()
            elif choice == "3":
                network_scripting_submenu()
            elif choice == "4":
                automation_scripting_submenu()
            elif choice == "5":
                security_scripting_submenu()
            elif choice == "6":
                game_scripting_submenu()
            elif choice == "7":
                data_scripting_submenu()
            elif choice == "8":
                application_scripting_submenu()
            elif choice == "99":
                return andro_menu()
            else:
                print(Fore.YELLOW + '  Incorrect choice. Please try again.' + Style.RESET_ALL)
                input('Press Enter to return to scripting menu...')
        except KeyboardInterrupt:
            print('\nGoodbye!')
            sys.exit()
        except ValueError:
            print(Fore.YELLOW + "Invalid input. Please enter a number." + Style.RESET_ALL)
            input('Press Enter to return to scripting menu...')


def system_scripting_submenu():
    while True:
        print(Fore.BLUE + '''
        [1] File management         [2] Process control
        [3] System monitoring       

        [99] Back
        ''')
        choice = input("Choice: ")
        if choice == "1":
            print("File management scripting...")
        elif choice == "2":
            print("Process control scripting...")
        elif choice == "3":
            print("System monitoring scripting...")
        elif choice == "99":
            return menu_scripting()
        else:
            print("Invalid choice.")


def web_scripting_submenu():
    while True:
        print(Fore.BLUE + '''
        [1] Web scraping            [2] API interaction
        [3] Dynamic content gen.    

        [99] Back
        ''')
        choice = input("Choice: ")
        if choice == "1":
            print("Web scraping scripting...")
        elif choice == "2":
            print("API interaction scripting...")
        elif choice == "3":
            print("Dynamic content generation scripting...")
        elif choice == "99":
            return menu_scripting()
        else:
            print("Invalid choice.")


def network_scripting_submenu():
    while True:
        print(Fore.BLUE + '''
        [1] Network scanning        [2] Packet analysis
        [3] Socket programming      

        [99] Back
        ''')
        choice = input("Choice: ")
        if choice == "1":
            print("Network scanning scripting...")
        elif choice == "2":
            print("Packet analysis scripting...")
        elif choice == "3":
            print("Socket programming scripting...")
        elif choice == "99":
            return menu_scripting()
        else:
            print("Invalid choice.")


def automation_scripting_submenu():
    while True:
        print(Fore.BLUE + '''
        [1] Task scheduling         [2] UI automation
        [3] Data processing         

        [99] Back
        ''')
        choice = input("Choice: ")
        if choice == "1":
            print("Task scheduling scripting...")
        elif choice == "2":
            print("UI automation scripting...")
        elif choice == "3":
            print("Data processing automation scripting...")
        elif choice == "99":
            return menu_scripting()
        else:
            print("Invalid choice.")


def security_scripting_submenu():
    while True:
        print(Fore.BLUE + '''
        [1] Vulnerability scanning      [2] Log analysis
        [3] Intrusion detection     

        [99] Back
        ''')
        choice = input("Choice: ")
        if choice == "1":
            print("Vulnerability scanning scripting...")
        elif choice == "2":
            print("Log analysis scripting...")
        elif choice == "3":
            print("Intrusion detection scripting...")
        elif choice == "99":
            return menu_scripting()
        else:
            print("Invalid choice.")


def game_scripting_submenu():
    while True:
        print(Fore.BLUE + '''
        [1] Game logic              [2] Modding tools
        [3] AI behaviors           

        [99] Back
        ''')
        choice = input("Choice: ")
        if choice == "1":
            print("Game logic scripting...")
        elif choice == "2":
            print("Modding tools scripting...")
        elif choice == "3":
            print("AI behaviors scripting...")
        elif choice == "99":
            return menu_scripting()
        else:
            print("Invalid choice.")


def data_scripting_submenu():
    while True:
        print(Fore.BLUE + '''
        [1] Data parsing            [2] Data transformation
        [3] Data visualization      

        [99] Back
        ''')
        choice = input("Choice: ")
        if choice == "1":
            print("Data parsing scripting...")
        elif choice == "2":
            print("Data transformation scripting...")
        elif choice == "3":
            print("Data visualization scripting...")
        elif choice == "99":
            return menu_scripting()
        else:
            print("Invalid choice.")


def application_scripting_submenu():
    while True:
        print(Fore.BLUE + '''
        [1] Plugin development      [2] Macro creation
        [3] API usage             

        [99] Back
        ''')
        choice = input("Choice: ")
        if choice == "1":
            print("Plugin development scripting...")
        elif choice == "2":
            print("Macro creation scripting...")
        elif choice == "3":
            print("API usage scripting...")
        elif choice == "99":
            return menu_scripting()
        else:
            print("Invalid choice.")


## Steganography menu settings
## Stegano submenu settings
def menu_stega():
    while True:
        print(Fore.WHITE + '------------------------------------------------------------------------------')
        print(
            Fore.WHITE + '                                   Steganography                                             ')
        print(Fore.WHITE + '------------------------------------------------------------------------------')
        print(Fore.BLUE + '''
        [1] Images                    [4] Text
        [2] Audio                     [5] Network
        [3] Video                     [6] File System     

        [99] Main menu      
         ''')
        print('\r')
        try:
            choice = input(
                Fore.RED + "steganography" + Fore.LIGHTWHITE_EX + "@" + Fore.RED + "Andromeda" + Fore.RESET + "~$ ")
            print('\r')
            if choice == "1":
                image_stega_submenu()
            elif choice == "2":
                audio_stega_submenu()
            elif choice == "3":
                video_stega_submenu()
            elif choice == "4":
                text_stega_submenu()
            elif choice == "5":
                network_stega_submenu()
            elif choice == "6":
                filesystem_stega_submenu()
            elif choice == "99":
                return andro_menu()
            else:
                print(Fore.YELLOW + '  Incorrect choice. Please try again.' + Style.RESET_ALL)
                input('Press Enter to return to steganography menu...')
        except KeyboardInterrupt:
            print('\nGoodbye!')
            sys.exit()
        except ValueError:
            print(Fore.YELLOW + "Invalid input. Please enter a number." + Style.RESET_ALL)
            input('Press Enter to return to steganography menu...')


def image_stega_submenu():
    while True:
        print(Fore.BLUE + '''
        [1] LSB Embedding             [2] Pixel Manipulation
        [3] Frequency Domain          

        [99] Back
        ''')
        choice = input("Choice: ")
        if choice == "1":
            print("LSB embedding steganography...")
        elif choice == "2":
            print("Pixel manipulation steganography...")
        elif choice == "3":
            print("Frequency domain steganography...")
        elif choice == "99":
            return
        else:
            print("Invalid choice.")


def audio_stega_submenu():
    while True:
        print(Fore.BLUE + '''
        [1] LSB Embedding             [2] Echo Hiding
        [3] Phase Coding              

        [99] Back
        ''')
        choice = input("Choice: ")
        if choice == "1":
            print("LSB embedding audio steganography...")
        elif choice == "2":
            print("Echo hiding audio steganography...")
        elif choice == "3":
            print("Phase coding audio steganography...")
        elif choice == "99":
            return menu_stega()
        else:
            print("Invalid choice.")


def video_stega_submenu():
    while True:
        print(Fore.BLUE + '''
        [1] Frame Embedding           [2] Motion Vectors
        [3] DCT Techniques            

        [99] Back
        ''')
        choice = input("Choice: ")
        if choice == "1":
            print("Frame embedding video steganography...")
        elif choice == "2":
            print("Motion vectors video steganography...")
        elif choice == "3":
            print("DCT techniques video steganography...")
        elif choice == "99":
            return menu_stega()
        else:
            print("Invalid choice.")


def text_stega_submenu():
    while True:
        print(Fore.BLUE + '''
        [1] Line Shifting             [2] Word Shifting
        [3] Character Coding          

        [99] Back
        ''')
        choice = input("Choice: ")
        if choice == "1":
            print("Line shifting text steganography...")
        elif choice == "2":
            print("Word shifting text steganography...")
        elif choice == "3":
            print("Character coding text steganography...")
        elif choice == "99":
            return menu_stega()
        else:
            print("Invalid choice.")


def network_stega_submenu():
    while True:
        print(Fore.BLUE + '''
        [1] Protocol Fields           [2] Packet Timing
        [3] IP Header Stego           

        [99] Back
        ''')
        choice = input("Choice: ")
        if choice == "1":
            print("Protocol fields network steganography...")
        elif choice == "2":
            print("Packet timing network steganography...")
        elif choice == "3":
            print("IP header steganography...")
        elif choice == "99":
            return menu_stega()
        else:
            print("Invalid choice.")


def filesystem_stega_submenu():
    while True:
        print(Fore.BLUE + '''
        [1] Alternate Data Streams    [2] Hidden Partitions
        [3] File Slack Space          

        [99] Back
        ''')
        choice = input("Choice: ")
        if choice == "1":
            print("Alternate data streams filesystem steganography...")
        elif choice == "2":
            print("Hidden partitions filesystem steganography...")
        elif choice == "3":
            print("File slack space filesystem steganography...")
        elif choice == "99":
            return menu_stega()
        else:
            print("Invalid choice.")


## Misc menu settings

def menu_misc():
    while True:
        print(Fore.WHITE + '------------------------------------------------------------------------------')
        print(Fore.WHITE + '                                   Misc                                             ')
        print(Fore.WHITE + '------------------------------------------------------------------------------')
        print(Fore.BLUE + '''
        [1]  File manipulation                    [6]  Hardware interact 
        [2]  Data conversion                      [7]  Encoding / Decoding
        [3]  System utilities                     [8]  Randomization    
        [4]  Text processing                      [9]  Mathematics tools
        [5]  Web scraping                         [10] Automation tools    

        [99] Main menu      
         ''')
        print('\r')
        try:
            choice = input(Fore.RED + "misc" + Fore.LIGHTWHITE_EX + "@" + Fore.RED + "Andromeda" + Fore.RESET + "~$ ")
            print('\r')
            if choice == "1":
                file_manipulation_submenu()
            elif choice == "2":
                data_conversion_submenu()
            elif choice == "3":
                system_utilities_submenu()
            elif choice == "4":
                text_processing_submenu()
            elif choice == "5":
                web_scraping_submenu()
            elif choice == "6":
                hardware_interaction_submenu()
            elif choice == "7":
                encoding_decoding_submenu()
            elif choice == "8":
                randomization_submenu()
            elif choice == "9":
                math_tools_submenu()
            elif choice == "10":
                automation_tools_submenu()
            elif choice == "99":
                return andro_menu()
            else:
                print(Fore.YELLOW + '  Incorrect choice. Please try again.' + Style.RESET_ALL)
                input('Press Enter to return to misc menu...')
        except KeyboardInterrupt:
            print('\nGoodbye!')
            sys.exit()
        except ValueError:
            print(Fore.YELLOW + "Invalid input. Please enter a number." + Style.RESET_ALL)
            input('Press Enter to return to misc menu...')


def file_manipulation_submenu():
    while True:
        print(Fore.BLUE + '''
        [1] File renaming             [2] File copying
        [3] File deletion             

        [99] Back
        ''')
        choice = input("Choice: ")
        if choice == "1":
            print("File renaming...")
        elif choice == "2":
            print("File copying...")
        elif choice == "3":
            print("File deletion...")
        elif choice == "99":
            return menu_misc()
        else:
            print("Invalid choice.")


def data_conversion_submenu():
    while True:
        print(Fore.BLUE + '''
        [1] CSV to JSON                 [2] JSON to XML
        [3] Image format conversion   

        [99] Back
        ''')
        choice = input("Choice: ")
        if choice == "1":
            print("CSV to JSON conversion...")
        elif choice == "2":
            print("JSON to XML conversion...")
        elif choice == "3":
            print("Image format conversion...")
        elif choice == "99":
            return menu_misc()
        else:
            print("Invalid choice.")


def system_utilities_submenu():
    while True:
        print(Fore.BLUE + '''
        [1] Process monitoring        [2] Disk usage analysis
        [3] System info retrieval     

        [99] Back
        ''')
        choice = input("Choice: ")
        if choice == "1":
            print("Process monitoring...")
        elif choice == "2":
            print("Disk usage analysis...")
        elif choice == "3":
            print("System info retrieval...")
        elif choice == "99":
            return menu_misc()
        else:
            print("Invalid choice.")


def text_processing_submenu():
    while True:
        print(Fore.BLUE + '''
        [1] Text parsing              [2] Text formatting
        [3] Regular expressions       

        [99] Back
        ''')
        choice = input("Choice: ")
        if choice == "1":
            print("Text parsing...")
        elif choice == "2":
            print("Text formatting...")
        elif choice == "3":
            print("Regular expressions...")
        elif choice == "99":
            return menu_misc()
        else:
            print("Invalid choice.")


def web_scraping_submenu():
    while True:
        print(Fore.BLUE + '''
        [1] HTML parsing              [2] Data extraction
        [3] Web page crawling         

        [99] Back
        ''')
        choice = input("Choice: ")
        if choice == "1":
            print("HTML parsing...")
        elif choice == "2":
            print("Data extraction...")
        elif choice == "3":
            print("Web page crawling...")
        elif choice == "99":
            return menu_misc()
        else:
            print("Invalid choice.")


def hardware_interaction_submenu():
    while True:
        print(Fore.BLUE + '''
        [1] Serial communication      [2] GPIO control
        [3] USB device interaction    

        [99] Back
        ''')
        choice = input("Choice: ")
        if choice == "1":
            print("Serial communication...")
        elif choice == "2":
            print("GPIO control...")
        elif choice == "3":
            print("USB device interaction...")
        elif choice == "99":
            return menu_misc()
        else:
            print("Invalid choice.")


def encoding_decoding_submenu():
    while True:
        print(Fore.BLUE + '''
        [1] Base64 encoding           [2] URL encoding
        [3] Hexadecimal conversion    

        [99] Back
        ''')
        choice = input("Choice: ")
        if choice == "1":
            print("Base64 encoding...")
        elif choice == "2":
            print("URL encoding...")
        elif choice == "3":
            print("Hexadecimal conversion...")
        elif choice == "99":
            return menu_misc()
        else:
            print("Invalid choice.")


def randomization_submenu():
    while True:
        print(Fore.BLUE + '''
        [1] Random number generation    [2] Random string generation
        [3] Data shuffling            

        [99] Back
        ''')
        choice = input("Choice: ")
        if choice == "1":
            print("Random number generation...")
        elif choice == "2":
            print("Random string generation...")
        elif choice == "3":
            print("Data shuffling...")
        elif choice == "99":
            return menu_misc()
        else:
            print("Invalid choice.")


def math_tools_submenu():
    while True:
        print(Fore.BLUE + '''
        [1] Statistical calculations    [2] Mathematical functions
        [3] Matrix operations        

        [99] Back
        ''')
        choice = input("Choice: ")
        if choice == "1":
            print("Statistical calculations...")
        elif choice == "2":
            print("Mathematical functions...")
        elif choice == "3":
            print("Matrix operations...")
        elif choice == "99":
            return menu_misc()
        else:
            print("Invalid choice.")


def automation_tools_submenu():
    while True:
        print(Fore.BLUE + '''
        [1] Task scheduling           [2] Script automation
        [3] Workflow automation       

        [99] Back
        ''')
        choice = input("Choice: ")
        if choice == "1":
            print("Task scheduling...")
        elif choice == "2":
            print("Script automation...")
        elif choice == "3":
            print("Workflow automation...")
        elif choice == "99":
            return menu_misc()
        else:
            print("Invalid choice.")


## Reverse menu settings

def menu_reverse():
    while True:
        print(Fore.WHITE + '------------------------------------------------------------------------------')
        print(Fore.WHITE + '                                  Reverse                                            ')
        print(Fore.WHITE + '------------------------------------------------------------------------------')
        print(Fore.BLUE + '''
        [1] Software                  [5] Game
        [2] Hardware                  [6] Firmware
        [3] Network protocol          [7] Mobile application     
        [4] Malware                   [8] Web application


        [99] Main menu      
         ''')
        print('\r')
        try:
            choice = input(
                Fore.RED + "reverse" + Fore.LIGHTWHITE_EX + "@" + Fore.RED + "Andromeda" + Fore.RESET + "~$ ")
            print('\r')
            if choice == "1":
                software_reverse_submenu()
            elif choice == "2":
                hardware_reverse_submenu()
            elif choice == "3":
                network_protocol_reverse_submenu()
            elif choice == "4":
                malware_reverse_submenu()
            elif choice == "5":
                game_reverse_submenu()
            elif choice == "6":
                firmware_reverse_submenu()
            elif choice == "7":
                mobile_application_reverse_submenu()
            elif choice == "8":
                web_application_reverse_submenu()
            elif choice == "99":
                return andro_menu()
            else:
                print(Fore.YELLOW + '  Incorrect choice. Please try again.' + Style.RESET_ALL)
                input('Press Enter to return to reverse menu...')
        except KeyboardInterrupt:
            print('\nGoodbye!')
            sys.exit()
        except ValueError:
            print(Fore.YELLOW + "Invalid input. Please enter a number." + Style.RESET_ALL)
            input('Press Enter to return to reverse menu...')


def software_reverse_submenu():
    while True:
        print(Fore.BLUE + '''
        [1] Static analysis           [2] Dynamic analysis
        [3] Disassembly               [99] Back
        ''')
        choice = input("Choice: ")
        if choice == "1":
            print("Static software reverse engineering...")
        elif choice == "2":
            print("Dynamic software reverse engineering...")
        elif choice == "3":
            print("Software disassembly...")
        elif choice == "99":
            return menu_reverse()
        else:
            print("Invalid choice.")


def hardware_reverse_submenu():
    while True:
        print(Fore.BLUE + '''
        [1] Circuit analysis          [2] Bus analysis
        [3] Component analysis        [99] Back
        ''')
        choice = input("Choice: ")
        if choice == "1":
            print("Circuit analysis hardware reverse engineering...")
        elif choice == "2":
            print("Bus analysis hardware reverse engineering...")
        elif choice == "3":
            print("Component analysis hardware reverse engineering...")
        elif choice == "99":
            return menu_reverse()
        else:
            print("Invalid choice.")


def network_protocol_reverse_submenu():
    while True:
        print(Fore.BLUE + '''
        [1] Packet capture analysis   [2] Protocol dissection
        [3] State machine analysis    [99] Back
        ''')
        choice = input("Choice: ")
        if choice == "1":
            print("Packet capture analysis network protocol reverse engineering...")
        elif choice == "2":
            print("Protocol dissection network protocol reverse engineering...")
        elif choice == "3":
            print("State machine analysis network protocol reverse engineering...")
        elif choice == "99":
            return menu_reverse()
        else:
            print("Invalid choice.")


def malware_reverse_submenu():
    while True:
        print(Fore.BLUE + '''
        [1] Static malware analysis   [2] Dynamic malware analysis
        [3] Behavioral analysis       [99] Back
        ''')
        choice = input("Choice: ")
        if choice == "1":
            print("Static malware reverse engineering...")
        elif choice == "2":
            print("Dynamic malware reverse engineering...")
        elif choice == "3":
            print("Malware behavioral analysis...")
        elif choice == "99":
            return menu_reverse()
        else:
            print("Invalid choice.")


def game_reverse_submenu():
    while True:
        print(Fore.BLUE + '''
        [1] Game logic analysis       [2] Asset extraction
        [3] Game engine analysis      [99] Back
        ''')
        choice = input("Choice: ")
        if choice == "1":
            print("Game logic reverse engineering...")
        elif choice == "2":
            print("Game asset extraction...")
        elif choice == "3":
            print("Game engine reverse engineering...")
        elif choice == "99":
            return menu_reverse()
        else:
            print("Invalid choice.")


def firmware_reverse_submenu():
    while True:
        print(Fore.BLUE + '''
        [1] Firmware extraction       [2] Firmware analysis
        [3] ROM analysis              [99] Back
        ''')
        choice = input("Choice: ")
        if choice == "1":
            print("Firmware extraction...")
        elif choice == "2":
            print("Firmware analysis...")
        elif choice == "3":
            print("ROM analysis...")
        elif choice == "99":
            return menu_reverse()
        else:
            print("Invalid choice.")


def mobile_application_reverse_submenu():
    while True:
        print(Fore.BLUE + '''
        [1] APK/IPA analysis          [2] Dynamic analysis
        [3] Code decompilation        [99] Back
        ''')
        choice = input("Choice: ")
        if choice == "1":
            print("APK/IPA analysis mobile application reverse engineering...")
        elif choice == "2":
            print("Dynamic analysis mobile application reverse engineering...")
        elif choice == "3":
            print("Mobile application code decompilation...")
        elif choice == "99":
            return menu_reverse()
        else:
            print("Invalid choice.")


def web_application_reverse_submenu():
    while True:
        print(Fore.BLUE + '''
        [1] Client-side analysis      [2] Server-side analysis
        [3] API analysis              [99] Back
        ''')
        choice = input("Choice: ")
        if choice == "1":
            print("Client-side web application reverse engineering...")
        elif choice == "2":
            print("Server-side web application reverse engineering...")
        elif choice == "3":
            print("API web application reverse engineering...")
        elif choice == "99":
            return menu_reverse()
        else:
            print("Invalid choice.")


## Web menu settings

def menu_web():
    while True:
        print(Fore.WHITE + '------------------------------------------------------------------------------')
        print(Fore.WHITE + '                                   Web                                              ')
        print(Fore.WHITE + '------------------------------------------------------------------------------')
        print(Fore.BLUE + '''
        [1] Injection SQL                                [8] Directory traversal
        [2] Cross-Site Scripting (XSS)                   [9] Remote Code Execution (RCE)
        [3] Cross-Site Request Forgery (CSRF)            [10] Web Shells     
        [4] Authentication Attacks                       [11] Clickjacking
        [5] Session Hijacking                            [12] MitM Attacks
        [6] DoS/DDoS Attacks                             [13] Web Defacement
        [7] File Inclusion                               [14] Phishing

        [99] Main menu      
         ''')
        print('\r')
        try:
            choice = input(Fore.RED + "web" + Fore.LIGHTWHITE_EX + "@" + Fore.RED + "Andromeda" + Fore.RESET + "~$ ")
            print('\r')
            if choice == "1":
                sql_injection_submenu()
            elif choice == "2":
                xss_submenu()
            elif choice == "3":
                csrf_submenu()
            elif choice == "4":
                authentication_attacks_submenu()
            elif choice == "5":
                session_hijacking_submenu()
            elif choice == "6":
                dos_ddos_submenu()
            elif choice == "7":
                file_inclusion_submenu()
            elif choice == "8":
                directory_traversal_submenu()
            elif choice == "9":
                rce_submenu()
            elif choice == "10":
                web_shells_submenu()
            elif choice == "11":
                clickjacking_submenu()
            elif choice == "12":
                mitm_attacks_submenu()
            elif choice == "13":
                web_defacement_submenu()
            elif choice == "14":
                phishing_submenu()
            elif choice == "99":
                return andro_menu()
            else:
                print(Fore.YELLOW + '  Incorrect choice. Please try again.' + Style.RESET_ALL)
                input('Press Enter to return to web menu...')
        except KeyboardInterrupt:
            print('\nGoodbye!')
            sys.exit()
        except ValueError:
            print(Fore.YELLOW + "Invalid input. Please enter a number." + Style.RESET_ALL)
            input('Press Enter to return to web menu...')


def sql_injection_submenu():
    while True:
        print(Fore.BLUE + '''
        [1] Union-based SQLi         [2] Error-based SQLi
        [3] Blind SQLi               

        [99] Back
        ''')
        choice = input("Choice: ")
        if choice == "1":
            print("Union-based SQL injection...")
        elif choice == "2":
            print("Error-based SQL injection...")
        elif choice == "3":
            print("Blind SQL injection...")
        elif choice == "99":
            return menu_web()
        else:
            print("Invalid choice.")


def xss_submenu():
    while True:
        print(Fore.BLUE + '''
        [1] Reflected XSS              [2] Stored XSS
        [3] DOM-based XSS              

        [99] Back
        ''')
        choice = input("Choice: ")
        if choice == "1":
            print("Reflected XSS...")
        elif choice == "2":
            print("Stored XSS...")
        elif choice == "3":
            print("DOM-based XSS...")
        elif choice == "99":
            return menu_web()
        else:
            print("Invalid choice.")


def csrf_submenu():
    while True:
        print(Fore.BLUE + '''
        [1] GET-based CSRF             [2] POST-based CSRF
        [3] Cookie-based CSRF          

        [99] Back
        ''')
        choice = input("Choice: ")
        if choice == "1":
            print("GET-based CSRF...")
        elif choice == "2":
            print("POST-based CSRF...")
        elif choice == "3":
            print("Cookie-based CSRF...")
        elif choice == "99":
            return menu_web()
        else:
            print("Invalid choice.")


def authentication_attacks_submenu():
    while True:
        print(Fore.BLUE + '''
        [1] Brute-force attacks        [2] Dictionary attacks
        [3] Credential stuffing        

        [99] Back
        ''')
        choice = input("Choice: ")
        if choice == "1":
            print("Brute-force authentication attacks...")
        elif choice == "2":
            print("Dictionary authentication attacks...")
        elif choice == "3":
            print("Credential stuffing attacks...")
        elif choice == "99":
            return menu_web()
        else:
            print("Invalid choice.")


def session_hijacking_submenu():
    while True:
        print(Fore.BLUE + '''
        [1] Session fixation           [2] Session stealing
        [3] Cookie manipulation        

        [99] Back
        ''')
        choice = input("Choice: ")
        if choice == "1":
            print("Session fixation attacks...")
        elif choice == "2":
            print("Session stealing attacks...")
        elif choice == "3":
            print("Cookie manipulation attacks...")
        elif choice == "99":
            return menu_web()
        else:
            print("Invalid choice.")


def dos_ddos_submenu():
    while True:
        print(Fore.BLUE + '''
        [1] SYN flood attacks          [2] HTTP flood attacks
        [3] UDP flood attacks          

        [99] Back
        ''')
        choice = input("Choice: ")
        if choice == "1":
            print("SYN flood attacks...")
        elif choice == "2":
            print("HTTP flood attacks...")
        elif choice == "3":
            print("UDP flood attacks...")
        elif choice == "99":
            return menu_web()
        else:
            print("Invalid choice.")


def file_inclusion_submenu():
    while True:
        print(Fore.BLUE + '''
        [1] Local file inclusion (LFI)  [2] Remote file inclusion (RFI)

        [99] Back
        ''')
        choice = input("Choice: ")
        if choice == "1":
            print("Local file inclusion (LFI) attacks...")
        elif choice == "2":
            print("Remote file inclusion (RFI) attacks...")
        elif choice == "99":
            return menu_web()
        else:
            print("Invalid choice.")


def directory_traversal_submenu():
    while True:
        print(Fore.BLUE + '''
        [1] Relative path traversal    [2] Absolute path traversal

        [99] Back
        ''')
        choice = input("Choice: ")
        if choice == "1":
            print("Relative path traversal attacks...")
        elif choice == "2":
            print("Absolute path traversal attacks...")
        elif choice == "99":
            return menu_web()
        else:
            print("Invalid choice.")


def rce_submenu():
    while True:
        print(Fore.BLUE + '''
        [1] Command injection          [2] Code injection

        [99] Back
        ''')
        choice = input("Choice: ")
        if choice == "1":
            print("Command injection attacks...")
        elif choice == "2":
            print("Code injection attacks...")
        elif choice == "99":
            return menu_web()
        else:
            print("Invalid choice.")


def web_shells_submenu():
    while True:
        print(Fore.BLUE + '''
        [1] Uploading web shells        [2] Using web shells

        [99] Back
        ''')
        choice = input("Choice: ")
        if choice == "1":
            print("Uploading web shells...")
        elif choice == "2":
            print("Using web shells...")
        elif choice == "99":
            return menu_web()
        else:
            print("Invalid choice.")


def clickjacking_submenu():
    while True:
        print(Fore.BLUE + '''
        [1] Iframe clickjacking        [2] CSS clickjacking

        [99] Back
        ''')
        choice = input("Choice: ")
        if choice == "1":
            print("Iframe clickjacking attacks...")
        elif choice == "2":
            print("CSS clickjacking attacks...")
        elif choice == "99":
            return menu_web()
        else:
            print("Invalid choice.")


def mitm_attacks_submenu():
    while True:
        print(Fore.BLUE + '''
        [1] ARP poisoning              [2] DNS spoofing
        [3] SSL stripping             

        [99] Back
        ''')
        choice = input("Choice: ")
        if choice == "1":
            print("ARP poisoning attacks...")
        elif choice == "2":
            print("DNS spoofing attacks...")
        elif choice == "3":
            print("SSL stripping attacks...")
        elif choice == "99":
            return menu_web()
        else:
            print("Invalid choice.")


def web_defacement_submenu():
    while True:
        print(Fore.BLUE + '''
        [1] File replacement           [2] Database modification

        [99] Back
        ''')
        choice = input("Choice: ")
        if choice == "1":
            print("Web defacement file replacement...")
        elif choice == "2":
            print("Web defacement database modification...")
        elif choice == "99":
            return menu_web()
        else:
            print("Invalid choice.")


def phishing_submenu():
    while True:
        print(Fore.BLUE + '''
        [1] Email phishing             [2] Website phishing

        [99] Back
        ''')
        choice = input("Choice: ")
        if choice == "1":
            print("Email phishing attacks...")
        elif choice == "2":
            print("Website phishing attacks...")
        elif choice == "99":
            return menu_web()
        else:
            print("Invalid choice.")


# --- Sign-Up Menu ---
def signup_menu():
    print(Fore.WHITE + '------------------------------------------------------------------------------')
    print(Fore.WHITE + '                                  SIGN UP                                    ')
    print(Fore.WHITE + '------------------------------------------------------------------------------')
    print(Fore.BLUE + '''
    Create your new user account.

    [99] Back to Main Menu
    ''')
    print('\r')

    try:
        new_username = input(Fore.RED + "Set your new ID :")

        if new_username == "99":
            print(Fore.YELLOW + "Returning to Main Menu." + Style.RESET_ALL)
            return main_menu()

        if new_username in USERS:
            print(Fore.RED + "  Username already exists. Please choose a different one." + Style.RESET_ALL)
            input('  Press Enter to continue...')
            signup_menu()
            return

        new_password = getpass.getpass(Fore.RED + "New password :" )
        confirm_password = getpass.getpass(Fore.RED + "Confirm password :" )
        print('\r')

        if new_password == confirm_password:
            USERS[new_username] = new_password
            save_users() # <--- IMPORTANT: Save users after creating a new account
            print(Fore.GREEN + f"  Account for '{new_username}' created successfully!" + Style.RESET_ALL)
            input('  Press Enter to continue...')
            return main_menu()
        else:
            print(Fore.RED + "  Passwords do not match. Please try again." + Style.RESET_ALL)
            input('  Press Enter to continue...')
            signup_menu()

    except KeyboardInterrupt:
        print('\n' + Fore.YELLOW + "  Sign-up cancelled. Exiting." + Style.RESET_ALL)
        sys.exit()

# --- Login Menu ---
def login_menu():
    print(Fore.WHITE + '------------------------------------------------------------------------------')
    print(Fore.WHITE + '                                   LOGIN                                     ')
    print(Fore.WHITE + '------------------------------------------------------------------------------')
    print(Fore.YELLOW + '''
    Enter your credentials to log in.
    ''')
    print('\r')

    try:
        username = input(Fore.RED + "Your ID : ")

        password = getpass.getpass(Fore.RED + "Your password : " )
        print('\r')

        if username in USERS and USERS[username] == password:
            os.system('cls' if os.name == 'nt' else 'clear')
            time.sleep(2)
            print(Fore.YELLOW + f"Login successful! Welcome, SIR !" + Style.RESET_ALL)
            time.sleep(1)
            print(Fore.YELLOW + f"Set session {username}")
            time.sleep(1)
            print(Fore.GREEN + 'Session ready ' + Style.RESET_ALL)
            time.sleep(2)
            andro_menu()
        else:
            print(Fore.RED + "  Invalid username or password. Please try again." + Style.RESET_ALL)
            input('  Press Enter to continue...')
            login_menu()

    except KeyboardInterrupt:
        print('\n' + Fore.YELLOW + "  Login cancelled. Exiting." + Style.RESET_ALL)
        sys.exit()

# --- Main Application Start ---
def start_app():
    load_users() # <--- IMPORTANT: Load users when the app starts
    while True:
        print(Fore.WHITE + '------------------------------------------------------------------------------')
        print(Fore.WHITE + '                            ANDROMEDA AUTHENTICATION SYSTEM                             ')
        print(Fore.WHITE + '------------------------------------------------------------------------------')
        print(Fore.BLUE + '''
        [1] Sign Up 
        [2] Login 
        [3] Create Data Base

        [99] Exit Application
        ''')
        print('\r')
        try:

            choice = input(Fore.RED + "Andromeda" + Fore.LIGHTWHITE_EX + "@" + Fore.RED + "Authentication" + Fore.RESET + "~$ ")
            print('\r')

            if choice == "1":
                signup_menu()
            elif choice == "2":
                login_menu()
            elif choice == "3":
                db_management_menu()
            elif choice == "99":
                print(Fore.YELLOW + "Exiting Andromeda,  See you next time!" + Style.RESET_ALL)
                sys.exit()
            else:
                print(Fore.RED + "  Invalid choice. Please select 1, 2, or 99." + Style.RESET_ALL)
                input('  Press Enter to continue...')
        except KeyboardInterrupt:
            print('\n' + Fore.YELLOW + "  Application terminated." + Style.RESET_ALL)
if __name__ == "__main__":
    start_app()
andro_menu()