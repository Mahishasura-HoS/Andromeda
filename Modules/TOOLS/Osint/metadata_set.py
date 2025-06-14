import sys  # To exit the script gracefully
from colorama import Fore, Style, init  # For colorful terminal output
from Modules.MENU.osint_menu import osint_menu
sys.path.append('Modules/TOOLS/Menu/OSINT')

# Initialize Colorama for cross-platform colored output.
#init(autoreset=True)

def metadata_menu():
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
                print(
                    Fore.YELLOW + "  This feature is currently OFF. Please wait for future updates." + Style.RESET_ALL)
                input('Press Enter to continue...')
                m()
            elif choice == "99":
                return osint_menu()
            else:
                print('  Incorrect choice. Please try again.')
                input('Press Enter to continue...')
                metadata_menu()
        except KeyboardInterrupt:
            print('\n')
            sys.exit()

if __name__ == "__main__":
    # When this script is run directly, it will start the Forensic Analysis Menu.
    # Ensure all tool-specific scripts (mig_tools.py, volatility_analyzer.py, etc.)
    # are in the same directory and properly configured.
    print(Fore.GREEN + "Starting Andromeda Meta-data menu..." + Style.RESET_ALL)
    metadata_menu()