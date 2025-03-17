import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from dir.site_info_dv import auth_site, report_site
from selenium.webdriver import ActionChains
from Authorization_Admin import authorization_docsvision_admin
from dir.auth_date import login, passwd
from action_report import transition_to_report_designer, transition_to_setting_reports, click_to_create_report, transition_to_report_list, delete_report
from dir.attributes_report import attributes_report_dictionary

options = webdriver.ChromeOptions()
options.add_argument('--headless')
with webdriver.Chrome() as browser:
    browser.implicitly_wait(20)
    try:
        # Проверка авторизации пользователя
        if (authorization_docsvision_admin(browser, login, passwd) == False):
            quit()

        # Переход в модуль конструктор отчетов.
        transition_to_report_designer(browser)

        # Переход в настройки отчетов.
        transition_to_setting_reports(browser)

        # Нажатие на кнопку создания отчета.
        click_to_create_report(browser)

        # Заполнение обязательных атрибутов
        name_report = "test_report_pmi_dell"
        browser.find_element(By.XPATH, attributes_report_dictionary['Название отчета']).send_keys(name_report)
        browser.find_element(By.XPATH, attributes_report_dictionary['Провайдер']).click()
        time.sleep(2)
        # Выбор провайдера FastReport
        browser.find_element(By.XPATH, "//button[@data-button-name='ok']").click()
        browser.find_element(By.CSS_SELECTOR, "[class='button-helper card-type-background-color-hover card-type-background-color-light primary-button align-center']").click()
        print("Сформирован черновик отчета - ОК")

        #Переход на вкладку Отчеты
        transition_to_report_list(browser)

        #Поиск отчета с наименованием test_report_pmi_dell
        browser.find_element(By.XPATH, "//div[text()='test_report_pmi_dell']").click()
        browser.find_element(By.XPATH, "//div[text()='Ошибка сервера: Ошибка сервиса отчетов: Отсутствует ссылка на шаблон отчета']")
        browser.find_element(By.XPATH, "//button[@class='button-helper empty-text stretch-width align-center']").click()
        print("Получено уведомление об ошибке отсутствия шаблона отчета - ОК")
        time.sleep(5)

        # Переход в настройки отчетов.
        transition_to_setting_reports(browser)

        #Удаление отчета по его названию
        delete_report(browser, name_report)

        print("Черновик отчета успешно удален - ОК")
        print("Автотест методики проверки №2.2 завершен - Успешно")
    except Exception as ex:
        print(f"Автотест методики проверки №2.2 завершен с Ошибкой: {str(ex)}")



