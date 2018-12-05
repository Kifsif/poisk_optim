from create_yandex_accounts import create_yandex_accounts
from test_proxies import test_proxies
from keyword_stuffing import keyword_stuffing
from add_ids import add_ids
from complex_analysis import complex_analysis
from parse_megaindex import parse_megaindex
from combine import combine

funcs = {"1":create_yandex_accounts,
         "2": test_proxies,
         "3": keyword_stuffing,
         "4": complex_analysis,
         "5": parse_megaindex,
         "6": combine
         }


choice = input("""1. Создать аккаунты яндекса.
2. Тест прокси.
3. Переоптимизация.
4. Комплексный анализ.
5. Парсим Мегаиндекс.
6. Комбинируем.
Что делаем: """)

funcs[choice]()

