import sys
from colorama import Fore, Style, init

from Modules.TOOLS.Forensic.email_set import email_menu

try:
    from Modules.DATABASE.data_utils import save_data
    from Modules.TOOLS.Forensic.mig_set import mig_menu
    from Modules.TOOLS.Forensic.volatility_set import volatility_menu
    from Modules.TOOLS.Forensic.blk_extract_set import bulk_extractor_menu
    from Modules.TOOLS.Forensic.caine_set import caine_menu
    from Modules.TOOLS.Forensic.tsk_set import tsk_main_menu


except ImportError as e:
    print(Fore.RED + f"[ERROR] Failed to import one or more forensic tool modules: {e}" + Style.RESET_ALL)
    print(Fore.RED + "Please ensure all required tool scripts are in the correct directory." + Style.RESET_ALL)
    sys.exit(1) # Exit if essential modules can't be loaded

# Initialize Colorama for colorful terminal output.
# autoreset=True ensures that color styles are reset after each print statement.
init(autoreset=True)


# --- Main Forensic Analysis Menu Function ---
# This function serves as the central hub for all forensic tools.
# -----------------------------------------------------------------------------

def forensic_analysis_menu():
    """
    Presents the main menu for various forensic analysis tools within the
    Andromeda Framework.
    """
    while True:
        print(Fore.WHITE + '\n------------------------------------------------------------------------------')
        print(Fore.WHITE + '                      ANDROMEDA FORENSIC TOOLS                        ')
        print(Fore.WHITE + '------------------------------------------------------------------------------')
        print(Fore.BLUE + '''
    [1] MIG                                         [5] The Sleuth Kit - TSK
    [2] Volatility 3                                [6] Email Harvester
    [3] Bulk Extractor                              [7] Remote Endpoint Response (GRR) -- OFF --
    [4] CAINE                                       
    
    [90] Save data
    [99] Andromeda Menu
        ''')
        print('\r') # Add a newline for cleaner prompt appearance

        choice = input(Fore.RED + "forensic" + Fore.LIGHTWHITE_EX + "@" + Fore.RED + "Andromeda" + Fore.RESET + "~$ ")
        print('\r') # Add a newline after user input

        if choice == "1":
            mig_menu()
        elif choice == "2":
            volatility_menu()
        elif choice == "3":
            bulk_extractor_menu()
        elif choice == "4":
            caine_menu()
        elif choice == "5":
            tsk_main_menu()
        elif choice == "6":
            email_menu()
        elif choice == "90":
            save_data()
        elif choice == "99":
            print(Fore.YELLOW + "Returning to Main Andromeda Menu." + Style.RESET_ALL)
            return # Exit this menu, returning to the calling function (e.g., andro_menu)
        else:
            print(Fore.RED + "  Invalid choice. Please select a valid option." + Style.RESET_ALL)

        # Pause to allow the user to read output before returning to the menu.
       # input(Fore.WHITE + '\nPress Enter to return to Forensic Analysis Menu...')

# --- Script Entry Point ---
# This block allows the script to be run directly for testing purposes.
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    # When this script is run directly, it will start the Forensic Analysis Menu.
    # Ensure all tool-specific scripts (mig_tools.py, volatility_analyzer.py, etc.)
    # are in the same directory and properly configured.
    print(Fore.GREEN + "Starting Andromeda Forensic Analysis Module..." + Style.RESET_ALL)
    forensic_analysis_menu()