# Digitalflake - Django Project

GitHub Repository: https://github.com/Satish1097/Digitalflake.git

## Requirements  
- Python 3.10  
- pip  
- virtualenv  
- PostgreSQL  

## Setup Instructions  

1. Clone the Repository  
git clone https://github.com/Satish1097/Digitalflake.git


2. Create and Activate Virtual Environment  
python3 -m venv env

On Windows:
env\Scripts\activate

On macOS/Linux:
source env/bin/activate

3. Install Dependencies  
pip install -r requirements.txt

Create a `.env` file in the project root with the following content:  

SECRET_KEY=your-secret-key
DEBUG=True

DATABASE_NAME=your_db_name
DATABASE_USER=your_db_user
DATABASE_PASSWORD=your_db_password
DATABASE_HOST=127.0.0.1
DATABASE_PORT=5432

EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_USE_SSL=False
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-email-password

python manage.py makemigrations
python manage.py migrate

python manage.py createsuperuser

python manage.py runserver


