from decouple import config

# PG_LOGIN = config('PG_LOGIN')
# PG_PASSWORD = config('PG_PASSWORD')
# PG_DBNAME = config('PG_DBNAME')
# PG_DBHOST = config('PG_DBHOST')
# PG_PORT = config('PG_PORT')
# PG_CONN_PARAMS = config('PG_PARAMS', default='')

SQLITE_DB = config('SQLITE_DB')
JWT_SECRET_KEY = config('JWT_SECRET_KEY', default='jwt_secret')  # openssl rand -hex 32
JWT_ALGORYTHM = config('JWT_ALGORYTHM')
JWT_EXPIRE_MINUTES = config('JWT_EXPIRE_MINUTES', cast=int)

SESSION_SECRET_KEY = config('SESSION_SECRET_KEY', default='super-secret-key')

YANDEX_CLIENT_ID = config('YANDEX_CLIENT_ID')
YANDEX_CLIENT_SECRET = config('YANDEX_CLIENT_SECRET')
YANDEX_CODE_URI = 'https://oauth.yandex.ru/authorize'
YANDEX_TOKEN_URI = 'https://oauth.yandex.ru/token'

VK_CLIENT_ID = config('VK_CLIENT_ID')
VK_CLIENT_SECRET = config('VK_CLIENT_SECRET')
VK_CODE_URI = 'https://oauth.vk.com/authorize'
VK_TOKEN_URI = 'https://oauth.vk.com/access_token'
