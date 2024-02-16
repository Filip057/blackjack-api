from .common import *
import os
import dotenv


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

dotenv.load_dotenv()
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'default-secret-key')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'blackjack',
        'USER': 'root',
        'PASSWORD': os.getenv('MYSQL_PASSWORD'),
        'HOST': 'localhost',   # Or the MySQL server host
        'PORT': '3306',        # Or the MySQL server port
    }
}
