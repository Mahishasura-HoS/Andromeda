import subprocess  # To run external commands (like 'mig')
import os  # To interact with the file system (create directories, list files)
import sys  # To exit the script gracefully
import datetime  # To generate timestamps for output files
from colorama import Fore, Style, init  # For colorful terminal output

# Initialize Colorama for cross-platform colored output.
init(autoreset=True)

# --- Configuration Section ---
# This section defines key paths and settings for the script.
# Adjust MIG_PATH to match your MIG installation.
# -----------------------------------------------------------------------------

# Path to your MIG executable.
# If 'mig' is in your system's PATH, you can simply use "mig".
# Otherwise, provide the full absolute path to the MIG executable.
# Examples:
#   Windows: r"C:\path\to\your\mig.exe"
#   Linux/macOS: "/opt/mig/mig"
MIG_PATH = "mig"  # Assuming 'mig' is in your system's PATH

# Directory where output from MIG commands will be saved.
# Each command's output will be stored in a timestamped file within this directory.
OUTPUT_DIR = "mig_output"

# Ensure the output directory exists.
os.makedirs(OUTPUT_DIR, exist_ok=True)


# --- Core MIG Interaction Functions ---
# These functions abstract the execution of MIG commands and handle file operations.
# -----------------------------------------------------------------------------

def _execute_mig_command(command_args: list, save_output: bool = False) -> tuple[bool, str]:
    """
    Internal helper function to execute a specific MIG command.
    It constructs the command, runs it via subprocess, and captures output/errors.

    Args:
        command_args (list): A list of arguments for MIG (e.g., ['-p'] for processes).
        save_output (bool, optional): If True, the output will be saved to a file
                                      in the OUTPUT_DIR with a timestamp.
                                      If False, output is printed to console.

    Returns:
        tuple[bool, str]: (True, output_string) on success, (False, error_string) on failure.
    """
    # Start building the full command to execute.
    # The first element is always the path to the MIG executable.
    full_command = [MIG_PATH]
    full_command.extend(command_args)  # Add specific arguments for the command

    print(Fore.CYAN + f"\n[INFO] Executing MIG command: {' '.join(full_command)}" + Style.RESET_ALL)

    try:
        # subprocess.run is used for executing external commands.
        # capture_output=True: captures stdout and stderr.
        # text=True: decodes stdout/stderr as text (UTF-8 by default).
        # check=False: prevents subprocess from raising an exception for non-zero exit codes.
        #              We handle the return code manually for more granular control.
        result = subprocess.run(
            full_command,
            capture_output=True,
            text=True,
            check=False
        )

        # Check the exit code of the MIG command.
        if result.returncode == 0:
            # Command executed successfully.
            output_data = result.stdout
            if save_output:
                # Generate a unique filename with timestamp for the output.
                # Use a simplified name for the file based on the first argument or a general 'mig_output'
                command_name = command_args[0].replace('-', '_') if command_args else "general"
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                output_filename = os.path.join(OUTPUT_DIR, f"mig_{command_name}_{timestamp}.txt")

                with open(output_filename, 'w', encoding='utf-8') as f:
                    f.write(output_data)
                print(Fore.GREEN + f"[SUCCESS] Output saved to: {output_filename}" + Style.RESET_ALL)
            else:
                # Print output directly to the console.
                print(Fore.GREEN + "[SUCCESS] Command output:\n" + Style.RESET_ALL)
                print(output_data)
            return True, output_data
        else:
            # Command failed. Report stdout and stderr for debugging.
            error_message = (
                f"[ERROR] MIG command failed with exit code {result.returncode}.\n"
                f"Stdout: \n{result.stdout.strip()}\n"  # .strip() removes leading/trailing whitespace
                f"Stderr: \n{result.stderr.strip()}"
            )
            print(Fore.RED + error_message + Style.RESET_ALL)
            return False, error_message

    except FileNotFoundError:
        # This error occurs if MIG_PATH is incorrect or 'mig' isn't found.
        return False, f"[ERROR] MIG executable not found at '{MIG_PATH}'.\n" \
                      "Please ensure the path is correct or 'mig' is in your system's PATH."
    except Exception as e:
        # Catch any other unexpected errors during subprocess execution.
        return False, f"[ERROR] An unexpected error occurred during command execution: {e}"


# --- MIG Menu ---
# This is the entry point for MIG features.
# -----------------------------------------------------------------------------

def mig_menu():
    """
    Main menu for MIG automation.
    """
    while True:
        print(Fore.WHITE + '\n------------------------------------------------------------------------------')
        print(Fore.WHITE + '                                  MIG Tools                                    ')
        print(Fore.WHITE + '------------------------------------------------------------------------------')
        print(Fore.BLUE + '''
            [1] List Processes (mig -p)
            [2] List Network Connections (mig -n)
            [3] List Loaded Modules (mig -m)
            [4] Show System Information (mig -s)
            [C] Custom MIG Command

            [99] Back to Main Menu
        ''')
        print('\r')

        choice = input(
            Fore.RED + "mig" + Fore.LIGHTWHITE_EX + "@" + Fore.RED + "Andromeda" + Fore.RESET + "~$ ").upper()
        if choice != '99':
            # Determine if the output should be saved to a file or printed to console.
            save_output_choice = input(Fore.CYAN + "Save output to file? (Y/n): " + Style.RESET_ALL).lower()
            should_save_output = (save_output_choice == 'y' or save_output_choice == '')

            print('\r')  # Add a newline for cleaner output

        if choice == "1":
            _execute_mig_command(["-p"], should_save_output)
        elif choice == "2":
            _execute_mig_command(["-n"], should_save_output)
        elif choice == "3":
            _execute_mig_command(["-m"], should_save_output)
        elif choice == "4":
            _execute_mig_command(["-s"], should_save_output)
        elif choice == "C":
            custom_args_str = input(
                Fore.MAGENTA + "Enter custom MIG arguments (e.g., '-f /path/to/dump', '-a process_name'): " + Style.RESET_ALL).strip()
            custom_args = custom_args_str.split() if custom_args_str else []
            _execute_mig_command(custom_args, should_save_output)
        elif choice == "99":
            print(Fore.YELLOW + "Returning to Forensic menu." + Style.RESET_ALL)
            return  # Return to the calling function
        else:
            print(Fore.RED + "  Invalid choice. Please select a valid option." + Style.RESET_ALL)

        # Pause to allow user to read output before returning to the menu.
        #input(Fore.WHITE + '\nPress Enter to return to MIG menu...')


# --- Script Entry Point ---
# This block allows the script to be run directly for testing purposes.
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    # When this script is run directly, it will start the MIG menu.
    # To test:
    # 1. Ensure 'mig' is in your PATH or update MIG_PATH.
    # 2. Run: python mig_tools.py
    print(Fore.GREEN + "Starting MIG Tools..." + Style.RESET_ALL)
    mig_menu()
