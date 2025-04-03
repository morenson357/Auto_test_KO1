from itertools import count
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from dir.site_info_dv import auth_site, report_site, main_menu
from selenium.webdriver import ActionChains
from dir.attributes_report import attributes_report_dictionary
from selenium.common.exceptions import NoSuchElementException
from Authorization_Admin import authorization_docsvision_admin
from dir.auth_date import login, passwd
from action_report import transition_to_report_designer, transition_to_setting_reports, click_to_create_report, transition_to_report_list, delete_report

def run_test():
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

            # Переход в настройки отчетов.
            transition_to_setting_reports(browser)

            # Нажатие на кнопку создания отчета.
            click_to_create_report(browser)


            # Функция проверки присутствия элементов на разметке.
            def check_exists_by_xpath(xpath):
                try:
                    elements = browser.find_elements(By.XPATH, xpath)
                    return len(elements) > 0
                except Exception as e:
                    print(f"Произошла непредвиденная ошибка: {e}")
                    return False

            # Заполнение обязательных атрибутов.
            name_report = "test_report_pmi_dell_4_1"
            browser.find_element(By.XPATH, attributes_report_dictionary['Название отчета']).send_keys(name_report)
            browser.find_element(By.XPATH, attributes_report_dictionary['Провайдер']).click()
            # Выбор провайдера FastReport
            time.sleep(2)
            browser.find_element(By.XPATH, "//button[@data-button-name='ok']").click()
            print('Обязательные поля заполнены - ОК')

            # Переход на вкладку условий доступности.
            browser.find_element(By.XPATH, "//li[@data-tipso-text='Условия доступности']").click()

            # Установка доступности для Тестового пользователя
            browser.find_element(By.XPATH, "//div[@data-control-name='BTL_Employees']//input").send_keys("Test user")
            browser.find_element(By.XPATH, "//a[@title = 'Test user user']").click()

            # Сохранить отчет..
            browser.find_element(By.XPATH, "//div[@class='dv-control system-custombutton no-stretch-width ']//div[text() = 'Сохранить']//ancestor::button").click()

            # Переход на вкладку Отчеты
            transition_to_report_list(browser)

            # Поиск созданного отчета.
            report_access = "//div[text() = '"+ name_report +"']"
            if (check_exists_by_xpath(report_access) == True):
                print("Автотест методики проверки №4.1` завершен с Ошибкой")
                quit()

            # Авторизация за Тестового пользователя.
            browser.find_element(By.XPATH, "//div[@data-testid = 'user-menu-button']").click()
            browser.find_element(By.XPATH, "//li[text()= 'Выход']").click()

            # Подтверждения алерта выхода
            alert = browser.switch_to.alert  # Получаем объект Alert
            alert.accept()  # Нажимает кнопку "OK" на алерте
            print("Алерт успешно подтвержден.")

            time.sleep(5)
            browser.find_element(By.XPATH, "//span[text() = 'Сменить пользователя']").click()
            time.sleep(5)
            login_tuser = r"VM-DV-REPORT-02\user1"
            passwd_tuser = "aSWS3dc12345"

            # Авторизации тестового пользователя.
            if (authorization_docsvision_admin(browser, login_tuser, passwd_tuser) == False):
                quit()

            # Переход в модуль конструктор отчетов.
            transition_to_report_designer(browser)
            time.sleep(2)

            # Поиск созданного отчета.
            time.sleep(2)
            result = False
            report_access = "//div[text() = '" + name_report + "']"
            if (check_exists_by_xpath(report_access) == True):
                result = True
                browser.find_element(By.XPATH, report_access).click()
                browser.find_element(By.XPATH, "//div[text() = 'Отменить']/ancestor::button)").click()
                print("Отчет найден на разметке - Успешно")

            browser.find_element(By.XPATH, "//div[@data-testid = 'user-menu-button']").click()
            browser.find_element(By.XPATH, "//li[text()= 'Выход']").click()

            # Подтверждения алерта выхода
            alert = browser.switch_to.alert  # Получаем объект Alert
            alert.accept()  # Нажимает кнопку "OK" на алерте
            print("Алерт успешно подтвержден.")

            # Авторизация за администратора Удаление отчета
            if (authorization_docsvision_admin(browser, login, passwd) == False):
                quit()
            # Переход в модуль конструктор отчетов.
            transition_to_report_designer(browser)

            # Переход в настройки отчетов.
            transition_to_setting_reports(browser)

            # Удаление отчета по его названию
            delete_report(browser, name_report)

            if result == True:
                print("Автотест методики проверки №4.1 завершен - Успешно")

        except Exception as ex:
            print(f"Автотест методики проверки №2.2 завершен с Ошибкой: {str(ex)}")
