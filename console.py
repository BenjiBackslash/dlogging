import argparse
from dal import DAL
import time
from dlogging.dlogging import str_to_level, level_to_str
parser = argparse.ArgumentParser()
parser.add_argument("-level", nargs='?', default="info")
args = parser.parse_args()





if __name__ == "__main__":
    dal = DAL()
    dal.connect()

    _from = None
    while True:
        level = str_to_level(args.level) if args.level else 10
        docs = dal.get(level, _from=_from)
        for doc in docs:
            _from = doc["time"]
            print("{} {} {} {}".format(doc["time"], doc["source"], level_to_str[doc["level"]], doc["message"]))
        time.sleep(1)



