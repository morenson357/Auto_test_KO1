import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from dir.site_info_dv import auth_site, report_site
from selenium.webdriver import ActionChains

options = webdriver.ChromeOptions()
options.add_argument('--headless')
with webdriver.Chrome() as browser:
    browser.implicitly_wait(20)
    try:
        browser.get(auth_site)
        browser.find_element(By.CLASS_NAME, "login-input__input").send_keys("vm-dv-report-02\Администратор")
        browser.find_element(By.NAME, "Пароль").send_keys("Patron_2001")
        browser.find_element(By.CLASS_NAME, "login-button").click()
        time.sleep(3)
        browser.find_element(By.XPATH, main_menu)
        print("Авторизация пройдена успешно - ОК")
        time.sleep(3)
        browser.get(report_site)
        print("Выполнен переход в модуль \"Конструктор отчетов\" - ОК")




        setting_reports = browser.find_element(By.XPATH, "//span[contains(text(),'Настройка отчетов')]")
        setting_reports.click()
        print("Выполнен переход на вкладку \"Настройка отчетов\" - ОК")

        browser.find_element(By.CSS_SELECTOR, "[class='MuiButtonBase-root MuiIconButton-root MuiIconButton-sizeMedium css-mndvqg-MuiButtonBase-root-MuiIconButton-root']").click()
        browser.find_element(By.XPATH, "//div[@data-tipso-text='Название']").find_element(By.TAG_NAME, 'input').send_keys('test_report_pmi_dell')
        browser.find_element(By.XPATH, "//div[@data-control-name='BTL_Provider']").find_element(By.TAG_NAME, 'button').click()
        time.sleep(2)
        browser.find_element(By.XPATH, "//button[@data-button-name='ok']").click()
        browser.find_element(By.CSS_SELECTOR, "[class='button-helper card-type-background-color-hover card-type-background-color-light primary-button align-center']").click()
        print("Сформирован черновик отчета - ОК")

        report_list = browser.find_element(By.XPATH, "//li[@class='MuiListItem-root MuiListItem-gutters MuiListItem-padding css-tciken-MuiListItem-root']//span[text()='Отчеты']")
        report_list.click()
        browser.find_element(By.XPATH, "//div[text()='test_report_pmi_dell']").click()
        browser.find_element(By.XPATH, "//div[text()='Ошибка сервера: Ошибка сервиса отчетов: Отсутствует ссылка на шаблон отчета']")
        browser.find_element(By.XPATH, "//button[@class='button-helper empty-text stretch-width align-center']").click()
        print("Получено уведомление об ошибке отсутствия шаблона отчета - ОК")

        setting_reports.click()
        actionChains = ActionChains(browser)
        actionChains.context_click(browser.find_element(By.XPATH,"//div[text()='test_report_pmi_dell']")).perform()
        browser.find_element(By.XPATH,"//li[text()='Удалить']").click()
        browser.find_element(By.XPATH, "//button[@datatestid='button-ok']").click()
        browser.find_element(By.XPATH, "//button[@class='button-helper empty-text stretch-width align-center']").click()
        time.sleep(2)
        print("Черновик отчета успешно удален - ОК")
        print("Автотест методики проверки №2.2 завершен - Успешно")
    except Exception as ex:
        print(f"Произошла ошибка: {str(ex)}")



