import sys
from colorama import *

from Modules.MENU.osint_menu import osint_menu


# Initialize Colorama for cross-platform colored output.
#init(autoreset=True)

def email_osint_menu():
    print(Fore.WHITE + '------------------------------------------------------------------------------')
    print(Fore.WHITE + '                             Email Searching Menu                                ')
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
            osint_menu()
        else:
            print('  Incorrect choice. Please try again.')
            input('Press Enter to continue...')
            email_harper()
    except KeyboardInterrupt:
        print('\n')
        sys.exit()

if __name__ == "__main__":
    # When this script is run directly, it will start the Forensic Analysis Menu.
    # Ensure all tool-specific scripts (mig_tools.py, volatility_analyzer.py, etc.)
    # are in the same directory and properly configured.
    print(Fore.GREEN + "Starting Andromeda Email Searching menu..." + Style.RESET_ALL)
    email_osint_menu()