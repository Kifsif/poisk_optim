from create_yandex_accounts import create_yandex_accounts
from test_proxies import test_proxies
from keyword_stuffing import keyword_stuffing

funcs = {"1":create_yandex_accounts,
         "2": test_proxies,
         "3": keyword_stuffing}

choice = input("""1. Создать аккаунты яндекса.
2. Тест прокси.
3. Переоптимизация.
What to do: """)

funcs[choice]()

