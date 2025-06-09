import sys
from Modules.TOOLS.Menu.osint_menu import osint_menu

sys.path.append('Modules/TOOLS/Menu/OSINT')

def web_analyzer_menu():
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
            return osint_menu()
        else:
            print('  Incorrect choice. Please try again.')
            input('Press Enter to continue...')
            web_scrap()
    except KeyboardInterrupt:
        print('\n')
        sys.exit()
