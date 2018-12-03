from general.general import get_project_paths
from general.general import get_list
import os
from config import READ_ENCODING
import yaml

PROJECT_NAME = "ComplexAnalysis"

INIT_DIR = get_project_paths(PROJECT_NAME)[1]
LOG_DIR = get_project_paths(PROJECT_NAME)[2]
KEYS_FILE = "keys.txt"

GOOGLE = "https://google.com"
YANDEX = "https://ya.ru"
settings = yaml.load(open(os.path.join(INIT_DIR, "init.yml"), "r"))
ANALYZE_GOOGLE = settings["google"]
ANALYZE_YANDEX = settings["yandex"]

KEYS = []

def initialize():
    keys = get_list(os.path.join(INIT_DIR, KEYS_FILE), READ_ENCODING)
    pass

def complex_analysis():
    initialize()

