# backup_db.py (updated config section)
import os
# ... other imports

# --- Database & Container Configuration ---
# Read from environment variables, providing defaults if not set
DB_CONTAINER_NAME = os.environ.get("PG_CONTAINER_NAME", "my-postgres-db")
DB_USER = os.environ.get("POSTGRES_USER", "myuser")
DB_PASSWORD = os.environ.get("POSTGRES_PASSWORD", "mypassword") # WARNING: For production, do NOT read password like this for direct use!
DB_NAME = os.environ.get("POSTGRES_DB", "mydatabase")
BACKUP_DIR = "./backups" # Directory on your host machine where backups will be stored

# ... rest of your backup_db.py script