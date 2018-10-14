import os
import re


_home_dir = os.path.expanduser('~')
_dlogging_home = os.path.join(_home_dir, "dlogging")
if not os.path.exists(_dlogging_home):
    os.makedirs(_dlogging_home)
_updater_pid_file = os.path.join(_dlogging_home,'updater.pid')


def iterate_fds(pid):
    dir = '/proc/'+str(pid)+'/fd'
    if not os.access(dir,os.R_OK|os.X_OK): return

    for fds in os.listdir(dir):
        for fd in fds:
            full_name = os.path.join(dir, fd)
            try:
                file = os.readlink(full_name)
                if file == '/dev/null' or \
                  re.match(r'pipe:\[\d+\]',file) or \
                  re.match(r'socket:\[\d+\]',file):
                    file = None
            except OSError as err:
                if err.errno == 2:
                    file = None
                else:
                    raise(err)

            yield (fd,file)


def _get_updater_pid():
    pid = None
    if os.path.exists(_updater_pid_file):
        with open(_updater_pid_file, "r") as fdr:
            pid = fdr.readline()
    return pid


def _check_file_free(pid, file_path):
    if pid is not None:
        for fd, file in iterate_fds(pid):
            if file == file_path:
                return False
    return True


def _logger_check_file_free(file_path):
    pid = _get_updater_pid()
    return _check_file_free(pid, file_path)
