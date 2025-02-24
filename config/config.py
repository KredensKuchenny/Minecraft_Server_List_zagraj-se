# Brand/service name
brand_name = "zagraj.se"

# Production mode (True means the application is running in a production environment)
production_mode = False

# Debug mode (False means debugging is disabled)
debug_mode = False

# Timezone in which the application operates
timezone = "Europe/Warsaw"

# Database login details (in this case, MongoDB)
database_login = {
    "host": "127.0.0.1",  # Database host address
    "port": "27017",  # Port where MongoDB is running
    "authentication_database": "zagraj_database",  # Database used for authentication
    "user": "zagraj_user",  # Database username
    "password": "zagraj_password",  # Database password
}

# The collection in the database that stores information about servers
server_list_collection = "server_list"

# The collection in the database that stores contact requests
contact_collection = "contact_requests"

# Time (in seconds) between consecutive updates of the server list
server_list_update_in_seconds = 30

# Time (in seconds) between consecutive updates of the server status
servers_status_update_in_seconds = 600

# Time (in days) after which an offline server is deleted from the database
offline_server_delete_time_in_days = 1

# Time (in hours) the user must wait before voting again
user_vote_cooldown_in_hours = 24
