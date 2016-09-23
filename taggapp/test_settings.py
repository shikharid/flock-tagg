from settings import *

import os

PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.MD5PasswordHasher',
)

DEBUG = True

EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'

COMPRESS_ENABLED = False
MEDIA_ROOT = os.path.join(BASE_DIR, 'media-test/')

# Re assigning because debug_toolbar should not be included while testing
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS
