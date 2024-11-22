import decouple

DROPBOX_ACCESS_TOKEN = decouple.config('DROPBOX_ACCESS_TOKEN')
PATH_DROPBOX = decouple.config('PATH_DROPBOX')

LOG_FILE = 'logs/app.log'

LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'