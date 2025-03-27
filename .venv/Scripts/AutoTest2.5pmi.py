from itertools import count
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from dir.site_info_dv import auth_site, report_site, main_menu
from selenium.webdriver import ActionChains
from dir.attributes_report import attributes_report_dictionary, parameters_report
from selenium.common.exceptions import NoSuchElementException
from Authorization_Admin import authorization_docsvision_admin
from dir.auth_date import login, passwd
from action_report import transition_to_report_designer, transition_to_setting_reports, click_to_create_report, transition_to_report_list, delete_report
from dir.function_date import dateContract, dateContractss, dateAdditionaloptions

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
        name_report = "test_report_pmi_dell"
        browser.find_element(By.XPATH, attributes_report_dictionary['Название отчета']).send_keys(name_report)
        browser.find_element(By.XPATH, attributes_report_dictionary['Провайдер']).click()
        # Выбор провайдера FastReport
        time.sleep(2)
        browser.find_element(By.XPATH, "//button[@data-button-name='ok']").click()
        print('Обязательные поля заполнены - ОК')


        count_parameters = 1
        control_names = []
        for row_pam in parameters_report:
            #Добавление новой строки таблицы параметров.
            add_row = browser.find_element(By.XPATH, "//div[@data-control-name='BTL_ReportParametersTable']//button[@data-button-name = 'add-row']")
            add_row.click()

            # Добавление нового параметра 1, 2, 3...
            buttons = browser.find_elements(By.XPATH, attributes_report_dictionary['Параметр'])
            buttons[-1].click()
            #Выбор параметра
            parameter = browser.find_element(By.XPATH, "//div[@title='" + row_pam['type'] + "']")
            parameter.click()
            browser.find_element(By.XPATH, "//button[@data-button-name='ok']").click()
            #Заполнения наименования
            names_p = browser.find_elements(By.XPATH, attributes_report_dictionary['Название параметра'])
            names_p[-1].send_keys(row_pam['name'])
            #Заполнение текста метки
            text_p = browser.find_elements(By.XPATH, attributes_report_dictionary['Текст метки'])
            text_p[-1].send_keys(row_pam['text_mark'])
            #Заполнение подсказки
            heants_p = browser.find_elements(By.XPATH, attributes_report_dictionary['Подсказка'])
            heants_p[-1].send_keys(row_pam['heant'])
            #Заполнение узлов
            if row_pam['nodes'] != '':
                nodes_p = browser.find_elements(By.XPATH, attributes_report_dictionary['Узел конструктора справочника'])
                nodes_p[-1].click()
                time.sleep(5)
                browser.find_element(By.XPATH, "//div[text() = 'Выбрать']/ancestor::button").click()
                time.sleep(5)
            #Заполнение свойств
            if row_pam['property'] != '':
                props_p = browser.find_elements(By.XPATH, attributes_report_dictionary['Свойства'])
                props_p[-1].send_keys(row_pam['property'])
        #Сохранить отчет.
        time.sleep(5)
        browser.find_element(By.CSS_SELECTOR, "[class='button-helper card-type-background-color-hover card-type-background-color-light primary-button align-center']").click()
        time.sleep(3)

        #Открытие созданного отчета.
        transition_to_report_list(browser)
        browser.find_element(By.XPATH, "//div[text() = 'test_report_pmi_dell']").click()

        #Функция проверки присутствия элементов на разметке.
        def check_exists_by_xpath(xpath):
            try:
               elements = browser.find_elements(By.XPATH, xpath)
               return len(elements) > 0
            except Exception as e:
                print(f"Произошла непредвиденная ошибка: {e}")
                return False

        value_controls = []
        #Заполнение элементов на разметке.
        for row_pam in parameters_report:

            #Заполнение Диапазон дат.
            if row_pam['type'] == "Диапазон дат":
                xpath_control = "//div[contains(@data-control-name, '" + row_pam['name'] + "')]//button[@class = 'MuiButtonBase-root MuiIconButton-root']"
                control_date = browser.find_elements(By.XPATH, xpath_control)
                control_date[0].click()
                time.sleep(2)
                browser.find_element(By.XPATH, "//span[text() = 'СЕГОДНЯ']/ancestor::button").click()
                value_controls.append(browser.find_elements(By.XPATH, "//div[contains(@data-control-name, '" + row_pam['name'] + "')]//input")[0].get_attribute('value'))

                time.sleep(5)
                control_date[1].click()
                time.sleep(2)
                browser.find_element(By.XPATH, "//span[text() = 'НЕДЕЛЯ']/ancestor::button").click()
                value_controls.append(browser.find_elements(By.XPATH, "//div[contains(@data-control-name, '" + row_pam['name'] + "')]//input")[1].get_attribute('value'))

            # Заполнение Диапазона чисел.
            elif row_pam['type'] == "Диапазон чисел":
                xpath_control = "//div[contains(@data-control-name, '" + row_pam['name'] + "')]//input"
                control_num = browser.find_elements(By.XPATH, xpath_control)
                control_num[0].send_keys("100")
                #value_controls.append("100")
                control_num[1].send_keys("3000")
                #value_controls.append("3000")

            # Заполнение ЭУ Строка конструктора справочников.
            elif row_pam['type'] == "ЭУ Строка конструктора справочников":
                xpath_control = "//div[contains(@data-control-name, '" + row_pam['name'] + "')]//button[@data-button-name='open-dictionary']"
                browser.find_element(By.XPATH, xpath_control).click()
                browser.find_element(By.XPATH, "//div[@title= 'Закупки']").click()
                value_controls.append("Закупки")
                browser.find_element(By.XPATH, "//button[@data-button-name = 'ok']").click()

            # Заполнение ЭУ Подразделение.
            elif row_pam['type'] == "ЭУ Подразделение":
                xpath_control = "//div[contains(@data-control-name, '" + row_pam['name'] + "')]//button[@data-button-name='open-dictionary']"
                browser.find_element(By.XPATH, xpath_control).click()
                browser.find_element(By.XPATH, "//span[text() = 'DV']/ancestor::button").click()
                value_controls.append("DV")
                browser.find_element(By.XPATH, "//div[text() = 'Выбрать']").click()

            # Заполнение ЭУ Сотрудники.
            elif row_pam['type'] == "ЭУ Сотрудники":
                xpath_control = "//div[contains(@data-control-name, '" + row_pam['name'] + "')]//button[@data-button-name='show-variants']"
                browser.find_element(By.XPATH, xpath_control).click()
                browser.find_element(By.XPATH, "//span[@title = 'Аксенов А. А.']/ancestor::div[@class='variant-row']").click()
                value_controls.append("Аксенов А. А.")
            # Заполнение ЭУ Перечисление.
            elif row_pam['type'] == "ЭУ Перечисление":
                value_controls.append("RUB")

        #Сохранение шаблона параметров и выбор Новые параметры
        browser.find_element(By.XPATH, "//div[text() = 'Сохранить как']").click()
        time.sleep(2)
        browser.find_element(By.XPATH, "//div[@data-control-name='templateName']//input").send_keys("testTemplate")
        time.sleep(2)
        browser.find_element(By.XPATH, "//div[@class='modal-dialog-button-panel-item']//div[text() = 'Сохранить']/ancestor::button").click()
        time.sleep(2)
        browser.find_element(By.XPATH, "//button[@class = 'button-helper empty-text stretch-width align-center']").click()
        time.sleep(2)
        browser.find_element(By.XPATH, "//div[text() = 'testTemplate']").click()
        time.sleep(2)
        browser.find_element(By.XPATH, "//div[text() = 'Новые параметры']").click()
        time.sleep(2)


        result = True
        out_value = []
        #Проверка очистки формы параметров.
        for row_pam in parameters_report:

            if row_pam['type'] == 'Диапазон дат':
                xpath_control = "//div[contains(@data-control-name, '" + row_pam['name'] + "')]//input"
                control_date = browser.find_elements(By.XPATH, xpath_control)
                if control_date[0].get_attribute("value") != '' and control_date[1].get_attribute("value") != '':
                    result = False
                    out_value.append(row_pam['type'] + "- не очищено")

            elif row_pam['type'] == "ЭУ Строка конструктора справочников":
                xpath_control = "//div[contains(@data-control-name, '" + row_pam['name'] + "')]//input"
                if browser.find_element(By.XPATH, xpath_control).get_attribute("value") != '':
                    result = False
                    out_value.append(row_pam['type'] + "- не очищено")

            elif row_pam['type'] == "ЭУ Подразделение":
                xpath_control = "//div[contains(@data-control-name, '" + row_pam['name'] + "')]//input"
                if browser.find_element(By.XPATH, xpath_control).get_attribute("value") != '':
                    result = False
                    out_value.append(row_pam['type'] + "- не очищено")

            elif row_pam['type'] == "ЭУ Сотрудники":
                xpath_control = "//div[contains(@data-control-name, '" + row_pam['name'] + "')]//span[text() = 'Аксенов А. А.']"
                if (check_exists_by_xpath(xpath_control) == True):
                    result = False
                    out_value.append(row_pam['type'] + "- не очищено")

        #Результат проверки очистки формы
        if result == False:
            print("\nАвтотест методики проверки №2.5-№2.6 завершен с Ошибкой:")
            for value in out_value:
                print(value)
                quit()

        #Выбор сохраненного шаблона
        browser.find_element(By.XPATH, "//div[text() = 'Новые параметры']").click()
        time.sleep(2)
        browser.find_element(By.XPATH, "//div[text() = 'testTemplate']").click()
        time.sleep(2)

        #Проверка соответствия заданым параметрам
        for row_pam in parameters_report:
            if row_pam['type'] == 'Диапазон дат':
                xpath_control = "//div[contains(@data-control-name, '" + row_pam['name'] + "')]//input"
                control_date = browser.find_elements(By.XPATH, xpath_control)
                if control_date[0].get_attribute("value") != value_controls[0] and control_date[1].get_attribute("value") != value_controls[1]:
                    result = False
                    out_value.append(row_pam['type'] + "- пуст")
            elif row_pam['type'] == "ЭУ Перечисление":
                xpath_control = "//div[contains(@data-control-name, '" + row_pam['name'] + "')]//div[text() = '"+ value_controls[2] +"']"
                if check_exists_by_xpath(xpath_control) == False:
                    result = False
                    out_value.append(row_pam['type'] + "- пуст")
            elif row_pam['type'] == "ЭУ Строка конструктора справочников":
                xpath_control = "//div[contains(@data-control-name, '" + row_pam['name'] + "')]//input"
                if browser.find_element(By.XPATH, xpath_control).get_attribute("value") != value_controls[3]:
                    result = False
                    out_value.append(row_pam['type'] + "- пуст")
            elif row_pam['type'] == "ЭУ Подразделение":
                xpath_control = "//div[contains(@data-control-name, '" + row_pam['name'] + "')]//input"
                if browser.find_element(By.XPATH, xpath_control).get_attribute("value") != value_controls[4]:
                    result = False
                    out_value.append(row_pam['type'] + "- пуст")
            elif row_pam['type'] == "ЭУ Сотрудники":
                xpath_control = "//div[contains(@data-control-name, '" + row_pam['name'] + "')]//span[text() = 'Аксенов А. А.']"
                if (check_exists_by_xpath(xpath_control) == False):
                    result = False
                    out_value.append(row_pam['type'] + "- пуст")

        #Формирование результатов проверки.
        if result == True:
            print("Автотест методики проверки №2.5-№2.6 завершен Успешно")
            browser.find_element(By.XPATH, "//div[text() = 'Отменить']").click()
            #Удаление отчета
            transition_to_setting_reports(browser)
            delete_report(browser, name_report)
        else:
            print("\nАвтотест методики проверки №2.5-№2.6 завершен с Ошибкой:")
            for value in out_value:
                print(value)

    except Exception as ex:
        print(f"Автотест методики проверки №2.5-№2.6 завершен с Ошибкой: {str(ex)}")

