import subprocess  # To run external commands (like vol.py)
import os  # To interact with the file system (create directories, list files)
import sys  # To exit the script gracefully
import datetime  # To generate timestamps for output files
from colorama import Fore, Style, init  # For colorful terminal output

# Initialize Colorama for cross-platform colored output.
# autoreset=True ensures that color styles are reset after each print statement.
init(autoreset=True)

# --- Configuration Section ---
# This section defines key paths and settings for the script.
# Adjust VOLATILITY_PATH to match your Volatility 3 installation.
# -----------------------------------------------------------------------------

# Path to your Volatility 3 executable (vol.py).
# If 'vol.py' is in your system's PATH, you can simply use "vol.py".
# Otherwise, provide the full absolute path.
# Examples:
#   Windows: r"C:\Users\YourUser\volatility3\vol.py"
#   Linux/macOS: "/opt/volatility3/vol.py"
VOLATILITY_PATH = "vol.py"

# Directory where your memory dump files (.raw, .mem, .vmem, etc.) are stored.
# The script will automatically create this directory if it doesn't exist.
MEMORY_DUMPS_DIR = "memory_dumps"

# Directory where output from Volatility plugins will be saved.
# Each plugin's output will be stored in a timestamped file within this directory.
OUTPUT_DIR = "volatility_output"

# Ensure necessary directories exist.
# os.makedirs creates directories recursively if needed.
os.makedirs(MEMORY_DUMPS_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)


# --- Core Volatility Interaction Functions ---
# These functions abstract the execution of Volatility commands and handle file operations.
# -----------------------------------------------------------------------------

def _execute_volatility_command(command_args: list, memory_dump_path: str = None, save_output: bool = False) -> tuple[
    bool, str]:
    """
    Internal helper function to execute a Volatility 3 command.
    It constructs the command, runs it via subprocess, and captures output/errors.

    Args:
        command_args (list): A list of arguments for Volatility (e.g., ['windows.pslist.PsList']).
        memory_dump_path (str, optional): Absolute path to the memory dump file.
                                          Required for most analysis plugins.
        save_output (bool, optional): If True, the output will be saved to a file
                                      in the OUTPUT_DIR with a timestamp.
                                      If False, output is printed to console.

    Returns:
        tuple[bool, str]: (True, output_string) on success, (False, error_string) on failure.
    """
    # Start building the full command to execute.
    # The first element is always the path to the Volatility 3 executable.
    full_command = [VOLATILITY_PATH]

    # Add the memory dump file argument if provided.
    if memory_dump_path:
        if not os.path.exists(memory_dump_path):
            return False, f"Memory dump file not found: {memory_dump_path}"
        full_command.extend(['-f', memory_dump_path])

    # Append the specific Volatility plugin and its arguments.
    full_command.extend(command_args)

    print(Fore.CYAN + f"\n[INFO] Executing Volatility command: {' '.join(full_command)}" + Style.RESET_ALL)

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

        # Check the exit code of the Volatility command.
        if result.returncode == 0:
            # Command executed successfully.
            output_data = result.stdout
            if save_output:
                # Generate a unique filename with timestamp for the output.
                plugin_name = command_args[0].split('.')[-1]  # Extract plugin name for filename
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                output_filename = os.path.join(OUTPUT_DIR,
                                               f"{plugin_name}_{os.path.basename(memory_dump_path).split('.')[0]}_{timestamp}.txt")

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
                f"[ERROR] Volatility command failed with exit code {result.returncode}.\n"
                f"Stdout: \n{result.stdout.strip()}\n"  # .strip() removes leading/trailing whitespace
                f"Stderr: \n{result.stderr.strip()}"
            )
            print(Fore.RED + error_message + Style.RESET_ALL)
            return False, error_message

    except FileNotFoundError:
        # This error occurs if VOLATILITY_PATH is incorrect or vol.py isn't found.
        return False, f"[ERROR] Volatility executable not found at '{VOLATILITY_PATH}'.\n" \
                      "Please ensure the path is correct or 'vol.py' is in your system's PATH."
    except Exception as e:
        # Catch any other unexpected errors during subprocess execution.
        return False, f"[ERROR] An unexpected error occurred during command execution: {e}"


