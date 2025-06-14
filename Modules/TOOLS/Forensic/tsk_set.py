import subprocess  # To run external TSK commands
import os  # To interact with the file system (list files, create directories)
import sys  # To exit the script gracefully
import datetime  # To generate timestamps for output files
from colorama import Fore, Style, init  # For colorful terminal output

# Initialize Colorama for cross-platform colored output.
init(autoreset=True)

# --- Configuration Section ---
# Define paths and settings for TSK tools and data.
# -----------------------------------------------------------------------------

# Path to the directory where TSK tools are located, or ensure they are in your system's PATH.
# If TSK tools (mmls, fsstat, fls, etc.) are in your system's PATH, you can use "mmls", "fsstat", etc. directly.
# Otherwise, provide the full path to the tools, e.g., "/usr/local/bin/tsk_tools/" or "C:\\Program Files\\SleuthKit\\bin\\"
# For simplicity, we'll assume they are in PATH or can be called directly.
TSK_TOOL_PREFIX = ""  # Leave empty if tools are in PATH, otherwise set to the path to the directory containing TSK executables

# Directory where your disk image files (.dd, .e01, .raw, etc.) are stored.
# The script will automatically create this directory if it doesn't exist.
DISK_IMAGES_DIR = "/Modules/Forensic/data/disk_images"

# Directory where output from TSK commands will be saved.
# Each command's output will be stored in a timestamped file within this directory.
OUTPUT_DIR = "/Modules/Forensic/data/tsk_output"

# Ensure necessary directories exist.
os.makedirs(DISK_IMAGES_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)


# --- Core TSK Interaction Functions ---
# These functions handle the execution of TSK commands and file operations.
# -----------------------------------------------------------------------------

def _execute_tsk_command(tool_name: str, command_args: list, image_path: str = None, save_output: bool = False,
                         raw_output_path: str = None) -> tuple[bool, str]:
    """
    Internal helper function to execute a specific TSK tool.

    Args:
        tool_name (str): The name of the TSK tool (e.g., "mmls", "fsstat", "fls").
        command_args (list): A list of arguments for the TSK tool.
        image_path (str, optional): Absolute path to the disk image file. Required for most tools.
        save_output (bool, optional): If True, stdout is saved to a timestamped file in OUTPUT_DIR.
        raw_output_path (str, optional): If provided, stdout is written directly to this file path
                                         without timestamping (useful for raw data like img_cat).

    Returns:
        tuple[bool, str]: (True, output_string) on success, (False, error_string) on failure.
    """
    # Prepend TSK_TOOL_PREFIX if it's set, otherwise just use the tool name.
    full_tool_path = os.path.join(TSK_TOOL_PREFIX, tool_name) if TSK_TOOL_PREFIX else tool_name

    full_command = [full_tool_path]

    if image_path:
        if not os.path.exists(image_path):
            return False, f"Disk image file not found: {image_path}"
        full_command.append(image_path)  # TSK tools typically take image path as first arg

    full_command.extend(command_args)  # Add specific arguments for the tool

    print(Fore.CYAN + f"\n[INFO] Executing TSK command: {' '.join(full_command)}" + Style.RESET_ALL)

    try:
        result = subprocess.run(
            full_command,
            capture_output=True,
            text=True,  # Decode stdout/stderr as text
            check=False  # Handle return code manually
        )

        if result.returncode == 0:
            output_data = result.stdout
            if raw_output_path:
                # Save raw output directly to the specified path (e.g., for recovered files)
                with open(raw_output_path, 'w', encoding='utf-8',
                          errors='ignore') as f:  # Use errors='ignore' for binary-like data
                    f.write(output_data)
                print(Fore.GREEN + f"[SUCCESS] Raw output saved to: {raw_output_path}" + Style.RESET_ALL)
            elif save_output:
                # Save formatted text output to a timestamped file
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                output_filename = os.path.join(OUTPUT_DIR,
                                               f"{tool_name}_{os.path.basename(image_path).split('.')[0]}_{timestamp}.txt")

                with open(output_filename, 'w', encoding='utf-8') as f:
                    f.write(output_data)
                print(Fore.GREEN + f"[SUCCESS] Command output saved to: {output_filename}" + Style.RESET_ALL)
            else:
                # Print output directly to the console
                print(Fore.GREEN + "[SUCCESS] Command output:\n" + Style.RESET_ALL)
                print(output_data)
            return True, output_data
        else:
            error_message = (
                f"[ERROR] TSK command '{tool_name}' failed with exit code {result.returncode}.\n"
                f"Stdout: \n{result.stdout.strip()}\n"
                f"Stderr: \n{result.stderr.strip()}"
            )
            print(Fore.RED + error_message + Style.RESET_ALL)
            return False, error_message

    except FileNotFoundError:
        return False, f"[ERROR] TSK tool '{tool_name}' not found at '{full_tool_path}'.\n" \
                      "Please check TSK_TOOL_PREFIX in configuration or ensure tools are in your system's PATH."
    except Exception as e:
        return False, f"[ERROR] An unexpected error occurred during command execution: {e}"


