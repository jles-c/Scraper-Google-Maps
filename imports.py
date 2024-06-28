import re
import time
import unicodedata
import sys
import numpy as np
import datetime
import pandas as pd

# Selenium library
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


## 1.2) Driver acces
acces = "/Users/jules/Desktop/Scripts/chromedriver"

## 1.4) Custom functions & class
class WebDriver:

    location_data = {}

    def __init__(self, driver):
        # self.PATH = ChromeDriverManager().install()
        # self.options = Options()
        # self.options.binary_location = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"
        # #self.options.add_argument("--headless")
        # self.driver = webdriver.Chrome(self.PATH, options=self.options)
        self.driver = driver
        
        self.location_data["name"] = "NA"
        self.location_data["avg rating"] = "NA"
        self.location_data["count rating"] = "NA"
        self.location_data["location"] = "NA"
        self.location_data["contact"] = "NA"
        self.location_data["website"] = "NA"
        self.location_data['category'] = "NA"
        self.location_data['url'] = "NA"
        self.location_data['iframe'] = "NA"

    def get_iframe(self):
        share_btn = self.driver.find_element(by = By.CSS_SELECTOR, value = "button[data-value='Share']")
        share_btn.click()
        time.sleep(0.6)
        embed_btn = self.driver.find_element(by = By.CSS_SELECTOR, value = "button[aria-label='Embed a map']")
        embed_btn.click()
        time.sleep(0.2)
        iframe = self.driver.find_element(by=By.CSS_SELECTOR, value = "input[value^='<iframe']").get_attribute('value')
        return iframe
    
    def get_location_data(self, url):
        try:
            name = self.driver.find_element(by = By.TAG_NAME, value = "h1")
            self.location_data["name"] = name.text
        except:
            pass
        try:
            avg_rating = self.driver.find_element(by = By.CSS_SELECTOR, value = "div[class='F7nice ']").find_element(by = By.CSS_SELECTOR, value = "span[aria-hidden='true']")
            self.location_data["avg rating"] = re.findall("\d.\d",avg_rating.text)[0]        
        except:
            pass
        try:
            count_rating = self.driver.find_element(by = By.CSS_SELECTOR, value = "span[aria-label$='reviews']")
            self.location_data["count rating"] = re.findall("\d+",count_rating.text)[0]
        except:
            pass
        try:
            address = self.driver.find_element(by = By.CSS_SELECTOR, value = "[data-item-id='address']")
            self.location_data["location"] = address.text
        except:
            pass
        try:
            phone_number = self.driver.find_element(by = By.CSS_SELECTOR, value = "[data-item-id*='phone']")
            self.location_data["contact"] = phone_number.text
        except:
            pass
        try:
            website = self.driver.find_element(by = By.CSS_SELECTOR, value = "[data-item-id='authority']")
            self.location_data["website"] = website.text
        except:
            pass
        try:
            category = self.driver.find_element(by = By.CSS_SELECTOR, value = "button[jsaction*='.category']")
            self.location_data["category"] = category.text
        except:
            pass
        try:
            self.location_data['url'] = url
            self.location_data['iframe'] = self.get_iframe()
        except:
            pass

    def scroll_the_page(self):
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "section-layout-root")))

            pause_time = 2
            max_count = 5
            x = 0

            while(x<max_count):
                scrollable_div = self.driver.find_element(by = By.CSS_SELECTOR, value = 'div.section-layout.section-scrollbox.scrollable-y.scrollable-show')
                try:
                    self.driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', scrollable_div)
                except:
                    pass
                time.sleep(pause_time)
                x=x+1
        except:
            self.driver.quit()
            
    def scrape(self, url):
        try:
            self.driver.get(url)
        
            if self.driver.current_url.find("consent.google") > -1:
                time.sleep(1)
                self.driver.find_element(by = By.CSS_SELECTOR, value = "button[jsname=b3VHJd]").click()
                
        except Exception as e:
            print(e)
