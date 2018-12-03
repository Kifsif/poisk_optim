# Сначала профилем Firefox выполните вход в Мегаиндекс.
# Емейлы: petrovinwoderland@gmail.com, artlebedev@tutanota.com
# Пароль: $7iejdlF40)

import glob
from general.general import get_project_paths
from selenium.common.exceptions import NoSuchElementException
from drv.drv import get_firefox_with_profile
import os
from general.general import get_list, write_phrase_to_log
from config import READ_ENCODING, WRITE_ENCODING
import sys
from time import sleep

PROJECT_NAME = "ParseMegaindex"
DOWNLOAD_DIR = "/home/michael/Downloads"

INIT_DIR = get_project_paths(PROJECT_NAME)[1]
LOG_DIR = get_project_paths(PROJECT_NAME)[2]
LOG_FILE = os.path.join(LOG_DIR, "log.txt")

MEGAINDEX_LOGIN_URL = 'https://ru.megaindex.com/auth'
MEGAINDEX_KEYWORDS_URL = 'https://ru.megaindex.com/a/urlkeywords'

def init_urls_to_parse():
    urls_file = os.path.join(INIT_DIR, "urls.csv")
    urls = get_list(urls_file, READ_ENCODING)
    return urls

def count_files():
    files_mask = os.path.join(DOWNLOAD_DIR, "*.csv")
    arr = glob.glob(files_mask)
    return len(arr)

from general.general import get_current_date_time
def rename_downloaded_file():
    # Google Chrome перестает автоматически переименовывать скачанные файлы с одинаковым именем, если их более 100.
    # Поэтому каждый скачанный файлы надо переименовать и переместить в отдельную папку.
    old_name = "keywords.csv"
    file_mask = os.path.join(DOWNLOAD_DIR, old_name)
    file = glob.glob(file_mask)
    os.rename(os.path.join(DOWNLOAD_DIR,
              old_name),
              os.path.join(DOWNLOAD_DIR, "{}_keywords_{}.csv".format(PROJECT_NAME, get_current_date_time())))


def parse_url(driver, url):
    if not url:
        raise Exception("URL пустой")

    try:  # Транзакция
        driver.get(MEGAINDEX_KEYWORDS_URL)
        init_number_of_files = count_files()
        url_input = driver.find_element_by_xpath('//input[@name="url"]')
        url_input.clear()
        url_input.send_keys(url)

        search_button = driver.find_element_by_tag_name('button')  # Это кнопка поиска.
        search_button.click()

        nothing_found = None  # Элемент, соответствуюий тегу с текстом "Ничего не найдено".

        try:
            nothing_found = driver.find_element_by_xpath('//td[contains(text(), "Ничего не найдено")]')
        except NoSuchElementException:
            pass  # ничего не делаем.

        if nothing_found:
            write_phrase_to_log("{}DELIMITER {} ничего не найдено.".format(url, PROJECT_NAME), 'a', WRITE_ENCODING, LOG_FILE)
            return

        export_to_csv_button = driver.find_element_by_xpath('//input[@type="button"]')  # Кнопка экспорта в CSV.

        export_to_csv_button.click()

        confirm_button = driver.find_element_by_xpath('//span[text()="Скачать файл"]')
        confirm_button.click()

        while True:
            current_number_of_files = count_files()
            if current_number_of_files > init_number_of_files:
                rename_downloaded_file()
                break
            sleep(1)

        write_phrase_to_log("{}DELIMITER {} успешно.".format(url, PROJECT_NAME), 'a', WRITE_ENCODING, LOG_FILE)

    except Exception as e:
        print("В каталоге проекта должен быть каталог log")
        print(e)
        parse_url(driver, url)

def get_last_parsed_url():
    # В лог-файле все строки содержат комментарий, отделенный от url словом "DELIMITER".
    log = get_list(LOG_FILE, READ_ENCODING)
    last_line_in_log = log[-1].strip()
    delimter_position = last_line_in_log.index("DELIMITER")
    return last_line_in_log[:delimter_position]


def get_start_position_to_parse(urls):

    try:
        with open(LOG_FILE, mode='r', encoding=READ_ENCODING) as f:
            log = list(f)
    except FileNotFoundError:
        return 0

    last_line_in_log = get_last_parsed_url()
    last_url_ind = len(urls) - 1

    index_of_already_parsed_url = urls.index(last_line_in_log)

    if index_of_already_parsed_url == last_url_ind:
        exit

    next_url = index_of_already_parsed_url + 1

    return next_url


def parse_all_urls(driver, urls):
    while True:
        parse_from_index = get_start_position_to_parse(urls)
        try:
            url = urls[parse_from_index]
        except IndexError:
            sys.exit()

        parse_url(driver, url)



def parse_megaindex():
    driver = get_firefox_with_profile()
    urls = init_urls_to_parse()
    parse_all_urls(driver, urls)
    driver.quit()