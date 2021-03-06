#
#  This is a example how how to integrate Quartermaster with a LDAP server
#
#  This configure requires "django-auth-ldap" to be added to "local_requirements.txt"
#
from datetime import timedelta
from io import StringIO
from urllib.parse import urlparse

import ldap
import paramiko
from django_auth_ldap.config import LDAPSearch

from ..base_settings import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'REPLACE_THIS'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

SERVER_BASE_URL = 'http://localhost:8000'
parsed_server_base_url = urlparse(SERVER_BASE_URL)

ALLOWED_HOSTS = ['backend', 'localhost', parsed_server_base_url.netloc]

# INSTALLED_APPS.extend([
#     'Teamcity',
# ])

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'REPLACE_THIS',
        'USER': 'REPLACE_THIS',
        'PASSWORD': 'REPLACE_THIS',
        'HOST': 'REPLACE_THIS',
    }
}

HUEY['connection']['host'] = "redis"
HUEY['consumer']['workers'] = 2

RESERVATION_MAX_MINUTES = timedelta(minutes=10)
RESERVATION_CHECKIN_TIMEOUT_MINUTES = timedelta(minutes=5)

########### SSH ###########
SSH_USERNAME = 'REPLACE_THIS'
# This is a example of how to load a private key as a string.
SSH_PRIVATE_KEY = paramiko.Ed25519Key.from_private_key(StringIO(
    """-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAAAMwAAAAtzc2gtZW
QyNTUxOQAAACBEwsJ2uZejpjzK4/aWeHgC7XFCC1RzfwC1pnq+K/QPhwAAAKCoPnpuqD56
bgAAAAtzc2gtZWQyNTUxOQAAACBEwsJ2uZejpjzK4/aWeHgC7XFCC1RzfwC1pnq+K/QPhw
AAAEBfU90mkx6CtUhIBc+d3JvXRN1idaETz+SeOhRv2mXXr0TCwna5l6OmPMrj9pZ4eALt
cUILVHN/ALWmer4r9A+HAAAAGXRpbS5sYXVyZW5jZUBzcGYzLXRvcGF6LTEBAgME
-----END OPENSSH PRIVATE KEY-----
"""))

# ########### TeamCity Intergration ###########
# TEAMCITY_USER = 'REPLACE_THIS'
# TEAMCITY_PASSWORD = 'REPLACE_THIS'
# TEAMCITY_HOST = 'https://REPLACE_THIS'
# TEAMCITY_RESERVATION_USERNAME = 'REPLACE_THIS'

########### LDAP CONFIGURATION ###########
AUTHENTICATION_BACKENDS = (
    "django_auth_ldap.backend.LDAPBackend",
    "django.contrib.auth.backends.ModelBackend"
)

AUTH_LDAP_SERVER_URI = 'ldap://ldap.example.com'
AUTH_LDAP_START_TLS = True
AUTH_LDAP_BIND_DN = 'CN=bind,OU=Services,OU=Users,DC=example,DC=com'
AUTH_LDAP_BIND_PASSWORD = 'REPLACE_THIS'
AUTH_LDAP_USER_SEARCH = LDAPSearch('OU=User,DC=example,DC=com', ldap.SCOPE_SUBTREE,
                                   "sAMAccountName=%(user)s")
AUTH_LDAP_USER_ATTR_MAP = {
    "username": "sAMAccountName",
    "first_name": "givenName",
    "last_name": "sn",
    "email": "mail",
}
# If you are having LDAP issues this may help debug them
# ldap.set_option(ldap.OPT_DEBUG_LEVEL, 4095)

# AUTH_LDAP_USER_FLAGS_BY_GROUP = {
#     "is_active": "cn=active,ou=django,ou=groups,dc=example,dc=com",
#     "is_staff": "cn=staff,ou=django,ou=groups,dc=example,dc=com",
#     "is_superuser": "OU=superusers,DC=example,DC=com",
# }
