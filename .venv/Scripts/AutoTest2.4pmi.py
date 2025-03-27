from itertools import count
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from dir.site_info_dv import auth_site, report_site, main_menu
from selenium.webdriver import ActionChains
from dir.attributes_report import attributes_report_dictionary, parameters_generate_report, data_report
from selenium.common.exceptions import NoSuchElementException
from Authorization_Admin import authorization_docsvision_admin
from dir.auth_date import login, passwd
from action_report import transition_to_report_designer, transition_to_setting_reports, click_to_create_report, transition_to_report_list, delete_report

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

        # Заполнение обязательных атрибутов.
        name_report = "test_report_pmi_dell_2.4"
        browser.find_element(By.XPATH, attributes_report_dictionary['Название отчета']).send_keys(name_report)
        browser.find_element(By.XPATH, attributes_report_dictionary['Провайдер']).click()
        # Выбор провайдера FastReport
        time.sleep(2)
        browser.find_element(By.XPATH, "//button[@data-button-name='ok']").click()
        print('Обязательные поля заполнены - ОК')
        for row_data in data_report:
            time.sleep(3)
            # Добавление новой строки таблицы данных.
            add_row = browser.find_element(By.XPATH, "//div[@data-control-name='BTL_ReportDataTable']//button[@data-button-name='add-row']")
            add_row.click()
            # Заполнение имя источника в шаблоне
            name_date = browser.find_elements(By.XPATH, attributes_report_dictionary['Имя источника в шаблоне'])
            name_date[-1].send_keys(row_data['name'])
            # Заполнение Типа источника в шаблоне
            type_date = browser.find_elements(By.XPATH, attributes_report_dictionary['Тип источника данных'])
            type_date[-1].click()
            browser.find_element(By.XPATH, "//div[@data-element-id = 'SQL']").click()
            # Заполнение Подключение
            connect_date = browser.find_elements(By.XPATH, attributes_report_dictionary['Подключение'])
            connect_date[-1].click()
            browser.find_element(By.XPATH, "//div[text() = 'docsvision']").click()
            browser.find_element(By.XPATH, "//button[@data-button-name = 'ok']").click()
            #Заполнение Функция
            browser.execute_script("layoutManager.getLayouts()[layoutManager.getLayouts().length - 1].controls.BTL_Function[layoutManager.getLayouts()[layoutManager.getLayouts().length - 1].controls.BTL_Function.length - 1].value = arguments[0]", row_data['function'])

        for row_pam in parameters_generate_report:
            # Добавление новой строки таблицы параметров.
            add_row = browser.find_element(By.XPATH,"//div[@data-control-name='BTL_ReportParametersTable']//button[@data-button-name = 'add-row']")
            add_row.click()
            # Добавление нового параметра 1, 2, 3...
            buttons = browser.find_elements(By.XPATH, attributes_report_dictionary['Параметр'])
            buttons[-1].click()
            # Выбор параметра
            parameter = browser.find_element(By.XPATH, "//div[@title='" + row_pam['type'] + "']")
            parameter.click()
            browser.find_element(By.XPATH, "//button[@data-button-name='ok']").click()
            # Заполнения наименования
            names_p = browser.find_elements(By.XPATH, attributes_report_dictionary['Название параметра'])
            names_p[-1].send_keys(row_pam['name'])
            # Заполнение текста метки
            text_p = browser.find_elements(By.XPATH, attributes_report_dictionary['Текст метки'])
            text_p[-1].send_keys(row_pam['text_mark'])
            # Заполнение подсказки
            heants_p = browser.find_elements(By.XPATH, attributes_report_dictionary['Подсказка'])
            heants_p[-1].send_keys(row_pam['heant'])
            # Заполнение узлов
            if row_pam['nodes'] != '':
                nodes_p = browser.find_elements(By.XPATH, attributes_report_dictionary['Узел конструктора справочника'])
                nodes_p[-1].click()
                time.sleep(5)
                browser.find_element(By.XPATH, "//div[text() = 'Выбрать']/ancestor::button").click()
                time.sleep(5)
            # Заполнение свойств
            if row_pam["property"] != '':
                property_p = browser.find_elements(By.XPATH, attributes_report_dictionary['Свойства'])
                property_p[-1].send_keys(row_pam["property"])

        browser.find_element(By.XPATH, attributes_report_dictionary['Шаблон отчета']).click()
        browser.find_element(By.XPATH, "//div[@data-control-name='paramalias3_Condition_alias2']//input[@data-testid='input']").send_keys("Contractrenewalreport.frx")
        browser.find_element(By.XPATH, "//div[text() = 'Искать']/ancestor::button").click()
        browser.find_element(By.XPATH, "//span[text() = 'Файл Contractrenewalreport.frx']/ancestor::div[@class = 'search-results-item-content']").click()
        browser.find_element(By.XPATH, "//div[text() = 'ОК']/ancestor::button").click()


        #Сохранить отчет.
        time.sleep(5)
        browser.find_element(By.CSS_SELECTOR, "[class='button-helper card-type-background-color-hover card-type-background-color-light primary-button align-center']").click()
        time.sleep(3)
        # Открытие созданного отчета.
        transition_to_report_list(browser)
        browser.find_element(By.XPATH, "//div[text() = '"+ name_report +"']").click()
        #Формирование отчета
        browser.find_element(By.XPATH, "//div[text() = 'Сформировать']").click()

        time.sleep(6)
        original_window = browser.current_window_handle
        handles = browser.window_handles
        new_tab_handle = handles[-1]  # Получаем дескриптор новой вкладки (последней в списке)
        browser.switch_to.window(new_tab_handle)  # Переключаемся на новую вкладку

        currency_find = browser.find_elements(By.XPATH, "//div[contains(text(), 'RUB')]")



        if len(currency_find) == 4:
            print("Автотест методики проверки №2.4 завершен - Успешно")
        else:
            print("Автотест методики проверки №2.4 завершен с ошибкой")
    except Exception as ex:
        print(f"Автотест методики проверки №2.4 завершен с Ошибкой: {str(ex)}")