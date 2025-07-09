from datetime import datetime
import sys


class LogType:
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    SUCCESS = "SUCCESS"
    DEBUG = "DEBUG"

def _current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def log(message, log_type=LogType.INFO, file=sys.stdout):
    timestamp = _current_time()
    print(f"[{timestamp}] [{log_type}] {message}", file=file)

def info(message):
    log(message, LogType.INFO)

def warning(message):
    log(message, LogType.WARNING)

def error(message):
    log(message, LogType.ERROR, file=sys.stderr)

def success(message):
    log(message, LogType.SUCCESS)

def debug(message):
    log(message, LogType.DEBUG)
