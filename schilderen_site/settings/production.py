from .base import *

print("✅ Using production settings")
print("✅ ROOT_URLCONF is:", ROOT_URLCONF)


DEBUG = True

ALLOWED_HOSTS = ['.onrender.com',            
    'schilderen-met-sabine.onrender.com',
    'www.schilderen-met-sabine.onrender.com',
    'schilderenmetsabine.nl',
    'www.schilderenmetsabine.nl',
]



try:
    from .local import *    
except ImportError:
    pass

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
}
