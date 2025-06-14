import sys
from colorama import Fore, Style, init

try:
    from Modules.TOOLS.Osint.email_osint_set import email_osint_menu
    from Modules.DATABASE.data_utils import save_data
    from Modules.TOOLS.Osint.ip_infos_set import ip_menu
    from Modules.TOOLS.Osint.metadata_set import metadata_menu
    from Modules.TOOLS.Osint.namesearch_set import namesearch_menu
    from Modules.TOOLS.Osint.phone_dir_set import phonedir_menu
    from Modules.TOOLS.Osint.web_analyzer_set import web_analyzer_menu

except ImportError as e:
    print(Fore.RED + f"[ERROR] Failed to import one or more osint tool modules: {e}" + Style.RESET_ALL)
    print(Fore.RED + "Please ensure all required tool scripts are in the correct directory." + Style.RESET_ALL)
    sys.exit(1) # Exit if essential modules can't be loaded

# Initialize Colorama for colorful terminal output.
# autoreset=True ensures that color styles are reset after each print statement.
init(autoreset=True)

# --- Main Forensic Analysis Menu Function ---
# This function serves as the central hub for all forensic tools.
# -----------------------------------------------------------------------------

def osint_menu():
    """
    Presents the main menu for various Osint tools within the
    Andromeda Framework.
    """
    while True:
        print(Fore.WHITE + '\n------------------------------------------------------------------------------')
        print(Fore.WHITE + '                      ANDROMEDA OSINT TOOLS                        ')
        print(Fore.WHITE + '------------------------------------------------------------------------------')
        print(Fore.BLUE + '''
    [1] Name Searching            [4] Email Searching  --OFF--
    [2] Phone Directory           [5] Web Analyzer     --OFF--
    [3] IP Information            [6] Meta-data Analyzer --OFF--     

    [90] Save 
    [99] Main menu      
        ''')
        print('\r')  # Add a newline for cleaner prompt appearance

        choice = input(Fore.RED + "Osint" + Fore.LIGHTWHITE_EX + "@" + Fore.RED + "Andromeda" + Fore.RESET + "~$ ")
        print('\r')  # Add a newline after user input

        if choice == "1":
            namesearch_menu()
        #elif choice == "2":
            #phonedir_menu()
        elif choice == "3":
            ip_menu()
        elif choice == "4":
            email_osint_menu()
        #elif choice == "5":
        #    web_analyzer_menu()
        elif choice == "6":
            metadata_menu()
        elif choice == "90":
           save_data()
        elif choice == "99":
            print(Fore.YELLOW + "Returning to  Andromeda Menu." + Style.RESET_ALL)
            return  # Exit this menu, returning to the calling function (e.g., andro_menu)
        else:
            print(Fore.RED + "  Invalid choice. Please select a valid option." + Style.RESET_ALL)


if __name__ == "__main__":
    # When this script is run directly, it will start the Forensic Analysis Menu.
    # Ensure all tool-specific scripts (mig_tools.py, volatility_analyzer.py, etc.)
    # are in the same directory and properly configured.
    print(Fore.GREEN + "Starting Andromeda Osint Module..." + Style.RESET_ALL)
    main_osint()