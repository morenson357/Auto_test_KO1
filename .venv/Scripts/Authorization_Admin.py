from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from dir.site_info_dv import auth_site, main_menu
#from dir.auth_date import login, passwd

def authorization_docsvision_admin(browser: webdriver.Chrome, login:str, passwd:str) -> bool:
    """Авторизует администратора в DocsVision и проверяет успешный вход."""
    try:
        browser.get(auth_site)

        # Ввод логина
        browser.find_element(By.CLASS_NAME, "login-input__input").send_keys(login)

        # Ввод пароля
        browser.find_element(By.NAME, "Пароль").send_keys(passwd)

        # Клик по кнопке входа
        browser.find_element(By.CLASS_NAME, "login-button").click()

        # Проверка загрузки основного меню
        browser.find_element(By.XPATH, main_menu)

        print("Авторизация пройдена успешно - ОК")
        return True
    except:
        print("Ошибка авторизации - ERROR")
        return False