#             self.driver.quit()
            pass
            
        time.sleep(1)
        
        self.get_location_data(url)

        return self.location_data

    def reset_location_data(self):
        self.location_data["name"] = "NA"
        self.location_data["avg rating"] = "NA"
        self.location_data["count rating"] = "NA"
        self.location_data["location"] = "NA"
        self.location_data["contact"] = "NA"
        self.location_data["website"] = "NA"
        self.location_data['category'] = "NA"
        self.location_data['url'] = "NA"
        self.location_data['iframe'] = "NA"

def clean_text(text):
    '''Clean html-like str object:
    - Strip strings in between <>, /* */, and starting with &
    - Strip carriage return
    - Convert to lower case
    - Remove accents, special caracters (remove \W like strings, "_") 
    - Remove numbers 
    - Single space all words 
    - remove ≤2 letters words
    '''
    # retirer tout ce qui est entre < >, entre /* */ et toutes les entités HTML (commençant par &)
    cleaned_text = re.sub('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});', ' ', text)
    cleaned_text = re.sub('/\*.*?\*\/', ' ', cleaned_text)
    cleaned_text = re.sub('var\s(.*?);', ' ', cleaned_text)
    # retirer les retours à la ligne
    cleaned_text = cleaned_text.replace(r'\n', ' ')
    # remplacer les majuscules par des minuscules
    cleaned_text = cleaned_text.lower()
    # retirer les accents
    cleaned_text = ''.join((c for c in unicodedata.normalize('NFD', cleaned_text) if unicodedata.category(c) != 'Mn'))
    # retirer les caractères spéciaux (\W inclut les espaces et la ponctuation et ASCII permet d'indiquer que tout ce qui n'est pas [a-zA-Z0-9] est un caractère spécial sauf _
    cleaned_text = cleaned_text.replace('œ', 'oe')
    cleaned_text = re.sub('\W', ' ', cleaned_text, flags = re.ASCII)
    # supprimer tous les élements avec un _
    cleaned_text = re.sub('\s([a-z]*?)_([a-z]*?)\s', ' ', cleaned_text)
    # retirer les chiffres et ce qui est collé à des lettres ou _
    cleaned_text = re.sub('[a-z_]*[0-9][a-z0-9_]*', ' ', cleaned_text)
    # rajouter des espaces avant et après chaque mot pour bien détecter la regex suivante
    cleaned_text = re.sub('\s', '  ', cleaned_text)
    # remplacer les lettres seules ou en duos seules (+ leurs espaces avant/apres) par un espace simple
    cleaned_text = re.sub('\s[a-z]{1,2}\s', ' ', cleaned_text)
    # remplacer les espaces multiples par des espaces simples
    cleaned_text = re.sub('\s+', ' ', cleaned_text)
    return cleaned_text
    
def progressBar(name, value, endvalue, bar_length = 50, width = 20):
        percent = float(value) / endvalue
        arrow = '-' * int(round(percent*bar_length) - 1) + '>'
        spaces = ' ' * (bar_length - len(arrow))
        description = str(name +" "+ str(value)+"/"+str(endvalue))
        sys.stdout.write("\r{0: <{1}} : [{2}]{3}%".format(\
                         description, width, arrow + spaces, int(round(percent*100,2))))
        sys.stdout.flush()
        if value == endvalue:     
             sys.stdout.write('\n\n')

def send_gmaps_search(search_url, driver):
    driver.get(search_url)
    # Bouton J'accepte:
    if driver.current_url.find("consent.google") > -1:
        time.sleep(1)
        driver.find_element(by = By.CSS_SELECTOR, value = "button[jsname=b3VHJd]").click()

def click_first_suggestion(driver):
    search_box_input = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,"input[id='searchboxinput']")))
    search_box_input.click()
    time.sleep(1)
    first_suggestion = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div[id='sbse0']")))
    first_suggestion.click()
    time.sleep(1)

def collect_pages_result(driver, w_websites, do_scroll = False, max_results:int = None):
    # Collect the current page results
    print('locate pane')
    pane = WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div[role='main']")))
    print("pane located")
    print('locate scroll element')
    # time.sleep(3)
    scrollbox = WebDriverWait(pane, 3).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "div[role='feed']")))
    
    # Scroll to bottom of page
    if do_scroll:
        print('scrolling...')
        scroll_to_end_of_page(driver, scrollbox)

    # Collect all results elements and add the href to results
    return list_results_with_websites_from_scrollbox(scrollbox, w_websites, max_results)

