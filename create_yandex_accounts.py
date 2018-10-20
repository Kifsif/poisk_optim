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



def check_limit_reached(chrome, firefox, phone_number_without_plus):
    global stale_phones
    try:
        elements_with_code = chrome.find_elements_by_xpath(
            "//*[contains(text(), 'Превышен')]")  # Превышен лимит отправляемых сообщений, попробуйте позже.
    except NoSuchElementException:
        pass # Do nothing.

    stale_phones.add(phone_number_without_plus)
    chrome.quit()
    firefox.quit()

    raise PnoneLimitExceededException()



def send_all_codes_to_stale(sms_texts):
    global stale_codes
    for sms_text in sms_texts:
        stale_codes.add(sms_text)


def try_code(chrome, firefox, phone_number_without_plus, counter=0):
    elements_with_code = firefox.find_elements_by_xpath("//*[contains(text(), 'подтвержд')]")
    sms_texts = [element.text.split(sep=".", maxsplit=1)[0][-6:] for element in elements_with_code]

    sleep(2)

    try:
        check_limit_reached(chrome, firefox, phone_number_without_plus)
    except PnoneLimitExceededException:
        return False

    phone_url = 'https://smsreceivefree.com/info/{}/'
    firefox.get(phone_url.format(phone_number_without_plus))

    probable_code = sms_texts[0]

    global stale_codes


    if probable_code in stale_codes:
        if counter == 3:
            return False

        send_all_codes_to_stale(sms_texts)

        sleep(3)
        counter += 1
        try_code(chrome, firefox, phone_number_without_plus, counter)

    else:
        stale_codes.add(probable_code)

    phone_code_element = chrome.find_element_by_id("phoneCode")
    phone_code_element.send_keys(probable_code)

    buttons = chrome.find_elements_by_tag_name("button")
    confirm_button = buttons[1]
    confirm_button.click()
    sleep(4)

    try:
        elements_with_code = firefox.find_elements_by_xpath("//*[contains(text(), 'неправильн')]") # Сообщение "Неправильный код, попробуйте ещё раз"
    except NoSuchElementException:
        pass
    register_button = buttons[2]
    register_button.click()

    return True


def open_yandex_to_register_acc(counter=0):
    global chrome

    if not all_phones:
        fill_all_phone_urls()

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

        phone_number = all_phones.pop()
        phone_element.send_keys(phone_number)


        phone_number_without_plus = phone_number[1:]

        firefox = get_firefox_with_profile()


        buttons = chrome.find_elements_by_tag_name('button')
        button_get_code = buttons[1] # Кнопка "Получить код"
        button_get_code.click()

        success = try_code(chrome, firefox, phone_number_without_plus)

        if success:
            print("Success: {}".format(login))
            chrome.quit()
            stale_phones.add(phone_number_without_plus)



def create_yandex_accounts():
    open_yandex_to_register_acc()
