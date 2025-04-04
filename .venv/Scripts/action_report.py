from selenium import webdriver
from dir.site_info_dv import report_site
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
from selenium.webdriver import ActionChains
from Authorization_Admin import check_exists_by_xpath

# Переход в модуль конструктор отчетов.
def transition_to_report_designer(browser: webdriver.Chrome):
    browser.get(report_site)
    print("Выполнен переход в модуль \"Конструктор отчетов\" - ОК")

# Переход в настройки отчетов.
def transition_to_setting_reports(browser: webdriver.Chrome):
    setting_reports = browser.find_element(By.XPATH, "//span[contains(text(),'Настройка отчетов')]")
    setting_reports.click()
    print("Выполнен переход на вкладку \"Настройка отчетов\" - ОК")

#Нажатие на кнопку создания отчета.
def click_to_create_report(browser: webdriver.Chrome):
    create_report = browser.find_element(By.CSS_SELECTOR, "[class='MuiButtonBase-root MuiIconButton-root MuiIconButton-sizeMedium css-mndvqg-MuiButtonBase-root-MuiIconButton-root']")
    create_report.click()
    time.sleep(3)

#Переход на вкладку Отчеты
def transition_to_report_list(browser: webdriver.Chrome):
    report_list = browser.find_element(By.XPATH, "//li[@class='MuiListItem-root MuiListItem-gutters MuiListItem-padding css-tciken-MuiListItem-root']//span[text()='Отчеты']")
    report_list.click()

#Нажатие на кпноку создания строки подключения
def create_new_connect(browser: webdriver.Chrome):
    time.sleep(12)
    create_connect = "//button[@class='MuiButtonBase-root MuiIconButton-root MuiIconButton-sizeMedium css-mndvqg-MuiButtonBase-root-MuiIconButton-root']"
    if check_exists_by_xpath(browser, create_connect) == True:
        browser.find_element(By.XPATH, create_connect).click()
    else:
        print("Кнопка создания строки подключения не найдена ERROR")
        quit()

# Переход на вкладку Подключения
def transition_to_connect(browser: webdriver.Chrome):
    to_connect = browser.find_element(By.XPATH, "//span[text() = 'Подключения']/ancestor::div[@class = 'MuiListItemText-root css-cfq8qh-MuiListItemText-root']")
    to_connect.click()
    print("Выполнен переход на вкладку \"Подключения\" - ОК")

#Удаление отчета
def delete_report(browser: webdriver.Chrome, name_report:str):
    actionChains = ActionChains(browser)
    xpath_name_report = "//div[text()='" + name_report + "']"
    actionChains.context_click(browser.find_element(By.XPATH, xpath_name_report)).perform()
    browser.find_element(By.XPATH, "//li[text()='Удалить']").click()
    time.sleep(2)
    browser.find_element(By.XPATH, "//button[@datatestid='button-ok']").click()
    time.sleep(2)
    browser.find_element(By.XPATH, "//button[@class='button-helper empty-text stretch-width align-center']").click()
    time.sleep(2)
    print("Отчет удален - ОК")

