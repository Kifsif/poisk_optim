from selenium.common.exceptions import NoSuchElementException
from drv.drv import get_proxy_list, get_chrome, get_proxy


init_proxy_list = get_proxy_list()
good_proxy_list = []
bad_proxy_list = []

def test_proxies():
    for i in range( len(init_proxy_list)):
        a_proxy = get_proxy()
        driver = get_chrome(a_proxy)
        driver.get("http://ip-api.com/")

        try:
            element = driver.find_element_by_id("qr")
        except NoSuchElementException:
            print("qr не найден")
            bad_proxy_list.append(a_proxy)
            driver.quit()
            continue

        driver.quit()
        good_proxy_list.append(a_proxy)

    print("Хорошие прокси:" + '\n'.join(good_proxy_list))
    print("Плохие прокси:" + '\n'.join(bad_proxy_list))

if __name__ == "__main__":
    test_proxies()