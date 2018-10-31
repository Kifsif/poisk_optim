from create_yandex_accounts import create_yandex_accounts
from test_proxies import test_proxies
from keyword_stuffing import keyword_stuffing
from yandex_reindex import yandex_reindex

funcs = {"1":create_yandex_accounts,
         "2": test_proxies,
         "3": keyword_stuffing,
         "4": yandex_reindex}


choice = input("""1. Создать аккаунты яндекса.
2. Тест прокси.
3. Переоптимизация.
4. Переобход страниц Yandex.
What to do: """)

funcs[choice]()

