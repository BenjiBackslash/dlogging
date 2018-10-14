import os
from pymongo.errors import PyMongoError
from dlogging.check_file_free import _dlogging_home, _updater_pid_file, _check_file_free
from dlogging.dlogging import _file_name_base
from datetime import datetime
import time
from dal import DAL

def parse_line(line):
    parts = line.split("#")
    return {
        "time": datetime.strptime(parts[0], "%Y-%m-%d %H:%M:%S.%f"),
        "source": parts[1],
        "level": int(parts[2]),
        "message": parts[3].rstrip("\n")

    }

def parse_file_name_pid(file_name):
    parts = file_name.split(".")
    pid = int(parts[1])
    return pid


if __name__ == "__main__":

    pid = os.getpid()
    with open(_updater_pid_file, "w") as fdw:
        fdw.write(str(pid))

    dal = DAL()
    dal.connect()

    while True:
        if os.path.exists(_dlogging_home):
            for f_name in os.listdir(_dlogging_home):
                path = os.path.join(_dlogging_home, f_name)
                if not os.path.isdir(path) and f_name.startswith(_file_name_base):
                    pid = parse_file_name_pid(f_name)
                    if _check_file_free(pid, path):
                        cur_docs = []
                        failed = False
                        try:
                            with open(path, "r") as fdr:
                                for line in fdr:
                                    doc = parse_line(line)
                                    cur_docs.append(doc)
                            os.remove(path)
                            dal.insert_many(cur_docs)
                        except IOError:
                            pass  # failed in opening, parsing, deleting. can happen if logger is operating on the file.
                                  # and as a result we dont delete so its ok.
                        except PyMongoError:
                            pass  # this will cause loss of the messages.
        print("amount of records in the DB: {}".format(dal.count()))
        time.sleep(30)




