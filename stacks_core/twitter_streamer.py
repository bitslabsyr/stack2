'''
'''
import os
import json
import logging
import logging.handlers
import time

import requests
import urllib3

LOG_PATH = "/var/stacks/logs"
DATA_PATH = "/var/stacks/data"
DATA_ARCHIVE_PATH = "/var/stacks/data_archive"

STREAM_API_URL = "https://api.twitter.com/2/tweets/search/stream"
STREAM_RULES_API_URL = STREAM_API_URL + "/rules"

REQUEST_WITH_RETRY = requests.Session()
REQUEST_WITH_RETRY.mount("https://", requests.adapters.HTTPAdapter(
    max_retries= urllib3.util.retry.Retry(
        total=5,
        backoff_factor=1,
        status_forcelist=[408, 409, 429, 500, 502, 503, 504]
    )
))

def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers

def get_rules(headers):
    response = requests.get(STREAM_RULES_API_URL, headers=headers)

    if response.status_code != 200:
        raise Exception("Cannot get rules (HTTP {}): {}".format(response.status_code, response.reason))

    return response.json()

def delete_rules(headers, rule_ids):
    if not rule_ids:
        return None

    payload = {"delete": {"ids": rule_ids}}
    response = requests.post(STREAM_RULES_API_URL, headers=headers, json=payload)

    if response.status_code != 200:
        raise Exception("Cannot delete rules (HTTP {}): {}".format(response.status_code, response.reason))

    return response.json()

def set_rules(headers, query_rules):
    query_rules
    payload = {"add": query_rules}
    response = requests.post(STREAM_RULES_API_URL, headers=headers, json=payload)

    if response.status_code != 201:
        raise Exception("Cannot add rules (HTTP {}): {}".format(response.status_code, response.reason))

    return response.json()

def get_stream(headers, query_parameters):

    query_parameters = {
        key: ",".join(value)
        for key, value
        in query_parameters.items()
    }

    data_logger = logging.getLogger('Data_Logger')
    with REQUEST_WITH_RETRY.get(STREAM_API_URL, headers=headers, params=query_parameters, stream=True) as response:
        if not response.ok:
            raise Exception("Cannot get stream (HTTP {}). {}".format(response.status_code, response.reason))

        for response_line in response.iter_lines():
            if not response_line:
                continue
            data_logger.info(response_line.decode())

def initialize_info_logger(log_config):
    formatter = logging.Formatter(fmt='%(asctime)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    rotating_handler = logging.handlers.TimedRotatingFileHandler(**log_config)
    rotating_handler.suffix = "%Y-%m-%d_%H-%M-%S.log"
    rotating_handler.setFormatter(formatter)
    info_logger = logging.getLogger('Info_Logger')
    info_logger.setLevel(logging.INFO)
    info_logger.addHandler(rotating_handler)
    return info_logger

def initialize_data_logger(log_config):
    rotating_handler = logging.handlers.TimedRotatingFileHandler(**log_config)
    rotating_handler.suffix = "%Y-%m-%d_%H-%M-%S.log"
    data_logger = logging.getLogger('Data_Logger')
    data_logger.setLevel(logging.INFO)
    data_logger.addHandler(rotating_handler)
    return data_logger

def main(CTX):

    info_logger_config = CTX["log"]
    info_logger_config["filename"] = os.path.join(LOG_PATH, "twitter_streamer")
    info_logger = initialize_info_logger(info_logger_config)
    info_logger.info(json.dumps(CTX))

    data_logger_config = CTX["data"]
    data_logger_config["filename"] = os.path.join(DATA_PATH, "tweets.log")
    data_logger = initialize_data_logger(data_logger_config)

    headers = create_headers(CTX["twitter_bearer_token"])
    current_rules = get_rules(headers)
    current_rule_ids = [rule["id"] for rule in current_rules.get("data", {})]
    info_logger.info("Current_Rules:")
    info_logger.info(json.dumps(current_rules, indent=4, sort_keys=True))

    info_logger.info("Current Rule Ids:")
    info_logger.info(json.dumps(current_rule_ids, indent=4, sort_keys=True))

    deleted_rules = delete_rules(headers, current_rule_ids)
    info_logger.info("Deleted_Rules:")
    info_logger.info(json.dumps(deleted_rules, indent=4, sort_keys=True))

    current_rules = set_rules(headers, CTX["query_rules"])
    info_logger.info("Current_Rules:")
    info_logger.info(json.dumps(current_rules, indent=4, sort_keys=True))

    i = 0
    while True:
        i += 1
        try:
            get_stream(headers, CTX["query_parameters"])
        except Exception as err:
            info_logger.error("%s: %s", i, err)
            time.sleep(5*60)

if __name__ == "__main__":
    with open(os.environ["STACKS_CONFIG"]) as file_in:
        CTX = json.load(file_in)
    main(CTX)
