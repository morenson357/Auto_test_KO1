#Атрибуты создания отчета на вкладке Основная информация
attributes_report_dictionary = {
    "Название отчета": "//div[@data-control-name='Name']//input",
    "Описание": "//div[@data-control-name='Description']//textarea",
    "Провайдер": "//div[@data-control-name='BTL_Provider']//button[@aria-label='Выбрать из справочника']",
    "Формат вывода": "//div[@data-control-name='BTL_OutputFormat']//div[@class='combobox-helper']",
    "Шаблон отчета": "//a[@data-tipso-text='Шаблон отчета']",
    "Не отображать на форме списка отчетов": "//input[@id='BTL_NotDisplay']",
    "Не используется": "//input[@id='NotAvailable']",
    "Имя источника в шаблоне": "//div[@data-control-name='BTL_TemplateSourceName[]']//input",
    "Тип источника данных": "//div[@data-control-name='BTL_DataSourseType[]'][@data-control-type-name='Dropdown']",
    "Подключение": "//div[@data-control-name='BTL_Connection[]']//button[@aria-label='Выбрать из справочника']",
    "Функция": "//div[@data-control-name='BTL_Function[]']//input",
    "Параметр": "//div[@data-control-name='BTL_Parameter[]']//button[@aria-label='Выбрать из справочника']",
    "Название параметра": "//div[@data-control-name='BTL_Name[]']//input",
    "Текст метки": "//div[@data-control-name='BTL_LabelText[]']//input",
    "Подсказка": "//div[@data-control-name='BTL_Placeholder[]']//input",
    "Узел конструктора справочника": "//div[@data-control-name='BTL_ItemType[]']//button[@aria-label='Выбрать из справочника']",
    "Обязательность": "//input[@id='BTL_Required[]']",
    "Скрытый": "//input[@id='BTL_Hidden[]']",
    "Свойства": "//div[@data-control-name='BTL_Properties[]']//input"
}
#Атрибуты создания отчета на вкладке Условия доступности
attributes_report_dictionary_access = {
    "Группы": "//div[@data-control-name='BTL_Groups']//div[@class='open-dictionary-button-icon dv-ico dv-ico-dictionary']",
    "Подразделения": "//div[@data-control-name='BTL_Units']//div[@class='open-dictionary-button-icon dv-ico dv-ico-dictionary']",
    "Сотрудники": "//div[@data-control-name='BTL_Employees']//div[@class='open-dictionary-button-icon dv-ico dv-ico-dictionary']",
}

parameters_report = [
    {"type": "Диапазон дат", "name": "date", "text_mark": "date", "heant": "date", "nodes": "", "required": "False", "hidden": "False", "property": "", "value": ""},
    {"type": "Диапазон чисел", "name": "num", "text_mark": "num", "heant": "num", "nodes": "", "required": "False", "hidden": "False", "property": ""},
    {"type": "ЭУ Перечисление", "name": "combo", "text_mark": "combo", "heant": "combo", "nodes": "", "required": "False", "hidden": "False", "property": "ENUM=0|EUR,1|RUB,2|USD;PROPERTY.default = 1"},
    {"type": "ЭУ Строка конструктора справочников", "name": "constr", "text_mark": "constr", "heant": "constr", "nodes": "Группы Договоров", "required": "False", "hidden": "False", "property": ""},
    {"type": "ЭУ Подразделение", "name": "Subdivision", "text_mark": "Subdivision", "heant": "Subdivision", "nodes": "", "required": "False", "hidden": "False", "property": ""},
    {"type": "ЭУ Сотрудники", "name": "person", "text_mark": "person", "heant": "person", "nodes": "", "required": "False", "hidden": "False", "property": ""}
]

attributes_connect = [
    {"name": "Название", "path": "//div[@data-tipso-text='Название']//input", "value": "DocsVision"},
    {"name": "Описание", "path": "//div[@data-tipso-text='Описание']//textarea", "value": "Test_Connect"},
    {"name": "Строка подключения", "path": "//div[@data-tipso-text='Строка подключения']//input", "value": "Data Source=VM-DV-REPORT-02;Initial Catalog=Docsvision;Integrated Security=False;User ID=admconnection;Password=1QWerty_12345"}
]




