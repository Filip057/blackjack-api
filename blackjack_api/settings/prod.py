from .common import *
import os
import dotenv

dotenv.load_dotenv()

DEBUG = False

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '[::1]']

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'default-secret-key')