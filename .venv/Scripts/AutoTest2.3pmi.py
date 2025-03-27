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
        name_report = "test_report_pmi_dell 2.3"
        browser.find_element(By.XPATH, attributes_report_dictionary['Название отчета']).send_keys(name_report)
        browser.find_element(By.XPATH, attributes_report_dictionary['Провайдер']).click()
        # Выбор провайдера FastReport
        time.sleep(2)
        browser.find_element(By.XPATH, "//button[@data-button-name='ok']").click()
        print('Обязательные поля заполнены - ОК')


        count_parameters = 15
        control_names = []
        for i in range(count_parameters):
            #Добавление новой строки таблицы параметров.
            browser.find_element(By.XPATH, '//div[@data-control-name="BTL_ReportParametersTable"]//span[@data-tipso-text="Добавить строку"]').click()

            # Добавление нового параметра 1, 2, 3...
            time.sleep(1)
            buttons = browser.find_elements(By.XPATH, attributes_report_dictionary['Параметр'])
            buttons[i].click()
            parameters = browser.find_elements(By.XPATH, '//div[@class="directory-select-dialog "]//div[@tabindex=0]')
            parameters[i].click()
            browser.find_element(By.XPATH, "//button[@data-button-name='ok']").click()

            #Получение названия типа параметра.
            time.sleep(1)
            parameters_name = browser.find_elements(By.XPATH, "//div[@data-control-name='BTL_Parameter[]']//input")
            parameter_type = parameters_name[i].get_attribute('value')

            #Заполнение Названия параметра и текста метки.
            time.sleep(1)
            text_names = browser.find_elements(By.XPATH, attributes_report_dictionary['Название параметра'])
            text_names[i].send_keys('contrl' + str(i + 1))
            control_names.append('contrl' + str(i + 1))
            text_marks = browser.find_elements(By.XPATH, attributes_report_dictionary['Текст метки'])
            text_marks[i].send_keys('Контрол ' + str(i + 1))

            if parameter_type == 'Расширение файла отчета':
                #Перезапись Названия параметра в списке.
                control_names[i] = 'format'
                time.sleep(1)
            elif parameter_type == 'ЭУ Ссылка на карточку':
                #Заполнение свойства Подсказка.
                time.sleep(1)
                prompts = browser.find_elements(By.XPATH, attributes_report_dictionary['Подсказка'])
                prompts[i].send_keys("link")
                time.sleep(1)
            elif parameter_type == 'ЭУ Строка конструктора справочников':
                #Выбор узла конструктора справочников.
                time.sleep(1)
                nodes_directory = browser.find_elements(By.XPATH, attributes_report_dictionary['Узел конструктора справочника'])
                time.sleep(1)
                nodes_directory[i].click()
                browser.find_element(By.XPATH, "//div[text() = 'Выбрать']").click()

        print("Параметры заполнены - ОК")
        #Сохранить отчет.
        time.sleep(5)
        browser.find_element(By.CSS_SELECTOR, "[class='button-helper card-type-background-color-hover card-type-background-color-light primary-button align-center']").click()
        time.sleep(3)
        print("Отчет сохранен - ОК")
        #Открытие созданного отчета.
        transition_to_report_list(browser)
        browser.find_element(By.XPATH, "//div[text() = '"+ name_report +"']").click()
        print("Отчет открыт - ОК")
        #Функция проверки присутствия элемента на разметке.
        def check_exists_by_xpath(xpath):
            try:
                browser.find_element(By.XPATH, xpath)
            except NoSuchElementException:
                return False
            return True

        errors = []

        #Проверка присутствия элементов на разметке.
        for name in control_names:
            xpath_control = "//div[contains(@data-control-name,'" + name + "')]"

            if (check_exists_by_xpath(xpath_control) == False):
                errors.append('ЭУ с названием ' + name + ' не найден - ERROR' )

        print("Проверка присутствия элементов пройдена - ОК")
        #Формирование результатов проверки.
        if len(errors) == 0:
            browser.find_element(By.XPATH, "//div[text() = 'Отменить']").click()
            #Удаление отчета
            transition_to_setting_reports(browser)
            delete_report(browser, name_report)
            print("Автотест методики проверки №2.3 завершен Успешно")
        else:
            print("\nАвтотест методики проверки №2.3 завершен с Ошибкой:")
            for error in errors:
                print(error)

    except Exception as ex:
        print(f"Автотест методики проверки №2.3 завершен с Ошибкой: {str(ex)}")

