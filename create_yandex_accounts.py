"""
firefox -p
Зайти на smsreceivefree.com и пройти капчу.

Если попросит регистрацию, зайти в tmpgmv,
найти отмеченное флажком письмо от me+activate@smsreceivefree.com и нажать Access Dashboard.
"""




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
from config import EXPLICIT_WAIT_PERIOD
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from urllib3.exceptions import MaxRetryError
import re

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

    chrome.quit()

    return True



def send_all_codes_to_stale(sms_texts):
    global stale_codes
    for sms_text in sms_texts:
        stale_codes.add(sms_text)


def get_confirmation_code(phone_number_without_plus):
    firefox.get("https://smsreceivefree.com/info/{}/".format(phone_number_without_plus))

    try:
        element_with_code = WebDriverWait(firefox, EXPLICIT_WAIT_PERIOD).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'подтвержд')]")))
    except TimeoutException:
        return False
        firefox.quit()

    received_text = element_with_code.text

    confirmation_code = re.search(r"(\d+)", received_text).group(0)

    # sleep(2)


    return confirmation_code

# def check_limit():
#     try:
#         check_limit_reached(chrome, firefox, phone_number_without_plus)
#     except PnoneLimitExceededException:
#         return False
#
#     phone_url = 'https://smsreceivefree.com/info/{}/'
#     firefox.get(phone_url.format(phone_number_without_plus))
#
#     probable_code = sms_texts[0]
#
#     global stale_codes
#
#
#     if probable_code in stale_codes:
#         if counter == 3:
#             return False
#
#         send_all_codes_to_stale(sms_texts)
#
#         sleep(3)
#         counter += 1
#         try_code(chrome, firefox, phone_number_without_plus, counter)
#
#     else:
#         stale_codes.add(probable_code)
#
#     phone_code_element = chrome.find_element_by_id("phoneCode")
#     phone_code_element.send_keys(probable_code)
#
#     buttons = chrome.find_elements_by_tag_name("button")
#     confirm_button = buttons[1]
#     confirm_button.click()
#     sleep(4)
#
#     try:
#         elements_with_code = firefox.find_elements_by_xpath("//*[contains(text(), 'неправильн')]") # Сообщение "Неправильный код, попробуйте ещё раз"
#     except NoSuchElementException:
#         pass
#     register_button = buttons[2]
#     register_button.click()

def try_code(confirmation_code):
    input_confirmation_code_element = chrome.find_element_by_id("phoneCode")
    input_confirmation_code_element.send_keys(confirmation_code)

    from selenium.webdriver import ActionChains
    actions = ActionChains(chrome)
    register_button= chrome.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/main/div/div/div/form/div[4]/button')
    actions.move_to_element(register_button).click().perform();
    # register_button.click()
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

        firefox = get_firefox_with_profile()


        buttons = chrome.find_elements_by_tag_name('button')
        button_get_code = buttons[1] # Кнопка "Получить код"
        button_get_code.click()

        limit_for_phone_reached = check_limit_reached(phone_number_without_plus)

        if limit_for_phone_reached:
            current_phone = None # Больше не использовать текущий телефонный номер.
            chrome.quit()
            continue

        confirmation_code = get_confirmation_code(phone_number_without_plus)

        success = try_code(confirmation_code)

        if not success:
            continue

        print("Success: {}".format(login))
        chrome.quit()




def create_yandex_accounts():
    if not all_phones:
        fill_all_phone_urls()

    open_yandex_to_register_acc()
    firefox.quit()
