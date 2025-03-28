from itertools import count
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from action_report import transition_to_report_designer, transition_to_setting_reports, click_to_create_report
from selenium.webdriver import ActionChains
from dir.attributes_report import attributes_report_dictionary, attributes_report_dictionary_access
from selenium.common.exceptions import NoSuchElementException
from Authorization_Admin import authorization_docsvision_admin
from dir.auth_date import login, passwd


options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument("--ignore-certificate-errors")
options.add_argument("--allow-running-insecure-content")
options.add_argument("--disable-web-security")

with webdriver.Chrome() as browser:
    browser.implicitly_wait(10)
    try:

        # Проверка авторизации пользователя.
        if (authorization_docsvision_admin(browser, login, passwd) == False):
            quit()
        # Переход в модуль конструктор отчетов.
        transition_to_report_designer(browser)

        # Переход в настройки отчетов.
        transition_to_setting_reports(browser)

        #Нажатие на кнопку создания отчета.
        click_to_create_report(browser)

        #Функция проверки присутствия элемента на разметке.
        def check_exists_by_xpath(xpath):
            try:
                browser.find_element(By.XPATH, xpath)
            except NoSuchElementException:
                return False
            return True

        #Добавление строк данных отчета и параметров.
        add_rows = browser.find_elements(By.XPATH, "//button[@data-button-name='add-row']")
        for i in add_rows:
            i.click()

        #Проверка присутствия элементов и вкладки Основная информация.
        errors = []

        browser.find_element(By.XPATH, "//li[@data-tipso-text='Основная информация']")
        print("Идёт проверка элементов Основная информация...")
        for key, value in attributes_report_dictionary.items():
            if (check_exists_by_xpath(value) == False):
                errors.append('Элемент управления ' + key +' не найден')

        #Проверка присутствия элементов на вкладке Условия доступности.
        access = browser.find_element(By.XPATH, "//li[@data-tipso-text='Условия доступности']")
        access.click()
        print("Идёт проверка элементов Условия доступности...")
        for key, value in attributes_report_dictionary_access.items():
            if (check_exists_by_xpath(value) == False):
                errors.append('Элемент управления ' + key + ' не найден')

        browser.find_element(By.XPATH, "//div[text() = 'Отменить']/ancestor::button[@tabindex='-1']").click()
        browser.find_element(By.XPATH, "//button[@datatestid='button-ok']").click()
        #Расчет результата выполнения кейса.
        if (len(errors) == 0):
            print("\nАвтотест методики проверки №2.1 завершен - Успешно")
        else:
            print("\nАвтотест методики проверки №2.1 завершен с Ошибкой:")
            for error in errors:
                print(error)
    except Exception as ex:
        print(f"Произошла ошибка: {str(ex)}")
