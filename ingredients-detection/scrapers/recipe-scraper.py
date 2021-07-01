import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options


def switch_to_recipe_tab():
    main_window = driver.current_window_handle
    windows = driver.window_handles

    for window in windows:
        if(window != main_window):
            driver.switch_to.window(window)
            break

    time.sleep(0.9)

def get_elements(css_selector, document=None, all=True):
    if not document: document = driver
    try:
        if all: return document.find_elements_by_css_selector(css_selector)
        return document.find_element_by_css_selector(css_selector)
    except NoSuchElementException:
        return None

def scrape_recipe_ingredients():
    full_recipe = WebDriverWait(driver, 100).until(
      EC.presence_of_element_located((By.LINK_TEXT, "CLICK TO SEE FULL RECIPE"))
    )
    full_recipe.click()

    ingredients = WebDriverWait(driver, 100).until(
      EC.presence_of_element_located((By.CLASS_NAME, "recipe-ingredients__list"))
    )
    
    items = get_elements(".recipe-ingredients__item", ingredients)
    ITEMs = []
    for item in items:
        ITEM = {}
        heading = get_elements(".recipe-ingredients__ingredient-heading", item, False)
        if heading: ITEM["heading"] = heading.text

        ingredient = get_elements(".recipe-ingredients__ingredient", item, False)
        if ingredient:
            quantity = get_elements(".recipe-ingredients__ingredient-quantity", item, False)
            if quantity: ITEM["quantity"] = quantity.text
            parts = get_elements(".recipe-ingredients__ingredient-parts", item, False)
            if parts: ITEM["ingredient"] = parts.text
        ITEMs.append(ITEM)
    
    return ITEMs

def scrape_recipe_directions():
    directions = WebDriverWait(driver, 100).until(
      EC.presence_of_element_located((By.CLASS_NAME, "recipe-directions"))
    )

    steps = get_elements(".recipe-directions__step", directions)
    DIRECTIONs = []
    for step in steps:
        DIRECTIONs.append(step.text)
    
    return DIRECTIONs

def scrape_recipe_basics():
    name = get_elements(".recipe-title", all=False)
    if name: name = name.text
    
    ready_in = get_elements(".recipe-facts__time", all=False)
    if ready_in: ready_in = ready_in.text.replace("READY IN:", "").strip()
    
    serves = get_elements(".recipe-facts__servings", all=False)
    if serves: serves = serves.text.replace("SERVES:", "").strip()

    return (name, ready_in, serves)


def scrape_recipe():
    reply = {
        "status": None, 
        "page": driver.title,
        "url": driver.current_url,
        "data": None,
    }
    try:
        ingredients = scrape_recipe_ingredients()
        directions = scrape_recipe_directions()
        name, ready_in, serves = scrape_recipe_basics()
        reply["status"] = "SUCCESS"
        reply["data"] = {
            "name": name,
            "ready_in": ready_in,
            "serves": serves,
            "url": driver.current_url,
            "directions": directions,
            "ingredients": ingredients,
        }
    except Exception as err:
        reply["status"] = "ERROR"
        reply["data"] = err
    finally:
        driver.close()
    return reply

def store_as_json(file_name, data):
    json_data = json.dumps(data, indent = 4)
    with open(file_name, "w") as file:
        file.write(json_data)



def scrape_recipes(url):
    driver.get(url)
    main_window = driver.current_window_handle
    recipes = get_elements(".recipe")

    RECIPEs = []
    ERRORed = []
    for recipe in recipes:
        recipe.click()
        switch_to_recipe_tab()
        reply = scrape_recipe()
        
        if reply["status"] == "SUCCESS":
            RECIPEs.append(reply["data"])
            print(f"SUCCESSfully scraped {reply['page']}")
        else:
            ERRORed.append(reply)
            print("-----------------------------------------------------")
            print(f"ERROR in scraping {reply['page']}")
            print(reply["url"])
            print(reply["data"])
            print("-----------------------------------------------------")

        driver.switch_to.window(main_window)
    
    store_as_json("recipes.json", RECIPEs)
    print("ERRORED SCRAPES: ", ERRORed)
    print("ALL DONE!")
    
if __name__=='__main__':
    CHROMEDRIVER_PATH = "./chromedriver.exe"
    DEBUG = False

    options = Options()
    options.headless = not DEBUG
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(CHROMEDRIVER_PATH, options=options)
    scrape_recipes("https://www.food.com/ideas/4th-of-july-side-dishes-6993#c-816635")
    driver.quit()