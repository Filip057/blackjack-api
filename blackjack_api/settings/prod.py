from .common import *
import os
import dotenv

dotenv.load_dotenv()

DEBUG = False

ALLOWED_HOSTS = []

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'default-secret-key')