def _list_disk_images() -> list[str]:
    """
    Scans the DISK_IMAGES_DIR and lists all available disk image files.

    Returns:
        list[str]: A list of filenames found in the DISK_IMAGES_DIR.
    """
    print(Fore.BLUE + f"\n[INFO] Checking for disk images in '{DISK_IMAGES_DIR}':" + Style.RESET_ALL)
    images = [f for f in os.listdir(DISK_IMAGES_DIR) if os.path.isfile(os.path.join(DISK_IMAGES_DIR, f))]

    if not images:
        print(
            Fore.YELLOW + "  No disk image files found. Please place .dd, .e01, .raw, etc. files here." + Style.RESET_ALL)
    else:
        for i, image in enumerate(sorted(images)):
            print(f"  [{i + 1}] {image}")
    return images


def _select_disk_image() -> str | None:
    """
    Prompts the user to select a disk image file from the available list.

    Returns:
        str | None: The absolute path of the selected disk image, or None if cancelled.
    """
    images = _list_disk_images()
    if not images:
        return None

    while True:
        try:
            choice = input(
                Fore.MAGENTA + "Enter the number of the disk image to analyze (or 0 to cancel): " + Style.RESET_ALL)
            choice_int = int(choice)

            if choice_int == 0:
                print(Fore.YELLOW + "Disk image selection cancelled." + Style.RESET_ALL)
                return None
            if 1 <= choice_int <= len(images):
                selected_image_filename = sorted(images)[choice_int - 1]
                selected_image_path = os.path.join(DISK_IMAGES_DIR, selected_image_filename)
                print(Fore.GREEN + f"Selected disk image: {selected_image_path}" + Style.RESET_ALL)
                return selected_image_path
            else:
                print(
                    Fore.RED + "Invalid number. Please enter a number from the list or 0 to cancel." + Style.RESET_ALL)
        except ValueError:
            print(Fore.RED + "Invalid input. Please enter a numerical value." + Style.RESET_ALL)


# --- TSK Analysis Submenu for Specific Tools ---
# This menu appears after a disk image has been selected.
# -----------------------------------------------------------------------------

