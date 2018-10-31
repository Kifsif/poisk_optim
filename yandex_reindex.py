"""
На первой строке логин.
На второй строке пароль.
На третьей строке дневной лимит переобхода.
"""
from general.general import get_project_paths
import os

WEBMASTER_URL = "https://webmaster.yandex.ru/"
LOGIN = ""
PASS = ""
BUNCH_SIZE = 0

PROJECT_NAME = "YandexReindex"
import datetime

LOG_DIR = get_project_paths(PROJECT_NAME)[2]
LOG_FILE = os.path.join(LOG_DIR, "{}_log.txt".format(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")))


def init():
    global LOGIN
    global PASS
    global BUNCH_SIZE
    pass


def yandex_reindex():
    init()
    print("Success")