import docker
import sys
import os
from colorama import Fore, Style, init # For colored output

# Initialize colorama
init(autoreset=True)

# --- Database Configuration ---
DB_IMAGE = "postgres:16"  # Use a specific PostgreSQL version
DB_CONTAINER_NAME = "my-postgres-db"
DB_PORT_HOST = 5432       # Port on your host machine
DB_PORT_CONTAINER = 5432  # Default PostgreSQL port inside the container

# IMPORTANT: For a production environment, use environment variables
# or a secure configuration management system for credentials!
DB_USER = os.environ.get("POSTGRES_USER", "myuser")
DB_PASSWORD = os.environ.get("POSTGRES_PASSWORD", "mypassword")
DB_NAME = os.environ.get("POSTGRES_DB", "mydatabase")

# --- Docker Client Initialization ---
try:
    client = docker.from_env()
    client.ping() # Test connection to Docker daemon
    print(Fore.GREEN + "Connected to Docker daemon successfully." + Style.RESET_ALL)
except Exception as e:
    print(Fore.RED + f"Error connecting to Docker daemon: {e}")
    print(Fore.YELLOW + "Please ensure Docker is running and accessible." + Style.RESET_ALL)
    sys.exit(1)

# --- Docker Database Management Functions ---

def create_db_container():
    """
    Creates and starts a PostgreSQL Docker container.
    """
    print(Fore.CYAN + f"\nAttempting to create and start '{DB_CONTAINER_NAME}' container..." + Style.RESET_ALL)

    try:
        # Check if container already exists
        try:
            container = client.containers.get(DB_CONTAINER_NAME)
            if container.status == 'running':
                print(Fore.YELLOW + f"Container '{DB_CONTAINER_NAME}' is already running." + Style.RESET_ALL)
                return container
            else:
                print(Fore.YELLOW + f"Container '{DB_CONTAINER_NAME}' exists but is not running. Starting it..." + Style.RESET_ALL)
                container.start()
                print(Fore.GREEN + f"Container '{DB_CONTAINER_NAME}' started successfully." + Style.RESET_ALL)
                return container
        except docker.errors.NotFound:
            # Container does not exist, proceed to create
            pass

        # Environment variables for PostgreSQL
        environment_vars = {
            "POSTGRES_USER": DB_USER,
            "POSTGRES_PASSWORD": DB_PASSWORD,
            "POSTGRES_DB": DB_NAME,
        }

        # Port mapping
        ports = {f"{DB_PORT_CONTAINER}/tcp": DB_PORT_HOST}

        # Create and run the container
        container = client.containers.run(
            DB_IMAGE,
            name=DB_CONTAINER_NAME,
            environment=environment_vars,
            ports=ports,
            detach=True,  # Run in background
            restart_policy={"Name": "on-failure", "MaximumRetryCount": 3} # Auto-restart on failure
        )
        print(Fore.GREEN + f"Container '{DB_CONTAINER_NAME}' created and started successfully!" + Style.RESET_ALL)
        print(Fore.YELLOW + f"You can connect to your PostgreSQL database at: localhost:{DB_PORT_HOST}" + Style.RESET_ALL)
        print(Fore.YELLOW + f"  Database: {DB_NAME}" + Style.RESET_ALL)
        print(Fore.YELLOW + f"  User: {DB_USER}" + Style.RESET_ALL)
        print(Fore.YELLOW + f"  Password: {DB_PASSWORD}" + Style.RESET_ALL)
        return container

    except docker.errors.ImageNotFound:
        print(Fore.RED + f"Error: Docker image '{DB_IMAGE}' not found. Please pull it: docker pull {DB_IMAGE}" + Style.RESET_ALL)
    except docker.errors.APIError as e:
        print(Fore.RED + f"Docker API Error: {e}" + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"An unexpected error occurred: {e}" + Style.RESET_ALL)
    return None

