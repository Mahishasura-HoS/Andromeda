import subprocess  # To run external Email Harvester commands
import os  # To interact with the file system (list files, create directories)
import sys  # To exit the script gracefully
import datetime  # To generate timestamps for output files
from colorama import Fore, Style, init  # For colorful terminal output
sys.path.append('Modules/TOOLS/Menu/OSINT')

# Initialize Colorama for cross-platform colored output.
init(autoreset=True)

# --- Configuration Section ---
# Define paths and settings for Email Harvester and data.
# -----------------------------------------------------------------------------

# Path to the Email Harvester executable.
# If 'emailharvester' is in your system's PATH, you can use "emailharvester" directly.
# Otherwise, provide the full absolute path.
# Examples:
#   Windows: r"C:\path\to\emailharvester.exe"
#   Linux/macOS: "/usr/local/bin/emailharvester" or "emailharvester"
EMAIL_HARVESTER_PATH = "emailharvester"  # Assuming 'emailharvester' is in PATH

# Directory where your input files (e.g., text files, logs, memory dumps) are located.
# The script will automatically create this directory if it doesn't exist.
INPUT_DATA_DIR = "/Modules/Forensic/data/email_harvester_inputs"

# Directory where extracted email addresses will be saved.
# Each run will have its own timestamped file in this directory.
OUTPUT_DIR = "/Modules/Forensic/data/email_harvester_outputs"

# Ensure necessary directories exist.
os.makedirs(INPUT_DATA_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)


# --- Core Email Harvester Interaction Functions ---
# These functions handle the execution of Email Harvester commands.
# -----------------------------------------------------------------------------

def _execute_email_harvester_command(input_path: str, output_filepath: str, command_args: list = None) -> tuple[
    bool, str]:
    """
    Internal helper function to execute Email Harvester.

    Args:
        input_path (str): Absolute path to the input file or directory for Email Harvester.
        output_filepath (str): Absolute path to the output file where emails will be saved.
        command_args (list, optional): A list of additional arguments for Email Harvester.

    Returns:
        tuple[bool, str]: (True, success_message) on success, (False, error_message) on failure.
    """
    if command_args is None:
        command_args = []

    # Typical command structure: emailharvester <input> -o <output> [options]
    # We will simulate a basic command, adjust if your tool has a different syntax.
    full_command = [EMAIL_HARVESTER_PATH, input_path]
    full_command.extend(command_args)  # Add specific options
    full_command.extend(["-o", output_filepath])  # Specify the output file

    print(Fore.CYAN + f"\n[INFO] Executing Email Harvester command:\n{' '.join(full_command)}" + Style.RESET_ALL)
    print(Fore.CYAN + f"[INFO] Emails will be saved to: {output_filepath}" + Style.RESET_ALL)

    try:
        # We capture output for display and logging.
        process = subprocess.run(
            full_command,
            capture_output=True,
            text=True,  # Decode stdout/stderr as text
            check=False  # Handle return code manually
        )

        if process.returncode == 0:
            success_message = f"[SUCCESS] Email Harvester finished. Check '{output_filepath}' for results."
            print(Fore.GREEN + success_message + Style.RESET_ALL)
            if process.stdout:
                print(Fore.BLUE + "Tool's standard output:\n" + process.stdout.strip() + Style.RESET_ALL)
            return True, success_message
        else:
            error_message = (
                f"[ERROR] Email Harvester failed with exit code {process.returncode}.\n"
                f"Standard Output:\n{process.stdout.strip()}\n"
                f"Standard Error:\n{process.stderr.strip()}"
            )
            print(Fore.RED + error_message + Style.RESET_ALL)
            return False, error_message

    except FileNotFoundError:
        return False, f"[ERROR] Email Harvester executable not found at '{EMAIL_HARVESTER_PATH}'.\n" \
                      "Please check EMAIL_HARVESTER_PATH in configuration or ensure it's in your system's PATH."
    except Exception as e:
        return False, f"[ERROR] An unexpected error occurred during command execution: {e}"


