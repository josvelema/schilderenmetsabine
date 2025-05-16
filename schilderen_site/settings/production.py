from .base import *

DEBUG = False

ALLOWED_HOSTS = [
    'schilderen-met-sabine.onrender.com',
    'www.schilderen-met-sabine.onrender.com',
    'schilderenmetsabine.nl',
    'www.schilderenmetsabine.nl',
]


try:
    from .local import *
except ImportError:
    pass
