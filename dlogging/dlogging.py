import threading
from email._header_value_parser import InvalidMailbox
from queue import Queue, Empty
from dlogging.check_file_free import _dlogging_home, _logger_check_file_free
import time
from datetime import datetime
import os


DEBUG = 10
INFO = 20
WARNING = 30
ERROR = 40
CRITICAL = 50

_q = Queue()
_configured = False
_log_thread = None
_level = None
_file_path = None

_file_name_base = "the_log_file"
_file_name_ext = "log"


def make_file_name(pid):
    return "{}.{}.{}".format(_file_name_base, str(pid), _file_name_ext)


class _DLoggingThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while True:
            if not _q.empty():
                try:
                    _free = _logger_check_file_free(_file_path)
                    if _free:
                        with open(_file_path, "a") as fdw:
                            try:
                                while True:
                                    message = _q.get(block=False)
                                    fdw.write("{time}#{source}#{level}#{message}\n".format(**message))
                            except Empty:
                                pass
                except IOError:
                    pass
            time.sleep(1)


def basicConfig(source="my_process", level=INFO):
    global _configured
    global _log_thread
    global _level
    global _source
    global _file_path
    if _configured:
        raise IOError("already configured")
    pid = os.getpid()
    _file_path = os.path.join(_dlogging_home, make_file_name(pid))
    _source = source
    _level = level
    _log_thread = _DLoggingThread()
    _log_thread.start()


level_to_str = {
    DEBUG: "debug",
    INFO: "info",
    WARNING: "warning",
    ERROR: "error",
    CRITICAL: "critical",
}

def str_to_level(s):
    for k, _s in level_to_str.items():
        if _s == s:
            return k
    return -1




def _add_message(message, level):
    if level >= _level:
        _q.put(
            {
                "time": datetime.utcnow(),
                "source": _source,
                "level": level,
                "message": message
            }
        )


def debug(message):
    _add_message(message, DEBUG)


def info(message):
    _add_message(message, INFO)


def warning(message):
    _add_message(message, WARNING)


def error(message):
    _add_message(message, ERROR)


def critical(message):
    _add_message(message, CRITICAL)



