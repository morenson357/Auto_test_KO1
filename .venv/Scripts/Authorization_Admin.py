import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from dir.site_info_dv import auth_site, main_menu
#from dir.auth_date import login, passwd
def check_exists_by_xpath(browser: webdriver.Chrome, xpath):
    try:
        elements = browser.find_elements(By.XPATH, xpath)
        return len(elements) > 0
    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}")
        return False
def authorization_docsvision_admin(browser: webdriver.Chrome, login:str, passwd:str) -> bool:
    """Авторизует администратора в DocsVision и проверяет успешный вход."""
    try:
        browser.get(auth_site)
        trust_button = "//button[@id = 'proceed-button']"
        if check_exists_by_xpath(browser, trust_button) == True:
            browser.find_element(By.XPATH, trust_button).click()

        time.sleep(1)
        remove_user = "//span[text() = 'Сменить пользователя']"
        if check_exists_by_xpath(browser, remove_user) == True:
            browser.find_element(By.XPATH, "//span[text() = 'Сменить пользователя']").click()
        # Ввод логина
        browser.find_element(By.XPATH, "//input[@name='Логин']").send_keys(login)

        # Ввод пароля
        browser.find_element(By.NAME, "Пароль").send_keys(passwd)

        # Клик по кнопке входа
        browser.find_element(By.CLASS_NAME, "login-button").click()
        time.sleep(10)
        # Проверка загрузки основного меню
        browser.find_element(By.XPATH, main_menu)

        print("Авторизация пройдена успешно - ОК")
        return True
    except:
        print("Ошибка авторизации - ERROR")
        return False





