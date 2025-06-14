import docker
import datetime
import os
import sys
from colorama import Fore, Style, init

# Initialize Colorama for cross-platform colored output
init(autoreset=True)

# --- Database Configuration (MUST match your docker-compose.yml) ---
DB_CONTAINER_NAME = "my-postgres-db"
DB_USER = os.environ.get("POSTGRES_USER", "myuser")        # Gets from environment variable, fallback to 'myuser'
DB_PASSWORD = os.environ.get("POSTGRES_PASSWORD", "mypassword") # Gets from environment variable, fallback to 'mypassword'
DB_NAME = os.environ.get("POSTGRES_DB", "mydatabase")      # Gets from environment variable, fallback to 'mydatabase'

# --- Backup Destination Configuration ---
BACKUP_DIR = "db_backups" # Local directory where backups will be saved
BACKUP_FILENAME_FORMAT = "{db_name}_{timestamp}.sql" # e.g., mydatabase_20250607_235900.sql

# --- Docker Client Initialization ---
try:
    client = docker.from_env()
    client.ping() # Test connection to Docker daemon
    print(Fore.GREEN + "  Connected to Docker daemon successfully." + Style.RESET_ALL)
except Exception as e:
    print(Fore.RED + f"  Error connecting to Docker daemon: {e}")
    print(Fore.YELLOW + "  Please ensure Docker Desktop/Daemon is running and accessible." + Style.RESET_ALL)
    sys.exit(1) # Exit if Docker daemon is not accessible

def backup_database():
    """
    Connects to the running PostgreSQL container and performs a database backup
    using pg_dump, saving the output to a local .sql file.
    """
    print(Fore.CYAN + f"\n------------------------------------------------------------------------------")
    print(Fore.CYAN + f"                                 DATABASE BACKUP                             ")
    print(Fore.CYAN + f"------------------------------------------------------------------------------")
    print(Fore.CYAN + f"  Attempting to back up database '{DB_NAME}' from container '{DB_CONTAINER_NAME}'..." + Style.RESET_ALL)

    # Ensure the backup directory exists
    try:
        os.makedirs(BACKUP_DIR, exist_ok=True)
    except OSError as e:
        print(Fore.RED + f"  Error creating backup directory '{BACKUP_DIR}': {e}" + Style.RESET_ALL)
        return False

    try:
        # Get the database container
        container = client.containers.get(DB_CONTAINER_NAME)

        # Check if the container is running
        if container.status != 'running':
            print(Fore.RED + f"  Error: Container '{DB_CONTAINER_NAME}' is not running (status: {container.status}). Please start it first (e.g., `docker compose up -d`)." + Style.RESET_ALL)
            return False

        # Generate a timestamp for the backup filename
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = BACKUP_FILENAME_FORMAT.format(db_name=DB_NAME, timestamp=timestamp)
        backup_filepath = os.path.join(BACKUP_DIR, backup_filename)

        # Define the pg_dump command to be executed inside the container
        # We pass PGPASSWORD as an environment variable for security,
        # so it's not visible in process lists.
        pg_dump_command = [
            "pg_dump",
            "-U", DB_USER,        # User for the database
            "-d", DB_NAME,        # Database name to dump
            "-h", "localhost",    # Host (localhost from container's perspective)
            "-p", "5432"          # Port (default PostgreSQL port inside container)
            # You can add -Fc for custom format (binary), or -Fp for plain text (default).
            # We'll use plain text SQL by default for simplicity.
        ]

        # Execute pg_dump command inside the container
        # container.exec_run returns a tuple: (exit_code, output_bytes)
        # demux=True allows getting stdout and stderr separately
        print(Fore.YELLOW + f"  Executing pg_dump inside container '{DB_CONTAINER_NAME}'..." + Style.RESET_ALL)
        exit_code, (stdout, stderr) = container.exec_run(
            cmd=pg_dump_command,
            environment={"PGPASSWORD": DB_PASSWORD}, # Securely pass the password
            stream=False, # Get all output at once
            demux=True    # Demultiplex stdout and stderr
        )

        if exit_code == 0:
            # Write the stdout (database dump) to the local file
            with open(backup_filepath, 'wb') as f: # Use 'wb' as output_bytes is bytes
                f.write(stdout)
            print(Fore.GREEN + f"  Database backup successful! Saved to: {backup_filepath}" + Style.RESET_ALL)
            return True
        else:
            print(Fore.RED + f"  pg_dump failed with exit code {exit_code}." + Style.RESET_ALL)
            if stderr:
                print(Fore.RED + "  Error output from pg_dump:\n" + stderr.decode('utf-8'))
            return False

    except docker.errors.NotFound:
        print(Fore.RED + f"  Error: Container '{DB_CONTAINER_NAME}' not found. Please ensure it is correctly named and exists." + Style.RESET_ALL)
        return False
    except docker.errors.APIError as e:
        print(Fore.RED + f"  Docker API Error: {e}" + Style.RESET_ALL)
        return False
    except Exception as e:
        print(Fore.RED + f"  An unexpected error occurred during backup: {e}" + Style.RESET_ALL)
        return False

# --- Main Execution (You can integrate this into your Andromeda menu) ---
if __name__ == "__main__":
    print(Fore.MAGENTA + "This script will attempt to backup your PostgreSQL database running in Docker." + Style.RESET_ALL)
    print(Fore.MAGENTA + "Ensure your 'my-postgres-db' container is running and your Docker Compose credentials match." + Style.RESET_ALL)

    backup_database()

    print(Fore.WHITE + "\n------------------------------------------------------------------------------")
    print(Fore.WHITE + "                           Backup Process Completed                           ")
    print(Fore.WHITE + "------------------------------------------------------------------------------")

    # Example of how you would integrate this into your Andromeda main menu:
    # You would create a new option in andro_menu() or a sub-menu like "Database Tools"
    # that calls the 'backup_database()' function.
    # For instance:
    # def andro_menu():
    #     # ... existing menu options ...
    #     print("[9] Database Tools")
    #     # ... rest of menu ...
    #     choice = input(...)
    #     if choice == "9":
    #         # You'd define a db_tools_menu() or directly call backup_database()
    #         backup_database()
    #         input('Press Enter to return to main menu...')
    #         andro_menu()
    #     # ...