def tsk_analysis_submenu(image_path: str):
    """
    Presents a submenu with specific TSK analysis options for the chosen disk image.

    Args:
        image_path (str): The absolute path to the disk image file being analyzed.
    """
    image_base_name = os.path.basename(image_path)
    print(Fore.WHITE + '\n------------------------------------------------------------------------------')
    print(Fore.WHITE + f'                    TSK Analysis for: {image_base_name} ')
    print(Fore.WHITE + '------------------------------------------------------------------------------')
    print(Fore.BLUE + '''
    [1] List Partition Tables (mmls)
    [2] Show File System Stats (fsstat)
    [3] List Directory Contents (fls)
    [4] Extract File by Inode (icat)
    [5] Raw Image Carving (img_cat)

    [C] Custom TSK Command
    [99] Back to Main TSK Menu (select another image)
        ''')
    print('\r')

    # Variables to store partition and file system information for sub-commands.
    # This avoids re-running mmls/fsstat multiple times for each command.
    current_partition_offset = None
    current_fs_type = None  # Not strictly used here, but good to remember for fsstat context

    while True:
        choice = input(Fore.RED + "analyze" + Fore.LIGHTWHITE_EX + "@" + Fore.RED + "TSK" + Fore.RESET + "~$ ").upper()

        should_save_output = False
        # For certain commands, we might want to ask to save, for others, it's automatic.
        if choice in ["1", "2", "3"]:  # Text-based outputs for these
            save_output_choice = input(Fore.CYAN + "Save output to file? (Y/n): " + Style.RESET_ALL).lower()
            should_save_output = (save_output_choice == 'y' or save_output_choice == '')
        print('\r')

        if choice == "1":  # mmls - List Partition Tables
            success, output = _execute_tsk_command("mmls", [], image_path, should_save_output)
            if success and "Offset" in output:
                # Try to parse offsets for later use with -o
                lines = output.splitlines()
                # Assuming standard mmls output, try to find offsets
                print(
                    Fore.YELLOW + "Detected partitions. To analyze a specific partition, note its 'Start Sector' offset." + Style.RESET_ALL)
                print(Fore.YELLOW + "You will need to enter this offset for 'fsstat', 'fls', etc." + Style.RESET_ALL)
        elif choice == "2":  # fsstat - Show File System Statistics
            offset_str = input(
                Fore.MAGENTA + "Enter partition start offset (e.g., 2048 for a typical first partition, or leave empty for no offset): " + Style.RESET_ALL).strip()
            offset_arg = ['-o', offset_str] if offset_str else []
            _execute_tsk_command("fsstat", offset_arg, image_path, should_save_output)
            if offset_str:
                current_partition_offset = offset_str  # Store for subsequent commands
        elif choice == "3":  # fls - List Directory Contents
            if not current_partition_offset:
                print(
                    Fore.YELLOW + "Warning: No partition offset set. Please run 'fsstat' with an offset first, or manually enter offset." + Style.RESET_ALL)
                offset_str = input(
                    Fore.MAGENTA + "Enter partition start offset for fls (e.g., 2048): " + Style.RESET_ALL).strip()
                if not offset_str:
                    print(Fore.RED + "Partition offset is required for fls. Aborting." + Style.RESET_ALL)
                    input(Fore.WHITE + '\nPress Enter to return to analysis submenu...')
                    continue
                current_partition_offset = offset_str

            directory_path = input(
                Fore.MAGENTA + "Enter directory path (e.g., '/', '/Windows/System32'): " + Style.RESET_ALL).strip()
            # fls command format: fls [options] image [imagesize] [offset] inode
            # We'll map directory_path to inode for simplicity, or use -p for path if needed.
            # For simplicity, we'll assume -p for path and -o for offset.
            fls_args = ['-o', str(current_partition_offset), '-p', directory_path]
            _execute_tsk_command("fls", fls_args, image_path, should_save_output)
        elif choice == "4":  # icat - Extract File by Inode
            if not current_partition_offset:
                print(
                    Fore.YELLOW + "Warning: No partition offset set. Please run 'fsstat' with an offset first, or manually enter offset." + Style.YELLOW)
                offset_str = input(
                    Fore.MAGENTA + "Enter partition start offset for icat (e.g., 2048): " + Style.RESET_ALL).strip()
                if not offset_str:
                    print(Fore.RED + "Partition offset is required for icat. Aborting." + Style.RESET_ALL)
                    input(Fore.WHITE + '\nPress Enter to return to analysis submenu...')
                    continue
                current_partition_offset = offset_str

            inode_num = input(Fore.MAGENTA + "Enter inode number of file to extract: " + Style.RESET_ALL).strip()
            if not inode_num.isdigit():
                print(Fore.RED + "Invalid inode number. Please enter a numeric value." + Style.RESET_ALL)
                continue

            output_filename_base = input(
                Fore.MAGENTA + "Enter output filename for extracted file (e.g., recovered_doc.docx): " + Style.RESET_ALL).strip()
            if not output_filename_base:
                print(Fore.RED + "Output filename cannot be empty." + Style.RESET_ALL)
                continue

            output_full_path = os.path.join(OUTPUT_DIR, output_filename_base)

            # icat args: icat [options] image [imagesize] [offset] inode
            icat_args = ['-o', str(current_partition_offset), inode_num]
            _execute_tsk_command("icat", icat_args, image_path, raw_output_path=output_full_path)

        elif choice == "5":  # img_cat - Raw Image Carving / Concatenation
            # img_cat is typically used to extract raw data blocks or entire image parts.
            # It's less common for specific file carving than icat, but useful for raw data.
            # Example: img_cat image [offset] [len]
            print(
                Fore.YELLOW + "Warning: img_cat is for raw data extraction. It requires an offset and length (in bytes)." + Style.RESET_ALL)
            offset_byte_str = input(
                Fore.MAGENTA + "Enter start byte offset for raw extraction (e.g., 0): " + Style.RESET_ALL).strip()
            length_byte_str = input(
                Fore.MAGENTA + "Enter length in bytes to extract (e.g., 1024): " + Style.RESET_ALL).strip()

            if not (offset_byte_str.isdigit() and length_byte_str.isdigit()):
                print(Fore.RED + "Invalid offset or length. Please enter numeric values." + Style.RESET_ALL)
                continue

            output_filename_base = input(
                Fore.MAGENTA + "Enter output filename for raw data (e.g., raw_data.bin): " + Style.RESET_ALL).strip()
            if not output_filename_base:
                print(Fore.RED + "Output filename cannot be empty." + Style.RESET_ALL)
                continue

            output_full_path = os.path.join(OUTPUT_DIR, output_filename_base)

            img_cat_args = [offset_byte_str, length_byte_str]
            _execute_tsk_command("img_cat", img_cat_args, image_path, raw_output_path=output_full_path)

        elif choice == "C":  # Custom TSK Command
            custom_tool = input(
                Fore.MAGENTA + "Enter custom TSK tool (e.g., 'blkls', 'tsk_recover'): " + Style.RESET_ALL).strip()
            custom_args_str = input(
                Fore.MAGENTA + "Enter any additional arguments (e.g., '-o 2048 /path/to/save', leave empty if none): " + Style.RESET_ALL).strip()

            custom_args = custom_args_str.split() if custom_args_str else []

            # Ask if the user wants to save output for custom commands.
            custom_save_output_choice = input(
                Fore.CYAN + "Save output to file for custom command? (Y/n): " + Style.RESET_ALL).lower()
            custom_should_save_output = (custom_save_output_choice == 'y' or custom_save_output_choice == '')

            _execute_tsk_command(custom_tool, custom_args, image_path, custom_should_save_output)
        elif choice == "99":
            print(Fore.YELLOW + "Returning to disk image selection." + Style.RESET_ALL)
            return  # Exit this submenu, returning to tsk_main_menu()
        else:
            print(Fore.RED + "  Invalid choice. Please select a valid option." + Style.RESET_ALL)

        input(Fore.WHITE + '\nPress Enter to return to analysis submenu...')


