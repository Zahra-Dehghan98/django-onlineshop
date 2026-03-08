import os

env = os.getenv("DJANGO-ENV", "dev").lower()

if env == 'dev':
    from .dev import *
if env == 'prod':
    from .prod import *