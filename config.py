from general.general import get_list
import os
import yaml

# General
all_settings = yaml.load(open("/home/michael/Documents/PoiskOptim/config.yml", "r"))
GENERAL_PATH = all_settings["paths"]["general_path"]


##########
# Encoding
READ_ENCODING = 'utf-8'
WRITE_ENCODING = 'utf-8'

##################
# Selenium drivers
IMPLICIT_WAIT_PERIOD = 14 # секунд.
EXPLICIT_WAIT_PERIOD = 12 # секунд.
#########################
# Firefox profile

# You may need to organize a Firefox profile.
# In the terminal type firefox -p
# Go to your page, cookies will be saved to the profile.

USE_FIREFOX_PROFILE = True
FIREFOX_PROFILE = '/home/michael/.mozilla/firefox/43w7gnt9.parsing' # cd ~/.mozilla/firefox
FIREFOX_WITH_IMG = False
                                                                    # ls -d $PWD/*
#########################
# Yandex Region

# Обязательно строкой, а не цифрой!
# https://tech.yandex.ru/xml/doc/dg/reference/regions-docpage/
YANDEX_REGION = '213' # С областью.


##########################
# Proxy

USE_PROXY = all_settings["proxies"]["use_garbage_proxies"]
GARBAGE_PROXIES = all_settings["garbage_proxies"]

# PRIVATE_PROXY = "91.193.110.57"
# PRIVATE_PROXY_LOGIN = "fzftRD"
# PRIVATE_PROXY_PASS = "ypN0Gj"



NUMBER_OF_ACCOUNTS = 100


NUMBER_OF_PHONES_PER_PAGE = 33

# YANDEX ACCOUNTS
PASSWORD = 'goskomstat'