def stop_db_container():
    """
    Stops the database container.
    """
    print(Fore.CYAN + f"\nAttempting to stop '{DB_CONTAINER_NAME}' container..." + Style.RESET_ALL)
    try:
        container = client.containers.get(DB_CONTAINER_NAME)
        if container.status == 'running':
            container.stop()
            print(Fore.GREEN + f"Container '{DB_CONTAINER_NAME}' stopped successfully." + Style.RESET_ALL)
        else:
            print(Fore.YELLOW + f"Container '{DB_CONTAINER_NAME}' is not running." + Style.RESET_ALL)
    except docker.errors.NotFound:
        print(Fore.YELLOW + f"Container '{DB_CONTAINER_NAME}' not found." + Style.RESET_ALL)
    except docker.errors.APIError as e:
        print(Fore.RED + f"Docker API Error: {e}" + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"An unexpected error occurred: {e}" + Style.RESET_ALL)

def remove_db_container():
    """
    Stops and removes the database container.
    WARNING: This will delete all data in the container's ephemeral storage.
    """
    print(Fore.CYAN + f"\nAttempting to stop and remove '{DB_CONTAINER_NAME}' container..." + Style.RESET_ALL)
    try:
        container = client.containers.get(DB_CONTAINER_NAME)
        if container.status == 'running':
            print(Fore.YELLOW + f"Stopping '{DB_CONTAINER_NAME}' before removal..." + Style.RESET_ALL)
            container.stop()
        container.remove() # Removes the container
        print(Fore.GREEN + f"Container '{DB_CONTAINER_NAME}' removed successfully." + Style.RESET_ALL)
    except docker.errors.NotFound:
        print(Fore.YELLOW + f"Container '{DB_CONTAINER_NAME}' not found." + Style.RESET_ALL)
    except docker.errors.APIError as e:
        print(Fore.RED + f"Docker API Error: {e}" + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"An unexpected error occurred: {e}" + Style.RESET_ALL)

def get_db_status():
    """
    Gets the status of the database container.
    """
    try:
        container = client.containers.get(DB_CONTAINER_NAME)
        print(Fore.BLUE + f"\nContainer '{DB_CONTAINER_NAME}' status: {container.status}" + Style.RESET_ALL)
        if container.status == 'running':
            print(Fore.BLUE + f"  Ports: {container.ports}" + Style.RESET_ALL)
    except docker.errors.NotFound:
        print(Fore.YELLOW + f"\nContainer '{DB_CONTAINER_NAME}' does not exist." + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"An unexpected error occurred getting status: {e}" + Style.RESET_ALL)


# --- Main Menu for the Program ---
def db_management_menu():
    """
    Main menu for managing the database Docker container.
    """
    while True:
        print(Fore.WHITE + '\n------------------------------------------------------------------------------')
        print(Fore.WHITE + '                         Docker Database Manager                               ')
        print(Fore.WHITE + '------------------------------------------------------------------------------')
        print(Fore.BLUE + '''
    [1] Start/Create Database Container
    [2] Stop Database Container
    [3] Remove Database Container (WARNING: Data will be lost!)
    [4] Check Database Status
    [99] Exit
        ''')
        print('\r')
        try:
            choice = input(Fore.RED + "db_manager" + Fore.LIGHTWHITE_EX + "@" + Fore.RED + "Andromeda" + Fore.RESET + "~$ ")
            print('\r')

            if choice == "1":
                create_db_container()
            elif choice == "2":
                stop_db_container()
            elif choice == "3":
                confirm = input(Fore.YELLOW + "Are you sure you want to remove the container and lose all its data? (y/N): " + Style.RESET_ALL).lower()
                if confirm == 'y':
                    remove_db_container()
                else:
                    print(Fore.WHITE + "Removal cancelled." + Style.RESET_ALL)
            elif choice == "4":
                get_db_status()
            elif choice == "99":
                print(Fore.YELLOW + "Exiting Docker Database Manager. Goodbye!" + Style.RESET_ALL)
                sys.exit(0)
            else:
                print(Fore.RED + "  Invalid choice. Please select a valid option." + Style.RESET_ALL)
            input(Fore.WHITE + '\nPress Enter to continue to menu...')

        except KeyboardInterrupt:
            print(Fore.YELLOW + "\nOperation cancelled. Exiting Docker Database Manager." + Style.RESET_ALL)
            sys.exit(0)

# --- Run the Manager ---
if __name__ == "__main__":
    db_management_menu()