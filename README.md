# Neetechs Backend

## Description

This is the backend for the Neetechs platform, built with Django. It provides APIs for user management, services, categories, checkout, chat, and more. <!-- User: Please update this description with more specific details about your project's purpose. -->

## Prerequisites

Before you begin, ensure you have the following installed:
*   Python 3.x (check your project's specific version requirements)
*   pip (Python package installer)
*   PostgreSQL (or the database system configured for the project)

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository-url>
cd neetechs-backend # Or your repository's directory name
```
<!-- User: Please replace `<repository-url>` with the actual URL of your repository. -->

### 2. Create and Activate a Virtual Environment

It's highly recommended to use a virtual environment to manage project dependencies.

**Unix/macOS (bash/zsh):**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows (Command Prompt):**
```bash
python -m venv venv
venv\Scripts\activate.bat
```

**Windows (PowerShell):**
```bash
python -m venv venv
venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

First, upgrade pip:
```bash
python -m pip install --upgrade pip
```

Then, install all required packages from `requirements.txt`:
```bash
pip install -r requirements.txt
```
This file should contain all necessary libraries like Django, Django REST framework, django-rest-knox, etc.

### 4. Database Setup

This project likely uses PostgreSQL.
*   Ensure PostgreSQL is installed and running on your system or accessible.
*   You will need to create a database and a user for this project.
*   Configure your database connection details in the environment variables (see next section).

For detailed instructions on installing and configuring PostgreSQL, please refer to the [official PostgreSQL documentation](https://www.postgresql.org/docs/). For Django-specific database setup, see the [Django database setup documentation](https://docs.djangoproject.com/en/stable/topics/db/models/#database-setup).

#### PostgreSQL Setup Notes (Linux Example)

The following commands are an example of how you might set up PostgreSQL on a Linux system. Adapt these to your specific environment and security requirements.

```bash
sudo apt update
sudo apt install postgresql postgresql-contrib

# Enable PostgreSQL to start on boot (system-dependent, may not be needed for all systems)
# sudo systemctl enable postgresql 
# sudo systemctl start postgresql 
# Or for older systems:
# update-rc.d postgresql enable
# service postgresql start

# --- Configuration (example paths, adjust as needed) ---
# The configuration files are typically in a version-specific directory, e.g., /etc/postgresql/X.Y/main/
# cd /etc/postgresql/<YOUR_PG_VERSION>/main/
#
# Edit pg_hba.conf to allow connections. 
# For local development, 'host all all 127.0.0.1/32 md5' or 'trust' might be used.
# For remote access, replace YOUR_IP_ADDRESS with your actual IP:
# Example: host    all             all             YOUR_IP_ADDRESS/32       md5
#
# Edit postgresql.conf to listen on appropriate addresses:
# Example: listen_addresses = 'localhost, YOUR_SERVER_IP' 
# (or '*' for all, but be careful with security implications)
#
# sudo systemctl restart postgresql # Or: service postgresql restart
```
**Note:** Modifying `pg_hba.conf` and `postgresql.conf` requires careful consideration of security. The example `trust` method is not recommended for production. Always use strong passwords and appropriate authentication methods. The commands `update-rc.d postgresql enable` and `service postgresql start` are for older SysVinit systems; modern systems typically use `systemctl`.

### 5. Environment Variables

This project uses `python-decouple` to manage application settings. You will likely need to create a `.env` file in the project root.

If a `.env.example` file is provided in the repository, copy it to `.env`:
```bash
cp .env.example .env
```
Then, edit the `.env` file to set the required environment variables, such as:
*   `SECRET_KEY`
*   Database settings (`DATABASE_URL` or individual `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`)
*   Email configuration
*   Stripe API keys
*   Any other external service credentials.

<!-- User: Please provide a .env.example file or list required environment variables here. -->

## Running the Development Server

Once the setup is complete, run the following commands to start the development server:

1.  **Create database migrations:**
    ```bash
    python manage.py makemigrations
    ```

2.  **Apply database migrations:**
    ```bash
    python manage.py migrate
    ```

3.  **Start the development server:**
    ```bash
    python manage.py runserver
    ```
The server will typically be available at `http://127.0.0.1:8000/`.

## Static Files (for Deployment)

When deploying your application, you'll need to collect all static files (CSS, JavaScript, images) into a single location. Django uses the `collectstatic` command for this.

```bash
python manage.py collectstatic
```
This command copies all static files from your apps into the directory specified by `STATIC_ROOT` in your `settings.py`.

If you are using `django-storages` and `boto3` to serve static files from a service like AWS S3, `collectstatic` will handle uploading these files to your configured S3 bucket.

## Troubleshooting

### Python Interpreter Mismatch in Virtual Environment
If you encounter an error like `No Python at 'C:\Users\jihad\AppData\Local\Programs\Python\Python310\python.exe'`, it means the Python interpreter specified in your virtual environment's `pyvenv.cfg` file is incorrect or the path has changed.

**Solution:**
1.  Open the `pyvenv.cfg` file located in the root of your virtual environment (e.g., `venv/pyvenv.cfg`).
2.  Look for the `home` key (or similar, depending on your OS and Python version).
3.  Update the path to point to the correct location of your Python executable.
    For example, if your Python 3.10 is actually at `C:\Python310\python.exe`, change it accordingly.
4.  Save the file and try reactivating the virtual environment.
