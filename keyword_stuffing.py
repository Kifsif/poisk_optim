"""
Сначала войти в Firefox с профилем firefox -p, залогиниться в Арсенкина.
"""

from general.general import get_region_name, write_phrase_to_log, \
    get_full_path_to_project_dir, get_project_paths, clear_files, \
    get_list

from config import WRITE_ENCODING, READ_ENCODING
import os
from time import sleep
from selenium.webdriver.common.keys import Keys

from drv.drv import get_firefox_with_profile
from selenium.webdriver.support.ui import Select

####
REGION = '213' # Строкой
SITE = "https://ritm-it.ru"


ARSENKIN_TOOL_URL = "https://arsenkin.ru/tools/filter/"
SIZE_OF_CHUNK = 10
PROJECT_NAME = "KeywordStuffing"
INIT_DIR = get_project_paths(PROJECT_NAME)[1]
LOG_DIR = get_project_paths(PROJECT_NAME)[2]
LOG_FILE = os.path.join(LOG_DIR, "{}_{}.html".format(get_region_name(REGION)[0],
                                                    get_region_name(REGION)[1]))
def get_phrases():
    pass


def get_chunks_generator(phrases):
    for i in range(0, len(phrases), SIZE_OF_CHUNK):
        yield phrases[i:i + SIZE_OF_CHUNK]

def fill_phrases(drv, chunk):
    str_phrases = "\n".join(chunk)
    textarea = drv.find_element_by_tag_name("textarea")
    textarea.send_keys(str_phrases)
    return textarea

def submit_button_click(drv):
    submit_button = drv.find_element_by_xpath("//*[contains(text(), 'Проверить')]")
    submit_button.click()

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
def get_results(drv):
    table_element = WebDriverWait(drv, 60).until(EC.presence_of_element_located((By.TAG_NAME, "tbody")))
    table_html = table_element.get_attribute("innerHTML")
    write_phrase_to_log(table_html, "a", WRITE_ENCODING, LOG_FILE)

def handle_chunks(drv, phrases):
    chunks = list(get_chunks_generator(phrases))
    for chunk in chunks:
        textarea = fill_phrases(drv, chunk)
        submit_button_click(drv)
        get_results(drv)
        textarea.clear()

def init_arsenkin_tool(drv):
    """
    Загрузить страницу с инструментом, обозначить регион и сайт.
    """

    drv.get(ARSENKIN_TOOL_URL)
    url = drv.find_element_by_name("url")
    url.send_keys(SITE)


def write_log_header():
    html = """
    <html>
            <head>
                <meta charset="utf-8">
            </head>
                <body>
            <table>			
    """
    write_phrase_to_log(html, "a", WRITE_ENCODING, LOG_FILE)

def write_log_footer():
    write_phrase_to_log("</table></body></html>", "a", WRITE_ENCODING, LOG_FILE)

def parse_all(phrases):
    drv = get_firefox_with_profile()
    init_arsenkin_tool(drv)
    write_log_header()
    handle_chunks(drv, phrases)
    write_log_footer()
    drv.quit()

def keyword_stuffing():
    clear_files(LOG_DIR)
    phrases = get_list(os.path.join(INIT_DIR, "init.txt"), READ_ENCODING)
    parse_all(phrases)

