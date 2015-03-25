from VLCwebsite.settings import *

DEBUG = TEMPLATE_DEBUG = False
DATABASE_NAME = 'production'
DATABASE_USER = 'app'
DATABASE_PASSWORD = 'letmein'

#CSRF_COOKIE_SECURE = True
#SESSION_COOKIE_SECURE = True

CONN_MAX_AGE = 60