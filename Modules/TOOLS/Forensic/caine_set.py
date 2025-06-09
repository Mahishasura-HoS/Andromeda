import sys
from colorama import Fore, Style, init

# Initialize Colorama for cross-platform colored output.
init(autoreset=True)

# --- CAINE Guidance Functions ---
# These functions provide information and instructions about the CAINE distribution.
# -----------------------------------------------------------------------------

def display_caine_info():
    """
    Displays general information about CAINE (Computer Aided Investigative Environment).
    """
    print(Fore.CYAN + "\n[INFO] Understanding CAINE (Computer Aided Investigative Environment)" + Style.RESET_ALL)
    print(Fore.WHITE + "------------------------------------------------------------------------------")
    print(Fore.LIGHTBLUE_EX + """
CAINE is a complete Linux distribution (a Live CD/DVD/USB) created for digital forensics.
It offers a user-friendly graphical interface and a comprehensive set of tools
for forensic analysis, incident response, and data recovery.

Key aspects of CAINE:
    -   Live Environment: Boots from removable media without affecting the suspect system.
    -   Forensic Tools: Includes a wide array of pre-installed tools (e.g., Autopsy, Wireshark, Volatility, GRR client, etc.).
    -   Write Blocker: By default, CAINE mounts all discovered devices in read-only mode to prevent accidental data modification.
    -   User-Friendly: Designed to simplify common forensic tasks.

When to use CAINE:
    -   To acquire images from suspect drives.
    -   To perform live forensics on a running system (with caution).
    -   To analyze acquired disk images using its bundled tools.
    -   As a portable forensic workstation.
""" + Style.RESET_ALL)
    print(Fore.WHITE + "------------------------------------------------------------------------------")


def display_caine_integration_guidance():
    """
    Provides guidance on how to integrate CAINE into a forensic workflow
    when using a Python-based framework.
    """
    print(Fore.CYAN + "\n[INFO] Integrating CAINE into Your Forensic Workflow" + Style.RESET_ALL)
    print(Fore.WHITE + "------------------------------------------------------------------------------")
    print(Fore.LIGHTBLUE_EX + """
Since CAINE is an operating system, you cannot directly 'run' it from this Python script
like a command-line tool or an API. Integration involves using CAINE as a separate,
complementary environment in your forensic process.

Here's how CAINE typically fits in and how your Python framework can complement it:

1.  Booting with CAINE:
    -   **Primary Use:** Use CAINE to boot a suspect machine or a forensic workstation.
    -   **Purpose:** To safely acquire disk images (e.g., with Guymager) without modifying the original evidence.
    -   **Action:** This is done *outside* of your Python framework's execution.

2.  Transferring Evidence:
    -   Once images are acquired using CAINE, you'd transfer them to your analysis machine
        (where your Python framework is running).
    -   **Example:** Copy .raw, .E01, or .dd files from the CAINE environment to your host's
        './memory_dumps' or './disk_images' directories.

3.  Analysis with Your Python Framework:
    -   After acquisition and transfer, your Python framework can then process these images.
    -   **Example:**
        -   Use the **Volatility 3 script** we created to analyze memory dumps (if collected).
        -   Use other Python-based tools or scripts you develop for disk image parsing,
            file carving, log analysis, etc.

4.  Leveraging CAINE's Bundled Tools (Manual):
    -   Many powerful tools are pre-installed in CAINE (e.g., Autopsy, Wireshark, The Sleuth Kit).
    -   You can manually launch and use these tools within the CAINE graphical environment
        for deeper analysis that might not be automated by your Python scripts.

In summary, CAINE is your initial acquisition and safe environment, while your Python framework
serves as your automated analysis and reporting engine on the collected evidence.
""" + Style.RESET_ALL)
    print(Fore.WHITE + "------------------------------------------------------------------------------")

# --- Main CAINE Menu ---
# This menu provides the user with options to learn about CAINE.
# -----------------------------------------------------------------------------

def caine_menu():
    """
    Main menu for CAINE guidance within the Andromeda Framework.
    """
    while True:
        print(Fore.WHITE + '\n------------------------------------------------------------------------------')
        print(Fore.WHITE + '                            CAINE Guidance Menu                               ')
        print(Fore.WHITE + '------------------------------------------------------------------------------')
        print(Fore.BLUE + '''
    [1] What is CAINE?
    [2] How to Integrate CAINE into My Forensic Workflow?

    [99] Back to Main Andromeda Menu
        ''')
        print('\r')

        choice = input(Fore.RED + "caine" + Fore.LIGHTWHITE_EX + "@" + Fore.RED + "Andromeda" + Fore.RESET + "~$ ")
        print('\r')

        if choice == "1":
            display_caine_info()
        elif choice == "2":
            display_caine_integration_guidance()
        elif choice == "99":
            print(Fore.YELLOW + "Returning to Main Andromeda Menu." + Style.RESET_ALL)
            return # Exit this menu, returning to the calling function (e.g., andro_menu)
        else:
            print(Fore.RED + "  Invalid choice. Please select a valid option." + Style.RESET_ALL)

        input(Fore.WHITE + '\nPress Enter to return to CAINE Guidance menu...')

# --- Script Entry Point ---
# This block allows the script to be run directly for testing purposes.
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    # When this script is run directly, it will start the CAINE guidance menu.
    # To test: python caine_guidance.py
    print(Fore.GREEN + "Starting CAINE Guidance for Andromeda Framework..." + Style.RESET_ALL)
    caine_menu()