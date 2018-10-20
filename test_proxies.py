import os
from selenium.common.exceptions import NoSuchElementException
from drv.drv import send_proxy_to_black_set
from config import GARBAGE_PROXY_LIST
from drv.drv import get_proxy_list, get_chrome

init_proxy_list = get_proxy_list()

def test_proxies():
    for i in range( len(init_proxy_list)):
        driver = get_chrome()
        driver.get("http://ip-api.com/")

        try:
            element = driver.find_element_by_id("qr")
        except NoSuchElementException:
            print("qr не найден")
            continue

        element_text = element.text
        ip = element_text.split(",")


        driver.quit()
        print(ip)

if __name__ == "__main__":
    test_proxies()