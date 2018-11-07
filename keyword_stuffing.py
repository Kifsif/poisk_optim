"""
Сначала войти в Firefox с профилем firefox -p, залогиниться в Арсенкина.
"""
from selenium.common.exceptions import TimeoutException, UnexpectedAlertPresentException, StaleElementReferenceException
from general.general import get_region_name, write_phrase_to_log, \
    get_full_path_to_project_dir, get_project_paths, clear_files, \
    get_list
from selenium.common.exceptions import NoSuchElementException
from config import WRITE_ENCODING, READ_ENCODING
import os
from time import sleep
from selenium.webdriver.common.keys import Keys

from drv.drv import get_firefox_with_profile
from selenium.webdriver.support.ui import Select
import datetime
from time import strftime
from itertools import chain

####
REGION = ""
SITE = ""


ARSENKIN_TOOL_URL = "https://arsenkin.ru/tools/filter/"
SIZE_OF_CHUNK = 10
PROJECT_NAME = "KeywordStuffing"
INIT_DIR = get_project_paths(PROJECT_NAME)[1]
LOG_DIR = get_project_paths(PROJECT_NAME)[2]
LOG_FILE = ""


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
# from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.wait import WebDriverWait
def get_results(drv):

    try:
        table_element = WebDriverWait(drv, 60).until(EC.presence_of_element_located((By.TAG_NAME, "tbody")))
    except TimeoutException as e:
        raise TimeoutException('Timeout exception')
    except UnexpectedAlertPresentException as e:
        raise UnexpectedAlertPresentException("Возможная причина - исчерпание лимиты у Арсенкина") # Это исключение мы нигде более не ловим. Просто сообщаем причину.

    sleep(2) # Следующий блок вызывал исключение. Т.е. таблица, вроде, есть, а элент th  в ней отсутствует. Поэтому добавлен слип.

    try:
        drv.find_element_by_xpath(
            "//th[text()='Релевантный URL в выдаче по запросу']")  # Проверяем, что данные, действительно, выведены. Одной проверки наличия таблицы недостаточно - будут пропуски ключей.
    except NoSuchElementException as e:
        raise NoSuchElementException(str(e))

    try:
        table_html = table_element.get_attribute("innerHTML")
    except StaleElementReferenceException:
        raise StaleElementReferenceException("StaleElementReferenceException")

    return table_html


def handle_chunks(drv, phrases):
    chunks = list(get_chunks_generator(phrases))


    chunk_counter = 0 # Нужен только для отладки.
    while chunks:
        chunk = chunks.pop(0)
        textarea = fill_phrases(drv, chunk)

        successful = False
        write_phrase_to_log('<tr><th>{}</th></tr>'.format(chunk_counter), "a", WRITE_ENCODING, LOG_FILE)
        while not successful:
            submit_button_click(drv)
            try:
                table_html = get_results(drv)
            except TimeoutException as e:
                print(e)
                continue # Repeat Submit button click. We skip this iteration, and "successful = False".
            except StaleElementReferenceException as e:
                print(e)
                continue # Repeat Submit button click. We skip this iteration, and "successful = False".
            except UnexpectedAlertPresentException as e:
                # Кончились лимиты. Запишем недопарсенное в файл.
                chunks.append(chunk)
                tmp_chunks = list(chain(*chunks))
                chunks_as_str = "\n".join(tmp_chunks)
                remainder = os.path.join(LOG_DIR, "future.txt")
                write_phrase_to_log(chunks_as_str, "w", WRITE_ENCODING, remainder)
                drv.quit()
                quit()
            except NoSuchElementException as e:
                print(e)
                continue

            write_phrase_to_log(table_html, "a", WRITE_ENCODING, LOG_FILE)
            successful = True

        chunk_counter += 1

        try:
            textarea.clear()
        except NoSuchElementException as e: # Один раз такое исключение встретилось. Если еще раз встретится, попробовать отдебажить.
            textarea = drv.find_element_by_tag_name("textarea")
            textarea.clear()
            print(e)

    print("Counter {}".format(chunk_counter))

import time

def init_arsenkin_tool(drv):
    """
    Загрузить страницу с инструментом, обозначить регион и сайт.
    """

    drv.get(ARSENKIN_TOOL_URL)
    url_element = drv.find_element_by_name("url")
    url_element.send_keys(SITE)

    region_element = WebDriverWait(drv, 10).until(EC.element_to_be_clickable((By.XPATH, "//select[@name='city']")))

    # Классы при просмотре через Inspect element и view page source отличаются.
    # Inspect element показывает, что прсутствует некий класс select2-hidden-accessible.
    # Удалим его. И select сразу станет видимым.
    drv.execute_script('arguments[0].classList.remove("select2-hidden-accessible");', region_element)

    region_element = Select(region_element)
    region_element.select_by_value(REGION)


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

def init(content_of_init_file):
    """
    Задать регион и сайт
    """
    global REGION
    global SITE
    global LOG_FILE

    SITE = content_of_init_file[0]

    assert ".ru" in SITE

    REGION = content_of_init_file[1]

    assert REGION.isdigit()

    LOG_FILE = os.path.join(LOG_DIR, "{}_{}_{}_{}.html".format(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S"),
                                                               SITE,
                                                               get_region_name(REGION)[0],
                                                               get_region_name(REGION)[1]))


def keyword_stuffing():
    content_of_init_file = get_list(os.path.join(INIT_DIR, "init.txt"), READ_ENCODING)
    init(content_of_init_file)
    phrases = content_of_init_file[2:]
    parse_all(phrases)

