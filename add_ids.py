from general.general import get_project_paths
import datetime
import os

PROJECT_NAME = "AddIds"

INIT_DIR = ""
LOG_DIR = ""


def initialize_globals():
    global INIT_DIR
    global LOG_DIR
    global LOG_FILE

    PROJECT_PATH, INIT_DIR, LOG_DIR, _ = get_project_paths(PROJECT_NAME)
    LOG_FILE = os.path.join(LOG_DIR, "{}_log.txt".format(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")))

def handle_file():
    pass

def add_ids():
    initialize_globals()
    handle_file()
    pass