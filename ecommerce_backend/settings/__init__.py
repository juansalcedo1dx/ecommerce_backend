import os

env = os.environ.get('DJANGO_ENV', 'dev')  # 'prod' o 'dev'

if env == 'prod':
    from .prod import *
else:
    from .dev import *
