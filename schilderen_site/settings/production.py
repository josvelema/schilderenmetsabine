from .base import *

DEBUG = False

ALLOWED_HOSTS = [
    'schilderen-met-sabine.onrender.com',
    'www.schilderen-met-sabine.onrender.com',
    'schilderenmetsabine.nl',
    'www.schilderenmetsabine.nl',
]

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-at#)%wm1keq%zf*gi=mcsjd21a$c5%l)lxj4l85$dhz8!b#ejw"


try:
    from .local import *
except ImportError:
    pass