def _list_input_data_sources() -> list[str]:
    """
    Scans the INPUT_DATA_DIR and lists all available files/directories for analysis.

    Returns:
        list[str]: A list of filenames or directory names found.
    """
    print(Fore.BLUE + f"\n[INFO] Checking for input data sources in '{INPUT_DATA_DIR}':" + Style.RESET_ALL)
    sources = []
    for f in os.listdir(INPUT_DATA_DIR):
        full_path = os.path.join(INPUT_DATA_DIR, f)
        if os.path.isfile(full_path) or os.path.isdir(full_path):
            sources.append(f)

    if not sources:
        print(
            Fore.YELLOW + "  No input files or directories found. Please place your forensic data here." + Style.RESET_ALL)
    else:
        for i, source in enumerate(sorted(sources)):
            type_str = " (Dir)" if os.path.isdir(os.path.join(INPUT_DATA_DIR, source)) else " (File)"
            print(f"  [{i + 1}] {source}{type_str}")
    return sources


def _select_input_data_source() -> str | None:
    """
    Prompts the user to select an input data source from the available list.

    Returns:
        str | None: The absolute path of the selected data source, or None if cancelled.
    """
    sources = _list_input_data_sources()
    if not sources:
        return None

    while True:
        try:
            choice = input(
                Fore.MAGENTA + "Enter the number of the data source to analyze (or 0 to cancel): " + Style.RESET_ALL)
            choice_int = int(choice)

            if choice_int == 0:
                print(Fore.YELLOW + "Data source selection cancelled." + Style.RESET_ALL)
                return None
            if 1 <= choice_int <= len(sources):
                selected_source_filename = sorted(sources)[choice_int - 1]
                selected_source_path = os.path.join(INPUT_DATA_DIR, selected_source_filename)
                print(Fore.GREEN + f"Selected data source: {selected_source_path}" + Style.RESET_ALL)
                return selected_source_path
            else:
                print(
                    Fore.RED + "Invalid number. Please enter a number from the list or 0 to cancel." + Style.RESET_ALL)
        except ValueError:
            print(Fore.RED + "Invalid input. Please enter a numerical value." + Style.RESET_ALL)


# --- Email Harvester Menu ---
# This is the main interface for Email Harvester features.
# -----------------------------------------------------------------------------


def email_menu():
    """
       Main menu for Email Harvester automation.
       Allows selection of an input data source and launches analysis options.
       """
    while True:
        print(Fore.WHITE + '\n------------------------------------------------------------------------------')
        print(Fore.WHITE + '                      Email Harvester Analysis Menu                           ')
        print(Fore.WHITE + '------------------------------------------------------------------------------')
        print(Fore.BLUE + '''
       [1] Select Input Data Source and Extract Emails
       [C] Run Custom Email Harvester Command (for advanced users)

       [99] Forensic Menu
           ''')
        print('\r')

        choice = input(
            Fore.RED + "email_harvester" + Fore.LIGHTWHITE_EX + "@" + Fore.RED + "Andromeda" + Fore.RESET + "~$ ").upper()
        print('\r')

        if choice == "1":
            selected_input_path = _select_input_data_source()
            if selected_input_path:
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                output_filename = f"emails_{os.path.basename(selected_input_path).replace('.', '_')}_{timestamp}.txt"
                output_filepath = os.path.join(OUTPUT_DIR, output_filename)

                # For this example, we don't add default additional arguments.
                # You can add common arguments like recursion here.
                _execute_email_harvester_command(selected_input_path, output_filepath)
            else:
                print(Fore.YELLOW + "No data source selected. Returning to Email Harvester menu." + Style.RESET_ALL)
        elif choice == "C":  # Custom Command
            custom_input_path = input(
                Fore.MAGENTA + "Enter input file/directory path (absolute or relative): " + Style.RESET_ALL).strip()
            if not custom_input_path:
                print(Fore.RED + "Input path cannot be empty." + Style.RESET_ALL)
                continue

            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            custom_output_filename = input(
                Fore.MAGENTA + f"Enter output filename (e.g., 'custom_emails_{timestamp}.txt'): " + Style.RESET_ALL).strip()
            if not custom_output_filename:
                print(Fore.RED + "Output filename cannot be empty." + Style.RESET_ALL)
                continue

if __name__ == "__main__":
    # When this script is run directly, it will start the CAINE guidance menu.
    # To test: python caine_guidance.py
    print(Fore.GREEN + "Starting Andromeda email menu..." + Style.RESET_ALL)
    email_menu()