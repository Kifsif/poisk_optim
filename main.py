from create_yandex_accounts import create_yandex_accounts
from test_proxies import test_proxies
from keyword_stuffing import keyword_stuffing
from add_ids import add_ids

funcs = {"1":create_yandex_accounts,
         "2": test_proxies,
         "3": keyword_stuffing,
         "4": add_ids,
         }


choice = input("""1. Создать аккаунты яндекса.
2. Тест прокси.
3. Переоптимизация.
4. Добавить id.
Что делаем: """)

funcs[choice]()

