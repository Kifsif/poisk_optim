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

USE_PROXY = True
PRIVATE_PROXY = "91.193.110.57"
PRIVATE_PROXY_LOGIN = "fzftRD"
PRIVATE_PROXY_PASS = "ypN0Gj"


NUMBER_OF_ACCOUNTS = 100

# Задавать только Http прокси.
GARBAGE_PROXY_LIST = """
37.228.89.215:80
91.122.47.157:8081
185.22.174.65:1448
193.109.161.105:57896
91.235.247.252:8081
134.249.121.156:48022
77.238.234.149:8081
145.239.81.69:8080
95.67.41.171:38463
195.208.172.70:8080
82.114.241.138:8080
94.242.58.14:10010
178.162.102.173:8081
94.45.131.213:32070"""

NUMBER_OF_PHONES_PER_PAGE = 33

# YANDEX ACCOUNTS
PASSWORD = 'goskomstat'