def click_next_page(driver):
    try : # Check if next page exists
        
        next_page = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[id=ppdPk-Ej1Yeb-LgbsSe-tJiF1e]")))
        next_page.click()
        next_page_exist = True
        time.sleep(1)
        
    except : 
        next_page_exist = False
    
    return next_page_exist

def no_results(driver):
    no_result=""
    try:
        pane = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, "pane")))
        no_result = WebDriverWait(pane, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div[class='V79n2d-di8rgd-aVTXAb-title']")))
        if no_result.text == 'Aucun résultat trouvé.':
            return True
        else : 
            return False
    except:
        return False

def get_date():  
    date = datetime.date.today().strftime("%Y-%m-%d")
    return date

def get_duration(start,end):
    duration = (end - start)
    hours = int(np.floor(duration/3600))
    minutes = int(np.floor(duration%3600/60)) 
    seconds = int(np.floor(duration%60))
    duration = "{}h {}min {}sec".format(hours,minutes,seconds)
    return duration

def get_unique_urls_serie(result_dict):
    """
    Take the result dict as an input (first key level = KW and second key level = cities), and return a deduplicated Serie of urls.
    """
    
    urls_list = []

    for kw in result_dict.keys():
        for city in result_dict[kw].keys():
            urls_list.append(result_dict[kw][city])

    urls_set = set(urls_list[0])
    urls_serie = pd.Series(list(urls_set))
    return urls_serie

def input_country_kw_cities(Input_city_dict, countries_dict):

    ### PICK COUNTRY TO SCRAP
    country_key = int(input("Enter number of zone to scrape : \n 1 : FR \n 2 : ES \n 3 : IT (empty) \n 4 : UK \n 5 : MX \n 6 : FR (paris arr) \n 7 : FR Test (75000)\n8 : ES Test (bcn) \n9 : custom cities (FR)"))
    locations_list = Input_city_dict[country_key]
    country = countries_dict[country_key]

    ### PICK KW TO SCRAP
    keywords_list = [input("Enter unique kw to scrape : \n")]

    ### PRINT COUNTRY AND KW
    print("country : {}\n list keywords : {}".format(country,keywords_list))

    return country, keywords_list, locations_list

def scroll_to_end_of_page(driver, scrollbox):
    time_start = time.time()
    timeout_loc = 30
    end_of_results_xpath = '//div[starts-with(@class,"PbZDve")]'
    Sx, Sy = scrollbox.location.values()
    Sx += 10
    Sy += 10
    scroll_origin = ScrollOrigin.from_viewport(Sx+10, Sy+10)

    while time.time()-time_start <= timeout_loc:
        if np.random.random()>=0.9:
            sleep = np.random.random()*2
            time.sleep(sleep)
            print(f'sleep for {sleep} secs...')
            print(f'time before timeout: {timeout_loc - (time.time()-time_start)}')
        if driver.find_elements(by = By.XPATH, value = end_of_results_xpath):
                # print("end of page")
                break

        ActionChains(driver).scroll_from_origin(scroll_origin,0,10000).perform()
        time.sleep(0.2)

def list_results_with_websites_from_scrollbox(scrollbox, w_websites, max_results:int = None):
    search_results_containers = scrollbox.find_elements(by = By.CSS_SELECTOR, value = "div[class ^= 'Nv2PK']")
    search_results = [el.find_element(by = By.CSS_SELECTOR, value = 'a[class = hfpxzc]') for el in search_results_containers]
    to_keep = []

    for elm in search_results:
        if not w_websites:
            to_keep.append(elm)
            continue

        aria_label = elm.get_attribute('aria-label')
        css = f"div[aria-label = '{aria_label}']"
        
        # To fix
        try :
            test_website = scrollbox.find_element(by = By.CSS_SELECTOR, value = css)
            test_website.find_element(by = By.CSS_SELECTOR, value = 'a[data-value*=Web]')
            to_keep.append(elm)
        except :
            continue

    # Return list of results with websites  
    if max_results:
        return [element.get_attribute("href") for element in to_keep][:max_results]

    return [element.get_attribute("href") for element in to_keep]