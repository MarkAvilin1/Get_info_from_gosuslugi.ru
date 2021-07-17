from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from time import sleep
import pandas as pd
import os

"""
    Скрипт, который авторизуется на Госуслугах Создает папку в корневом каталоге скрипта и сохраняет паспортные 
    данные в файл Завершает успешное выполнение
"""

# Данные для авторизации
ACCOUNT_EMAIL = "Почта пользователя"
ACCOUNT_PASSWORD = "Пароль"

# Набор переменных для сбора информации
driver = ""
passport_type = ""
full_name = ""
passport_number = ""
issuing_by = ""
department_code = ""
issue_date = ""

try:
    # С помощью selenium, открыть сайт госуслуги
    chrome_driver_path = "chromedriver/chromedriver.exe"
    driver = webdriver.Chrome(chrome_driver_path)
    driver.get("https://www.gosuslugi.ru/")
    sleep(5)
except Exception as e:
    print(e)

try:
    # Для входа в личный кабинет
    document_list = driver.find_element_by_link_text("Личный кабинет")
    document_list.click()
    sleep(5)

    # Для авторизации
    email_field = driver.find_element_by_id("login")
    email_field.send_keys(ACCOUNT_EMAIL)
    password_field = driver.find_element_by_id("password")
    password_field.send_keys(ACCOUNT_PASSWORD)
    password_field.send_keys(Keys.ENTER)
    sleep(5)

    # Для открытия окна чтобы получить данные
    user_choices = driver.find_element_by_xpath(
        "/html/body/lk-root/header/lib-header/div/div/div[2]/div[2]/div[1]/div/lib-login/div/div[2]/div[1]")
    user_choices.click()
    sleep(2)

    # Для входа в профиль чтобы получить ФИО
    profile = driver.find_element_by_link_text("Профиль")
    profile.click()
    sleep(5)

    # Для получения ФИО
    full_name = driver.find_element_by_xpath("/html/body/lk-root/main/lk-settings/div/div/div[2]/lk-account/div[1]/"
                                             "div[1]/div[2]").text
    sleep(2)

    # Для открытия окна чтобы получить данные
    user_choices = driver.find_element_by_xpath("/html/body/lk-root/header/lib-header/div/div/div[2]/div[2]/"
                                                "div[1]/div/lib-login/div/div[2]/div[1]")
    user_choices.click()
    sleep(2)

    # Для входа в документы чтобы получить паспортные данные
    document_list = driver.find_element_by_xpath("/html/body/lk-root/header/lib-header/div/div/div[2]/div[2]/div[2]/"
                                                 "lib-user-menu/div/div[1]/div/div[1]/ul[2]/li[4]/div/span")
    document_list.click()
    sleep(5)

    # Для получения паспортных данных
    passport_type = driver.find_element_by_css_selector("#passport > lk-doc-card > section > a > div.header > h4").text
    passport_number = driver.find_element_by_css_selector("#passport > lk-doc-card > section > a > div.content > "
                                                          "lk-doc-card-row:nth-child(1) > h5").text
    issuing_by = driver.find_element_by_css_selector(
        "#passport > lk-doc-card > section > a > div.content > lk-doc-card-"
        "row:nth-child(2) > div > div.text-plain.mt-4").text
    department_code = driver.find_element_by_css_selector(
        "#passport > lk-doc-card > section > a > div.content > lk-doc-"
        "card-row:nth-child(3) > div > div.text-plain.mt-4").text
    issue_date = driver.find_element_by_css_selector(
        "#passport > lk-doc-card > section > a > div.content > lk-doc-card-"
        "row:nth-child(4) > div > div.text-plain.mt-4").text
except NoSuchElementException as e:
    print(e)

# Для закрытия сайта после сбора информации
driver.quit()

# Словарь для формата данных
personal_data = {
    "Тип паспорта": passport_type,
    "ФИО": full_name,
    "Серия и номер": passport_number,
    "Выдан": issuing_by,
    "Код подразделения": department_code,
    "Дата выдачи": issue_date,
}

# Для создания директории
directory = "data"

# Для проверки на наличие директории, и создание в случаи отсутствия
if not os.path.exists(directory):
    os.mkdir(directory)

# Для создания дата фрейма с индексом
df = pd.Series(personal_data).to_frame()

# Записать собранные паспортные данные в exel файл
df.to_excel("data/паспортные_данные.xlsx")
