import subprocess  # To run external Bulk Extractor commands
import os  # To interact with the file system (list files, create directories)
import sys  # To exit the script gracefully
import datetime  # To generate timestamps for output directories
from colorama import Fore, Style, init  # For colorful terminal output

# Initialize Colorama for cross-platform colored output.
init(autoreset=True)

# --- Configuration Section ---
# Define paths and settings for Bulk Extractor and data.
# -----------------------------------------------------------------------------

# Path to the Bulk Extractor executable.
# If 'bulk_extractor' is in your system's PATH, you can use "bulk_extractor" directly.
# Otherwise, provide the full absolute path.
# Examples:
#   Windows: r"C:\Program Files\bulk_extractor\bulk_extractor.exe"
#   Linux/macOS: "/usr/local/bin/bulk_extractor" or "bulk_extractor"
BULK_EXTRACTOR_PATH = "bulk_extractor"  # Assuming 'bulk_extractor' is in PATH

# Directory where your input files (disk images, files, or folders) are located.
# The script will automatically create this directory if it doesn't exist.
INPUT_DATA_DIR = "/Modules/Forensic/data/forensic_data_sources"

# Directory where Bulk Extractor's output reports will be saved.
# Each run will get its own timestamped subdirectory within this.
BULK_EXTRACTOR_OUTPUT_BASE_DIR = "/Modules/Forensic/data/bulk_extractor_reports"

# Ensure necessary directories exist.
os.makedirs(INPUT_DATA_DIR, exist_ok=True)
os.makedirs(BULK_EXTRACTOR_OUTPUT_BASE_DIR, exist_ok=True)


# --- Core Bulk Extractor Interaction Functions ---
# These functions handle the execution of Bulk Extractor commands.
# -----------------------------------------------------------------------------

