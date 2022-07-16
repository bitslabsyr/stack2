'''
'''
import os
import json
import logging
import logging.handlers
import time
import shutil
import datetime

import pymongo

LOG_PATH = "/var/stacks/logs"
DATA_PATH = "/var/stacks/data"
DATA_ARCHIVE_PATH = "/var/stacks/data_archive"

def initialize_info_logger(log_config):
    formatter = logging.Formatter(fmt='%(asctime)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    rotating_handler = logging.handlers.TimedRotatingFileHandler(**log_config)
    rotating_handler.suffix = "%Y-%m-%d_%H-%M-%S.log"
    rotating_handler.setFormatter(formatter)
    info_logger = logging.getLogger('Info_Logger')
    info_logger.setLevel(logging.INFO)
    info_logger.addHandler(rotating_handler)
    return info_logger

def push_rows(CTX, rows):
    info_logger = logging.getLogger('Info_Logger')

    db_config = CTX["persistance"]

    server_name = db_config["server_name"]
    port = db_config["port"]
    username = db_config["username"]
    password = db_config["password"]
    database_name = db_config["database_name"]
    collection_name = db_config["collection_name"]

    server_url = f"mongodb://{username}:{password}@{server_name}:{port}"

    mongoClient= pymongo.MongoClient(server_url)
    mongoDatabase = mongoClient[database_name]
    mongoCollection = mongoDatabase[collection_name]

    info_logger.info(f"loading: { len(rows) } rows to mongo")

    if rows:
        mongoCollection.insert_many(rows)

def main(CTX):
    info_logger_config = CTX["log"]
    info_logger_config["filename"] = os.path.join(LOG_PATH, "mongo_loader")
    info_logger = initialize_info_logger(info_logger_config)
    info_logger.info(json.dumps(CTX))

    i = 0
    while True:
        i += 1
        try:

            for file in os.listdir(DATA_PATH):
                if file.endswith(".log"):
                    source = os.path.join(DATA_PATH, file)
                    destination = os.path.join(DATA_ARCHIVE_PATH, file)

                    #with open(source) as file_in:
                    #    rows = [json.loads(row) for row in file_in]

                    rows = []
                    with open(source) as file_in:
                        for row in file_in:
                            row = json.loads(row)

                            created_at = row["data"].get("created_at")
                            if created_at:
                                row["data"]["created_at"] = datetime.datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%S.%fZ")

                            rows.append(row)

                    push_rows(CTX, rows)

                    info_logger.info(f"Archiving: {source} To: {destination}")
                    shutil.move(source, destination)

        except Exception as err:
            info_logger.error("%s: %s", i, err)
            print("%s: %s", i, err)

        time.sleep(1*60)

if __name__ == "__main__":
    with open(os.environ["STACKS_CONFIG"]) as file_in:
        CTX = json.load(file_in)
    main(CTX)
