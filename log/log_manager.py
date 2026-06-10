from datetime import datetime
import os

_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

_LEVELS = {
    'DEBUG': 0,
    'INFO': 1,
    'ERROR': 2
}

LOG_LEVEL = os.environ.get('LOG_LEVEL', 'DEBUG').upper()
_CURRENT_LEVEL = _LEVELS.get(LOG_LEVEL, 0)

def _log(level_name, message):
    #if _LEVELS[level_name] >= _CURRENT_LEVEL:
    print(f'{datetime.now().strftime(_DATE_FORMAT)} - {level_name} - {message} | {LOG_LEVEL} - {_CURRENT_LEVEL}')

def log_error(message):
    _log('ERROR', message)

def log_info(message):
    _log('INFO', message)

def log_debug(message):
    _log('DEBUG', message)