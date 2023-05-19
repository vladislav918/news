# Django project 

- Python 3.9
- Django 3.2
- PostgreSQL

## Installation and launch of the project

To install and run the project, follow these steps:

1. Clone the repository on your computer:

git clone https://github.com/vladislav918/news.git

2. Create a virtual environment and activate it:

python -m venv env
source env/bin/activate

3. Install project dependencies:

pip install -r requirements.txt

4. Create a PostgreSQL database and set up a connection to it in a file `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mydatabase',
        'USER': 'mydatabaseuser',
        'PASSWORD': 'mypassword',
        'HOST': 'localhost',
        'PORT': '',
    }
}
```

5. Run migrations to create tables in the database:

python manage.py migrate

6. Run server:

python manage.py runserver
