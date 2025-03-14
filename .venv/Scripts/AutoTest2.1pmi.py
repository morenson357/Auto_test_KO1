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

options = webdriver.ChromeOptions()
options.add_argument('--headless')
with webdriver.Chrome() as browser:
    browser.implicitly_wait(6)
    try:
        browser.get(auth_site)
        browser.find_element(By.CLASS_NAME, "login-input__input").send_keys("vm-dv-report-02\Администратор")
        browser.find_element(By.NAME, "Пароль").send_keys("Patron_2001")
        browser.find_element(By.CLASS_NAME, "login-button").click()
        #time.sleep(5)
        browser.find_element(By.XPATH, main_menu)
        print("Авторизация пройдена успешно - ОК")
        #time.sleep(3)
        browser.get(report_site)
        print("Выполнен переход в модуль \"Конструктор отчетов\" - ОК")

        setting_reports = browser.find_element(By.XPATH, "//span[contains(text(),'Настройка отчетов')]")
        setting_reports.click()
        print("Выполнен переход на вкладку \"Настройка отчетов\" - ОК")

        create_report = browser.find_element(By.CSS_SELECTOR, "[class='MuiButtonBase-root MuiIconButton-root MuiIconButton-sizeMedium css-mndvqg-MuiButtonBase-root-MuiIconButton-root']")
        create_report.click()
        time.sleep(5)

        def check_exists_by_xpath(xpath):
            try:
                browser.find_element(By.XPATH, xpath)
            except NoSuchElementException:
                return False
            return True

        add_rows = browser.find_elements(By.XPATH, "//button[@data-button-name='add-row']")
        for i in add_rows:
            i.click()
        
        errors = []
        print("Идёт проверка элементов...")
        for key, value in attributes_report_dictionary.items():
            if (check_exists_by_xpath(value) == False):
                errors.append('Элемент управления ' + key +' не найден')

        if (len(errors) == 0):
            print("\nАвтотест методики проверки №2.1 завершен - Успешно")
        else:
            print("\nАвтотест методики проверки №2.1 завершен с Ошибкой:")
            for error in errors:
                print(error)
        
    except Exception as ex:
        print(f"Произошла ошибка: {str(ex)}")