def _execute_bulk_extractor_command(input_path: str, output_dir: str, command_args: list = None) -> tuple[bool, str]:
    """
    Internal helper function to execute Bulk Extractor.

    Args:
        input_path (str): Absolute path to the input file or directory for Bulk Extractor.
        output_dir (str): Absolute path to the output directory for this specific run.
        command_args (list, optional): A list of additional arguments for Bulk Extractor.

    Returns:
        tuple[bool, str]: (True, success_message) on success, (False, error_message) on failure.
    """
    if command_args is None:
        command_args = []

    # Basic command structure: bulk_extractor -o <output_dir> <input_path>
    full_command = [BULK_EXTRACTOR_PATH, "-o", output_dir, input_path]
    full_command.extend(command_args)  # Add any specific flags (e.g., -E email, -x all)

    print(Fore.CYAN + f"\n[INFO] Executing Bulk Extractor command:\n{' '.join(full_command)}" + Style.RESET_ALL)
    print(Fore.CYAN + f"[INFO] Output will be saved to: {output_dir}" + Style.RESET_ALL)

    try:
        # We don't capture_output here directly because Bulk Extractor is chatty
        # and its main output is files. We'll let it print to console and check return code.
        process = subprocess.Popen(full_command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

        # Print output in real-time to the console for user feedback
        for line in process.stdout:
            print(Fore.BLUE + line.strip() + Style.RESET_ALL)

        process.wait()  # Wait for the process to complete

        if process.returncode == 0:
            success_message = f"[SUCCESS] Bulk Extractor finished. Check '{output_dir}' for results."
            print(Fore.GREEN + success_message + Style.RESET_ALL)
            return True, success_message
        else:
            error_message = (
                f"[ERROR] Bulk Extractor failed with exit code {process.returncode}.\n"
                f"Check console output above for details."
            )
            print(Fore.RED + error_message + Style.RESET_ALL)
            return False, error_message

    except FileNotFoundError:
        return False, f"[ERROR] Bulk Extractor executable not found at '{BULK_EXTRACTOR_PATH}'.\n" \
                      "Please check BULK_EXTRACTOR_PATH in configuration or ensure it's in your system's PATH."
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


# --- Bulk Extractor Menu ---
# This is the main interface for Bulk Extractor features.
# -----------------------------------------------------------------------------

def bulk_extractor_menu():
    """
    Main menu for Bulk Extractor automation.
    Allows selection of an input data source and launches analysis options.
    """
    while True:
        print(Fore.WHITE + '\n------------------------------------------------------------------------------')
        print(Fore.WHITE + '                      Bulk Extractor Analysis Menu                            ')
        print(Fore.WHITE + '------------------------------------------------------------------------------')
        print(Fore.BLUE + '''
    [1] Select Input Data Source
    [2] List Available Features (bulk_extractor -L)

    [99] Back to Main Forensic Menu
        ''')
        print('\r')

        choice = input(
            Fore.RED + "bulk_extractor" + Fore.LIGHTWHITE_EX + "@" + Fore.RED + "Andromeda" + Fore.RESET + "~$ ")
        print('\r')

        if choice == "1":
            selected_input_path = _select_input_data_source()
            if selected_input_path:
                bulk_extractor_analysis_submenu(selected_input_path)
            else:
                print(Fore.YELLOW + "No data source selected. Returning to Bulk Extractor menu." + Style.RESET_ALL)
        elif choice == "2":
            # List all available features (scanners) in Bulk Extractor
            print(Fore.CYAN + "\n[INFO] Listing all available Bulk Extractor features (scanners)..." + Style.RESET_ALL)
            try:
                # Run bulk_extractor with the -L flag to list features.
                # No input path or output directory needed for this command.
                result = subprocess.run([BULK_EXTRACTOR_PATH, "-L"], capture_output=True, text=True, check=True)
                print(Fore.GREEN + result.stdout + Style.RESET_ALL)
            except FileNotFoundError:
                print(
                    Fore.RED + f"[ERROR] Bulk Extractor executable not found at '{BULK_EXTRACTOR_PATH}'. Cannot list features." + Style.RESET_ALL)
            except subprocess.CalledProcessError as e:
                print(Fore.RED + f"[ERROR] Failed to list features: {e.stderr}" + Style.RESET_ALL)
        elif choice == "99":
            print(Fore.YELLOW + "Returning to Main Forensic Menu." + Style.RESET_ALL)
            return  # Exits this menu, returning to the calling function (e.g., forensic_analysis_menu)
        else:
            print(Fore.RED + "  Invalid choice. Please select a valid option." + Style.RESET_ALL)

        input(Fore.WHITE + '\nPress Enter to return to Bulk Extractor menu...')


# --- Bulk Extractor Analysis Submenu ---
# This submenu appears after an input data source has been selected.
# -----------------------------------------------------------------------------

def bulk_extractor_analysis_submenu(input_path: str):
    """
    Presents a submenu with specific analysis options for the chosen input data source.

    Args:
        input_path (str): The absolute path to the input file or directory.
    """
    input_base_name = os.path.basename(input_path)

    while True:
        print(Fore.WHITE + '\n------------------------------------------------------------------------------')
        print(Fore.WHITE + f'                 Bulk Extractor Analysis for: {input_base_name} ')
        print(Fore.WHITE + '------------------------------------------------------------------------------')
        print(Fore.BLUE + '''
    [1] Run Default Scan (all enabled features)
    [2] Extract Emails Only (-E email)
    [3] Extract URLs Only (-E url)
    [4] Extract Credit Card Numbers Only (-E acct)
    [C] Run Custom Scan (specify features/flags)

    [99] Back to Bulk Extractor Main Menu
        ''')
        print('\r')

        choice = input(
            Fore.RED + "be_analyze" + Fore.LIGHTWHITE_EX + "@" + Fore.RED + "Andromeda" + Fore.RESET + "~$ ").upper()
        print('\r')

        # Generate a unique output directory for this run
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir_name = f"be_report_{os.path.basename(input_path).replace('.', '_')}_{timestamp}"
        current_output_path = os.path.join(BULK_EXTRACTOR_OUTPUT_BASE_DIR, output_dir_name)
        os.makedirs(current_output_path, exist_ok=True)  # Ensure output dir exists

        if choice == "1":  # Run Default Scan
            _execute_bulk_extractor_command(input_path, current_output_path)
        elif choice == "2":  # Extract Emails Only
            _execute_bulk_extractor_command(input_path, current_output_path, ["-E", "email"])
        elif choice == "3":  # Extract URLs Only
            _execute_bulk_extractor_command(input_path, current_output_path, ["-E", "url"])
        elif choice == "4":  # Extract Credit Card Numbers Only
            _execute_bulk_extractor_command(input_path, current_output_path, ["-E", "acct"])
        elif choice == "C":  # Run Custom Scan
            custom_features = input(
                Fore.MAGENTA + "Enter features to enable (e.g., 'email,url,phone') or disable (-x all): " + Style.RESET_ALL).strip()
            custom_flags = input(
                Fore.MAGENTA + "Enter any additional flags (e.g., '--resume', '--stop_on_error', leave empty): " + Style.RESET_ALL).strip()

            args = []
            if custom_features:
                # If the user provides "-x all", this will handle it. Otherwise, assume -E.
                if custom_features.startswith("-x"):
                    args.extend(custom_features.split())
                else:
                    args.extend(["-E", custom_features])
            if custom_flags:
                args.extend(custom_flags.split())

            _execute_bulk_extractor_command(input_path, current_output_path, args)
        elif choice == "99":
            print(Fore.YELLOW + "Returning to Bulk Extractor Main Menu." + Style.RESET_ALL)
            return  # Exit this submenu
        else:
            print(Fore.RED + "  Invalid choice. Please select a valid option." + Style.RESET_ALL)

        input(Fore.WHITE + '\nPress Enter to return to analysis submenu...')


# --- Script Entry Point ---
# This block allows the script to be run directly for testing purposes.
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    # To run this script directly for testing:
    # 1. Ensure Bulk Extractor is installed and in your system's PATH, or set BULK_EXTRACTOR_PATH.
    # 2. Place some forensic data (disk images, files, or folders) into the './forensic_data_sources' directory.
    # 3. Run: python bulk_extractor_analyzer.py
    print(Fore.GREEN + "Starting Bulk Extractor Automation Tool for Andromeda Framework..." + Style.RESET_ALL)
    bulk_extractor_menu()