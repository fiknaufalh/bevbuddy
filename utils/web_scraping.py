from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchWindowException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
import traceback
import json
import re

def main():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    wait = WebDriverWait(driver, 10)

    URL = "https://www.starbucks.com/menu"

    menu_table = []
    nutrition_table = []

    driver.maximize_window()
    driver.get(URL)

    wait.until(EC.presence_of_element_located((By.ID, "drinks")))
    drinks = driver.find_element(By.ID, "drinks")
    categories_link = [(category.text, category.get_attribute("href")) 
                        for category in drinks.find_elements(By.TAG_NAME, "a")]

    menus = []
    exclude_category = ["coffee-travelers"]
    for category_link in categories_link:
        driver.get(category_link[1])
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "section")))
        subcategories = driver.find_elements(By.TAG_NAME, "section")
        menus_web = [subcategory.find_elements(By.TAG_NAME, "a") 
                    for subcategory in subcategories if subcategory.get_attribute("id") not in exclude_category]

        for menu in menus_web:
            for item in menu:
                menus.append((item.get_attribute("data-e2e"), item.get_attribute("href")))

    for menu in menus:
        driver.get(f"{menu[1]}/nutrition")

        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1 + div")))
            nutrition_dict = extract_nutrition(driver, menu[1])
            menu_dict = extract_menu(driver, menu[1])

            nutrition_table.append(nutrition_dict)
            menu_table.append(menu_dict)
        except:
            traceback.print_exc()
            continue

    export_to_json(menu_table, r"/data/web_scraping/menu.json")
    export_to_json(nutrition_table, r"/data/web_scraping/nutrition.json")


def export_to_json(data, filename):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

def extract_product_id(url):
    pattern = r'/product/(\d+)/'
    match = re.search(pattern, url)
    
    if match:
        product_id = match.group(1)
        return int(product_id)
    else:
        return None

def extract_nutrition(driver, menu):
    nutrition_dict = {
        "id_menu": "",
        "calories": "",
        "protein": "",
        "fats": "",
        "carbs": "",
        "sugar": "",
    }

    nutrition_dict["id_menu"] = extract_product_id(menu)

    nutrition_list = driver.find_elements(By.CSS_SELECTOR, "div[data-e2e='nutritionTable'] > div")

    nutrition_dict["calories"] = float(nutrition_list[0].find_element(
        By.CSS_SELECTOR, "span > span + span").text.split()[0])
    nutrition_dict["protein"] = float(nutrition_list[5]. find_element(
        By.CSS_SELECTOR, "span > span + span").text.split()[0])
    nutrition_dict["fats"] = float(nutrition_list[1].find_element(
        By.CSS_SELECTOR, "span > span + span").text.split()[0])
    nutrition_dict["carbs"] = float(nutrition_list[4].find_element(
        By.CSS_SELECTOR, "span > span + span").text.split()[0])
    nutrition_dict["sugar"] = float(nutrition_list[4].find_element(
        By.CSS_SELECTOR, "div + div + div > div > span > span + span").text.split()[0])

    return nutrition_dict

def extract_menu(driver, menu):
    menu_dict = {
        "id": "",
        "name": "",
        "desc": "",
        "category": "",
        "url_img": ""
    }

    menu_dict["id"] = extract_product_id(menu)
    menu_dict["name"] = driver.find_element(By.CSS_SELECTOR, "h1").text
    menu_dict["desc"] = driver.find_element(By.CSS_SELECTOR, "p[data-e2e='productDescription']").text.strip('"')
    menu_dict["category"] = driver.find_elements(By.CSS_SELECTOR, "a[class='text-noUnderline']")[1].text
    menu_dict["url_img"] = driver.find_element(By.TAG_NAME, "img").get_attribute("src")

    return menu_dict

if __name__ == "__main__":
    main()