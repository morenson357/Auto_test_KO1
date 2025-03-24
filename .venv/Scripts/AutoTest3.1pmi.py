from itertools import count
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from dir.site_info_dv import auth_site, report_site, main_menu
from selenium.webdriver import ActionChains
from dir.attributes_report import attributes_report_dictionary, parameters_report, attributes_connect
from selenium.common.exceptions import NoSuchElementException
from Authorization_Admin import authorization_docsvision_admin
from dir.auth_date import login, passwd
from action_report import transition_to_report_designer, transition_to_setting_reports, click_to_create_report, transition_to_report_list, delete_report, transition_to_connect, create_new_connect

options = webdriver.ChromeOptions()
options.add_argument('--headless')

with webdriver.Chrome() as browser:
    browser.implicitly_wait(10)
    try:
        # Проверка авторизации пользователя.
        if (authorization_docsvision_admin(browser, login, passwd) == False):
            quit()

        # Переход в модуль конструктор отчетов.
        transition_to_report_designer(browser)

        # Переход в справочник подключения.
        transition_to_connect(browser)

        # Нажатие на кнопку создания строки подключения.
        create_new_connect(browser)

        # Заполнение полей в соответствии с справочником.
        for control in attributes_connect:
            browser.find_element(By.XPATH, control["path"]).send_keys(control["value"])

        # Сохранение строки справочника.
        browser.find_element(By.XPATH, "//div[text() = 'Сохранить']/ancestor::button").click()

        # Открытие созданного отчета
        browser.find_element(By.XPATH, "//div[@title = 'Test_Connect']/ancestor::div[@role='row']").click()

        # Проверка заполнения атрибутов строки подключения.
        errors = []
        for control in attributes_connect:
            element_value = browser.find_element(By.XPATH, control["path"]).get_attribute('value')
            if element_value != control['value']:
                errors.append(control['name'] + "не найден на разметке.")

        browser.find_element(By.XPATH, "//div[text()='Отменить']").click()

        # Удаление строки подключения
        delete_report(browser, attributes_connect[0]["value"])

        # Расчет результатов.
        if len(errors) > 0:
            print("Автотест методики проверки №3.1 завершен с Ошибкой")
            for error in errors:
                print(error)
        else:
            print("Автотест методики проверки №3.1 завершен Успешно")

    except Exception as ex:
        print(f"Автотест методики проверки №3.1завершен с Ошибкой: {str(ex)}")