def _list_memory_dumps() -> list[str]:
    """
    Scans the MEMORY_DUMPS_DIR and lists all available memory dump files.

    Returns:
        list[str]: A list of filenames found in the MEMORY_DUMPS_DIR.
    """
    print(Fore.BLUE + f"\n[INFO] Checking for memory dumps in '{MEMORY_DUMPS_DIR}':" + Style.RESET_ALL)
    # os.listdir gets all entries; os.path.isfile filters for actual files.
    dumps = [f for f in os.listdir(MEMORY_DUMPS_DIR) if os.path.isfile(os.path.join(MEMORY_DUMPS_DIR, f))]

    if not dumps:
        print(
            Fore.YELLOW + "  No memory dump files found. Please place .raw, .mem, .vmem, etc. files here." + Style.RESET_ALL)
    else:
        for i, dump in enumerate(sorted(dumps)):  # Sorted for consistent display order
            print(f"  [{i + 1}] {dump}")
    return dumps


def _select_memory_dump() -> str | None:
    """
    Prompts the user to select a memory dump file from the available list.

    Returns:
        str | None: The absolute path of the selected memory dump, or None if cancelled.
    """
    dumps = _list_memory_dumps()
    if not dumps:
        # No dumps available, cannot select.
        return None

    while True:
        try:
            choice = input(
                Fore.MAGENTA + "Enter the number of the memory dump to analyze (or 0 to cancel): " + Style.RESET_ALL)
            choice_int = int(choice)

            if choice_int == 0:
                print(Fore.YELLOW + "Memory dump selection cancelled." + Style.RESET_ALL)
                return None
            if 1 <= choice_int <= len(dumps):
                # Return the absolute path to the selected dump.
                selected_dump_filename = sorted(dumps)[choice_int - 1]  # Ensure index matches sorted list
                selected_dump_path = os.path.join(MEMORY_DUMPS_DIR, selected_dump_filename)
                print(Fore.GREEN + f"Selected memory dump: {selected_dump_path}" + Style.RESET_ALL)
                return selected_dump_path
            else:
                print(
                    Fore.RED + "Invalid number. Please enter a number from the list or 0 to cancel." + Style.RESET_ALL)
        except ValueError:
            print(Fore.RED + "Invalid input. Please enter a numerical value." + Style.RESET_ALL)


# --- Volatility Submenu for Specific Analysis ---
# This menu appears after a memory dump has been selected.
# -----------------------------------------------------------------------------

def volatility_analysis_submenu(memory_dump_path: str):
    """
    Presents a submenu with specific Volatility analysis options for the chosen memory dump.

    Args:
        memory_dump_path (str): The absolute path to the memory dump file being analyzed.
    """
    # Display the current memory dump being analyzed in the submenu header.
    dump_base_name = os.path.basename(memory_dump_path)
    print(Fore.WHITE + '\n------------------------------------------------------------------------------')
    print(Fore.WHITE + f'                 Volatility Analysis for: {dump_base_name} ')
    print(Fore.WHITE + '------------------------------------------------------------------------------')
    print(Fore.BLUE + '''
    [1] List Processes (windows.pslist.PsList)
    [2] List Open Network Connections (windows.netscan.Netscan)
    [3] List Loaded DLLs (windows.dlllist.DllList)
    [4] Get Command History (windows.cmdline.CmdLine)
    [5] Scan for Malicious Code (windows.malfind.Malfind)
    [6] Show Loaded Kernel Modules (windows.modules.Modules)
    [7] List Registry Hives (windows.hivescan.HiveScan)
    [8] Extract Hashes (windows.hashdump.Hashdump)
    [9] Process Environment Variables (windows.envars.Envars)
    [10] List Mutexes (windows.mutantscan.MutantScan)

    [C] Custom Plugin Command
    [99] Back to Main Volatility Menu (select another dump)
        ''')
    print('\r')

    while True:
        choice = input(
            Fore.RED + "analyze" + Fore.LIGHTWHITE_EX + "@" + Fore.RED + "Volatility" + Fore.RESET + "~$ ").upper()

        # Determine if the output should be saved to a file or printed to console.
        # For simplicity, we'll ask the user for each command.
        # In a real app, you might have a global setting.
        save_output_choice = input(Fore.CYAN + "Save output to file? (Y/n): " + Style.RESET_ALL).lower()
        should_save_output = (save_output_choice == 'y' or save_output_choice == '')

        print('\r')  # Add a newline for cleaner output

        if choice == "1":
            _execute_volatility_command(['windows.pslist.PsList'], memory_dump_path, should_save_output)
        elif choice == "2":
            _execute_volatility_command(['windows.netscan.Netscan'], memory_dump_path, should_save_output)
        elif choice == "3":
            _execute_volatility_command(['windows.dlllist.DllList'], memory_dump_path, should_save_output)
        elif choice == "4":
            _execute_volatility_command(['windows.cmdline.CmdLine'], memory_dump_path, should_save_output)
        elif choice == "5":
            _execute_volatility_command(['windows.malfind.Malfind'], memory_dump_path, should_save_output)
        elif choice == "6":
            _execute_volatility_command(['windows.modules.Modules'], memory_dump_path, should_save_output)
        elif choice == "7":
            _execute_volatility_command(['windows.hivescan.HiveScan'], memory_dump_path, should_save_output)
        elif choice == "8":
            print(
                Fore.YELLOW + "[WARNING] Hashdump might require specific system information or elevated privileges. Be careful." + Style.RESET_ALL)
            _execute_volatility_command(['windows.hashdump.Hashdump'], memory_dump_path, should_save_output)
        elif choice == "9":
            _execute_volatility_command(['windows.envars.Envars'], memory_dump_path, should_save_output)
        elif choice == "10":
            _execute_volatility_command(['windows.mutantscan.MutantScan'], memory_dump_path, should_save_output)
        elif choice == "C":
            # Allow the user to enter any custom Volatility plugin and arguments.
            custom_plugin = input(
                Fore.MAGENTA + "Enter custom Volatility plugin (e.g., 'windows.dumpfiles.DumpFiles --pid 1234'): " + Style.RESET_ALL)
            custom_args_str = input(
                Fore.MAGENTA + "Enter any additional arguments for the plugin (e.g., '--dump-dir /path/to/save', leave empty if none): " + Style.RESET_ALL)

            # Split arguments only if the string is not empty to avoid creating [''] from an empty string.
            custom_args = custom_args_str.split() if custom_args_str else []

            full_custom_command = [custom_plugin] + custom_args
            _execute_volatility_command(full_custom_command, memory_dump_path, should_save_output)
        elif choice == "99":
            print(Fore.YELLOW + "Returning to memory dump selection." + Style.RESET_ALL)
            return  # Exit this submenu, returning to volatility_menu()
        else:
            print(Fore.RED + "  Invalid choice. Please select a valid option." + Style.RESET_ALL)

        # Prompt to continue after each command execution or invalid input.
        input(Fore.WHITE + '\nPress Enter to return to analysis submenu...')


