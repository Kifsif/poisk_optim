from selenium import webdriver
from config import FIREFOX_PROFILE, GARBAGE_PROXY_LIST, IMPLISIT_WAIT_PERIOD, USE_FIREFOX_PROFILE, USE_PROXY
from copy import deepcopy
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver import Chrome
from copy import deepcopy
from selenium import webdriver
import os


def get_firefox_with_profile():
    # You may need to organize a Firefox profile.
    # In the terminal type firefox -p
    # Go to your page, cookies will be saved to the profile.


    if USE_FIREFOX_PROFILE:
        firefox_profile = webdriver.FirefoxProfile(FIREFOX_PROFILE)

    # firefox_profile.set_preference('permissions.default.image', 2) # Without images.
    # firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', False) # Without flash.

    return webdriver.Firefox(firefox_profile)
















tmp_proxy_list = []


PROXY_BLACK_SET = set()

def send_proxy_to_black_set(a_proxy):
    global PROXY_BLACK_LIST
    PROXY_BLACK_SET.add(a_proxy)

def get_proxy_list():
    proxy_list = GARBAGE_PROXY_LIST.split()
    proxy_set = set(proxy_list)
    tmp_proxy_list = list(proxy_set)
    return tmp_proxy_list


def get_proxy():
    global tmp_proxy_list
    try:
        a_proxy = tmp_proxy_list.pop()
    except IndexError:
        tmp_proxy_list = get_proxy_list()
        a_proxy = tmp_proxy_list.pop()

    if a_proxy in PROXY_BLACK_SET:
        get_proxy()

    return a_proxy


chrome_options = webdriver.ChromeOptions()



def get_chrome(a_proxy=None):
    """
    Получить вебдрайвер Хром.

    :param a_proxy: Иногда удобно использовать этот параметр. Например, при проверке прокси.
    :return:
    """
    if USE_PROXY and (a_proxy == None):
        # Если параметр a_proxy не задан, но надо использовать прокси, то получим прокси.
        a_proxy = get_proxy()

    desired_capabilities = DesiredCapabilities.CHROME.copy()

    if a_proxy:
        desired_capabilities["proxy"] = {'proxyType': 'MANUAL',
                                         'httpProxy': a_proxy, 'autodetect': False}

    chrome_options.add_argument('--proxy-server={}'.format(a_proxy))
    driver = Chrome(desired_capabilities=desired_capabilities)
    driver.implicitly_wait(IMPLISIT_WAIT_PERIOD)

    return driver











#
#
# def get_chrome():
#     # Pure means without a profile.
#
#     chromeOptions = webdriver.ChromeOptions()
#     prefs = {"profile.managed_default_content_settings.images": 2} # Without images.
#     chromeOptions.add_experimental_option("prefs", prefs)
#
#     driver = webdriver.Chrome(chrome_options=chromeOptions)
#
#     return driver
