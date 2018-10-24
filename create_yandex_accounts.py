"""
firefox -p
Зайти на smsreceivefree.com и пройти капчу.

Если попросит регистрацию, зайти в tmpgmv,
найти отмеченное флажком письмо от me+activate@smsreceivefree.com и нажать Access Dashboard.
"""



from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Firefox
from selenium.webdriver.common.keys import Keys
from drv.drv import get_firefox_with_profile, get_chrome, send_proxy_to_black_set
from drv.drv import get_chrome
from config import NUMBER_OF_PHONES_PER_PAGE, PASSWORD
from random import choice
import string
from uuid import uuid4
from time import sleep
from config import EXPLICIT_WAIT_PERIOD, WRITE_ENCODING
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from urllib3.exceptions import MaxRetryError
import re
from general.general import get_project_paths, write_phrase_to_log
import os

PROJECT_NAME = "CreateYandexAccounts"
import datetime

LOG_DIR = get_project_paths(PROJECT_NAME)[2]
LOG_FILE = os.path.join(LOG_DIR, "{}_log.txt".format(datetime.datetime.now().strftime("%Y-%m-%d")))

stale_phones = set()
stale_codes = set()
all_phones = []
chrome = None
firefox = None

def fill_all_phone_urls():
    global all_phones
    global firefox

    firefox = get_firefox_with_profile()
    url_pattern = "https://smsreceivefree.com/country/{}"

    for country in ["canada", "usa", ]:
        firefox.get(url_pattern.format(country))
        all_number_elements = firefox.find_elements_by_class_name("numbutton")
        all_phones += [element.text.split(maxsplit=1)[0] for element in all_number_elements]

    firefox.quit()



def get_random_string(string_length):
    return "".join(choice(string.ascii_letters) for _ in range(string_length))

def generate_unique_login():
    max_login_length = 30

    random_letter = get_random_string(1)
    unique_combination = random_letter + str(uuid4()).replace("-", "") # Логин Яндекса не должен начинаться с цифры.

    unique_combination = unique_combination[:max_login_length]

    return unique_combination





class PnoneLimitExceededException(Exception):

    def __init__(self,*args,**kwargs):
        Exception.__init__(self,"Превышен лимит отправляемых сообщений, попробуйте позже.")



def check_limit_reached(phone_number_without_plus):
    # global stale_phones
    global all_phones
    try:
        elements_with_code = WebDriverWait(chrome, EXPLICIT_WAIT_PERIOD).until(
           EC.presence_of_element_located((By.CLASS_NAME,"error-message")))  # Превышен лимит отправляемых сообщений, попробуйте позже.
    except TimeoutException:
        return False # Яндекс не ругался. Т.е. лимит для телефона не превышен.
    except MaxRetryError:
        # Превышен лимит отправляемых сообщений, попробуйте позже.
        sleep(3)
        check_limit_reached(phone_number_without_plus)

    # stale_phones.add(phone_number_without_plus)
    print("Лимит для телефона превышен.")
    chrome.quit()

    return True



def send_all_codes_to_stale(sms_texts):
    global stale_codes
    for sms_text in sms_texts:
        stale_codes.add(sms_text)


def get_confirmation_code(phone_number_without_plus):
    firefox = get_firefox_with_profile()
    firefox.get("https://smsreceivefree.com/info/{}/".format(phone_number_without_plus))

    try:
        element_with_code = WebDriverWait(firefox, EXPLICIT_WAIT_PERIOD).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'подтвержд')]")))
    except TimeoutException:
        firefox.quit()
        return False

    received_text = element_with_code.text

    confirmation_code = re.search(r"(\d+)", received_text).group(0)
    firefox.quit()

    # sleep(2)


    return confirmation_code

def get_code_button():
    try:
        get_text_button = chrome.find_element_by_xpath("//*[@id='root']/div/div[2]/div/main/div/div/div/form/div[3]/div/div[2]/div/div/button")
    except NoSuchElementException:
        pass
    return get_text_button


def try_code(confirmation_code):
    input_confirmation_code_element = chrome.find_element_by_id("phoneCode")
    input_confirmation_code_element.send_keys(confirmation_code)
    sleep(1)


    try:
        confirm_button = chrome.find_element_by_xpath("//*[@id='root']/div/div[2]/div/main/div/div/div/form/div[3]/div/div[2]/div/div[2]/div[2]/button")
    except NoSuchElementException:
        pass # Ничего не делаем. Так и должно быть.

    try:
        confirm_button.click()
    except UnboundLocalError:
        pass  # Ничего не делаем. Так и должно быть.


    actions = ActionChains(chrome)

    register_button=chrome.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/main/div/div/div/form/div[4]/button')
    actions.move_to_element(register_button).click().perform();

    # Проверим, что, действительно, перешли на страницу управления созданным аккаунтом.
    try:
        acc_management_link = chrome.find_element_by_link_text("Управление аккаунтом")
    except NoSuchElementException:
        return False

    return True




def open_yandex_to_register_acc():
    global chrome

    current_phone = None
    while all_phones:
        chrome = get_chrome()
        url = "https://passport.yandex.ru/registration"
        chrome.get(url)
        try:
            first_name_element = chrome.find_element_by_id("firstname")
        except NoSuchElementException:
            send_proxy_to_black_set()

        first_name_element.send_keys(get_random_string(string_length=10))

        last_name_element = chrome.find_element_by_id("lastname")
        last_name_element.send_keys(get_random_string(string_length=10))

        login_element = chrome.find_element_by_id("login")
        login = generate_unique_login()
        login_element.send_keys(login)

        password_element = chrome.find_element_by_id("password")
        password_element.send_keys(PASSWORD)

        password_confirm_element = chrome.find_element_by_id("password_confirm")
        password_confirm_element.send_keys(PASSWORD)

        phone_element = chrome.find_element_by_id("phone")

        phone_number = current_phone or all_phones.pop()
        phone_element.send_keys(phone_number)


        phone_number_without_plus = phone_number[1:]

        # firefox = get_firefox_with_profile()


        buttons = chrome.find_elements_by_tag_name('button')
        # button_get_code = buttons[1] # Кнопка "Получить код"
        button_get_code = get_code_button()

        button_get_code.click()

        limit_for_phone_reached = check_limit_reached(phone_number_without_plus)

        if limit_for_phone_reached:
            current_phone = None # Больше не использовать текущий телефонный номер.
            chrome.quit()
            continue

        confirmation_code = get_confirmation_code(phone_number_without_plus)

        success = try_code(confirmation_code)

        if not success:
            chrome.quit()
            continue

        print("Success: {}".format(login))
        write_phrase_to_log(login, "a", WRITE_ENCODING, LOG_FILE)
        chrome.quit()




def create_yandex_accounts():
    if not all_phones:
        fill_all_phone_urls()

    open_yandex_to_register_acc()
    firefox.quit()
