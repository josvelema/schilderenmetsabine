from .base import *

print("✅ Using production settings")
print("✅ ROOT_URLCONF is:", ROOT_URLCONF)


DEBUG = False

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