# --- Main TSK Menu ---
# This is the entry point for TSK features, handling disk image selection.
# -----------------------------------------------------------------------------

def tsk_main_menu():
    """
    Main menu for The Sleuth Kit (TSK) automation.
    Allows selection of a disk image and launches the analysis submenu.
    """
    while True:
        print(Fore.WHITE + '\n------------------------------------------------------------------------------')
        print(Fore.WHITE + '                     The Sleuth Kit (TSK) Automation Menu                     ')
        print(Fore.WHITE + '------------------------------------------------------------------------------')
        print(Fore.BLUE + '''
    [1] Select Disk Image for Analysis
    [2] View TSK Tool Help (mmls -V or other tool help)

    [99] Back to Main Andromeda Menu
        ''')
        print('\r')

        choice = input(Fore.RED + "tsk" + Fore.LIGHTWHITE_EX + "@" + Fore.RED + "Andromeda" + Fore.RESET + "~$ ")
        print('\r')

        if choice == "1":
            selected_image_path = _select_disk_image()
            if selected_image_path:
                tsk_analysis_submenu(selected_image_path)
            else:
                print(Fore.YELLOW + "No disk image selected. Returning to TSK main menu." + Style.RESET_ALL)
        elif choice == "2":
            # Just show general help for a common TSK tool, like mmls version.
            # You could expand this to list help for specific tools.
            _execute_tsk_command("mmls", ["-V"])  # No image needed for version info
        elif choice == "99":
            print(Fore.YELLOW + "Returning to Main Andromeda Menu." + Style.RESET_ALL)
            return  # Exits this menu, returning to the calling function (e.g., andro_menu)
        else:
            print(Fore.RED + "  Invalid choice. Please select a valid option." + Style.RESET_ALL)

        input(Fore.WHITE + '\nPress Enter to return to TSK menu...')


# --- Script Entry Point ---
# This block allows the script to be run directly for testing purposes.
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    # When this script is run directly, it will start the TSK menu.
    # To test:
    # 1. Ensure TSK tools are installed and in your system's PATH, or set TSK_TOOL_PREFIX.
    # 2. Place disk image files (e.g., .dd, .e01, .raw) into the './disk_images' directory.
    # 3. Run: python tsk_analyzer.py
    print(Fore.GREEN + "Starting TSK Analyzer for Andromeda Framework..." + Style.RESET_ALL)
    tsk_main_menu()