# --- Main Volatility Menu ---
# This is the entry point for Volatility features, handling dump selection.
# -----------------------------------------------------------------------------

def volatility_menu():
    """
    Main menu for the Volatility 3 automation.
    Allows selection of a memory dump and launches the analysis submenu.
    """
    while True:
        print(Fore.WHITE + '\n------------------------------------------------------------------------------')
        print(Fore.WHITE + '                         Volatility 3 Automation Menu                         ')
        print(Fore.WHITE + '------------------------------------------------------------------------------')
        print(Fore.BLUE + '''
    [1] Select Memory Dump for Analysis
    [2] List all available Volatility plugins (vol.py -h output)

    [99] Back to Main Andromeda Menu
        ''')
        print('\r')

        choice = input(Fore.RED + "volatility" + Fore.LIGHTWHITE_EX + "@" + Fore.RED + "Andromeda" + Fore.RESET + "~$ ")
        print('\r')

        if choice == "1":
            selected_dump_path = _select_memory_dump()
            if selected_dump_path:
                # If a memory dump is successfully selected, enter the detailed analysis submenu.
                volatility_analysis_submenu(selected_dump_path)
            else:
                print(Fore.YELLOW + "No memory dump selected. Returning to Volatility main menu." + Style.RESET_ALL)
        elif choice == "2":
            # This option doesn't require a memory dump file.
            _execute_volatility_command(['-h'])
        elif choice == "99":
            print(Fore.YELLOW + "Returning to Main Andromeda Menu." + Style.RESET_ALL)
            return  # Exits this menu, returning to the calling function (e.g., andro_menu)
        else:
            print(Fore.RED + "  Invalid choice. Please select a valid option." + Style.RESET_ALL)

        # Pause to allow user to read output before returning to the menu.
        input(Fore.WHITE + '\nPress Enter to return to Volatility menu...')


# --- Script Entry Point ---
# This block allows the script to be run directly for testing purposes.
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    # When this script is run directly, it will start the Volatility menu.
    # To test:
    # 1. Ensure 'vol.py' is in your PATH or update VOLATILITY_PATH.
    # 2. Place some memory dump files (e.g., .raw, .mem) into the './memory_dumps' directory.
    # 3. Run: python volatility_analyzer.py
    print(Fore.GREEN + "Starting Volatility Analyzer for Andromeda Framework..." + Style.RESET_ALL)
    volatility_menu()