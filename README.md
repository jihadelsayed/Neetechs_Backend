# Neetechs_Backend


# to activate venv
On Unix or MacOS, using the bash shell: source /path/to/venv/bin/activate
On Unix or MacOS, using the csh shell: source /path/to/venv/bin/activate.csh
On Unix or MacOS, using the fish shell: source /path/to/venv/bin/activate.fish
On Windows using the Command Prompt: path\to\venv\Scripts\activate.bat
On Windows using PowerShell: path\to\venv\Scripts\Activate.ps1

# error no python
No Python at 'C:\Users\jihad\AppData\Local\Programs\Python\Python310\python.exe'
change pyvenv.cfg to where is your python is

# install pip
```
python -m pip install --upgrade pip
```
# to install
```
pip install -r requirements.txt
```



# Installing Django
pip install django

# Installing requirment library
pip install python-decouple

python -m pip install --upgrade pip
pip install daphne

pip install django-restframework
pip3 install djangorestframework
pip install -U django-rest-knox
pip install django-cors-headers
pip install django-filter
pip install django-storages
pip install Pillow
pip install requests
pip install opencv-python
pip install django_countries
pip install boto3
pip install django-imagekit==4.0.2.0
pip install djangorestframework_recaptcha
pip install django-push-notifications
pip install psycopg2-binary 
pip install stripe==2.57.0



# pip install django-pyodbc-azure
# pip install psycopg2-binary
pip install fcm-django<1

# collect static for aws s3
```
python manage.py collectstatic

```
##### Set up the postgresql
List of commands used:

sudo apt update
apt install postgresql postgresql-contrib
update-rc.d postgresql enable
service postgresql startcd ../etc/postgresql/9.5/main
edit pg_hba.conf:   all  all  (YOUR IP ADDRESS)/32   trust
edit postgresql.conf:  listen_addresses = '*' 

service postgresql restart