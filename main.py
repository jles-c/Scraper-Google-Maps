## 1.1) Imports

# Selenium library
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService


#Processing library

import pandas as pd
import time
import datetime
import re

# IMPORTS AND CUSTOM FUNCTIONS
from imports import WebDriver, clean_text, progressBar, send_gmaps_search, click_first_suggestion, collect_pages_result, click_next_page, no_results, get_date, get_duration, get_unique_urls_serie, input_country_kw_cities
from variable import Input_city_dict, countries_dict

country, keywords_list, locations_list = input_country_kw_cities(Input_city_dict, countries_dict)
do_scroll = input("Scroll to retrieve all results ? (Y/n - Press enter for yes):")
max_results = input("Max number of results : (Press enter to retrieve all results):")

if max_results == '':
    max_results = None
    print('no max results')

else:
    max_results = int(max_results)
    print(f'max results : {max_results}')

if do_scroll in ('', 'Y'):
    do_scroll = True
else:
    do_scroll = False

w_websites = input("Only results with website ? (Y/n - Press enter for yes):")

if w_websites in ('', 'Y'):
    w_websites = True
    unique_websites = input("One result per website ? (Y/n - Press enter for yes):")

    if unique_websites in ('', 'Y'):
        unique_websites = True
        print('Scraping one result per website')

    else:
        unique_websites = False
        print('Scraping all results (dont dedpulicate on website)')

else:
    w_websites = False
    unique_websites = False
    print('Scraping all results (with and w/o website)')


### COLLECT RESULTS URLs
start = time.time()
# options = Options()
#options.add_argument("--headless")
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

value = 1
endvalue = len(keywords_list)*len(locations_list)
nb_url = 0
kw_dict = dict()

for kw in keywords_list:
    
    city_dict=dict()
    
    for loc in locations_list:
        results_gmap_url = list()
        if country.lower() in loc.lower():
            url = "https://www.google.com/maps/search/" + clean_text(kw)+" "+loc
        else : 
            url = "https://www.google.com/maps/search/" + clean_text(kw)+" "+loc +" "+ country
        url+='?hl=en'
        progressBar("gmaps_search_urls...", value, endvalue, bar_length = 50, width = 20)
        value+=1
        
        try: # Check if search is already scraped
            if loc in city_dict.keys():
                continue
        except:
            pass
            
        # launch gmaps search 
        send_gmaps_search(url,driver)
        # Load variables:
        first_suggestion_checked = False   
        time.sleep(1)

        # while True:

            # try: # Collect current page results
                # time.sleep(1)
                #print("start collecting results")
        try:
            results_gmap_url += collect_pages_result(driver, w_websites, do_scroll, max_results)
        
        except:
            if re.match('/maps/place', driver.current_url):
                city_dict[loc] = [driver.current_url]
            else:
                print(f'error : {driver.current_url}')
                continue

            # except: #redirect to first_suggestion if not already checked and if not "Aucun résultat"
            #     #print("except while collecting results")
            #     if not first_suggestion_checked and not no_results(driver):
            #         # Go to first suggestion and restart collect
            #         click_first_suggestion(driver)
            #         first_suggestion_checked = True
            #         time.sleep(1)
            #         continue
                
            
            # if not click_next_page(driver):
            #     break
                       
        city_dict[loc] = results_gmap_url.copy()
    kw_dict[kw] = city_dict.copy()
# driver.quit()

end = time.time()
for key in kw_dict.keys():
    for city in kw_dict[key].keys():
        nb_url += len(kw_dict[key][city])
unique_urls = len(get_unique_urls_serie(kw_dict))
print("-"*30)
print("Duration : {}".format(get_duration(start, end)))
print("Urls scraped : {}".format(nb_url))
print("Unique urls scraped : {}".format(unique_urls))
print("-"*30+"\n")

### SCRAP INFOS FROM URLs WITH WEBSITES

start = time.time()
x = WebDriver(driver)
result_dict = dict()
url_scraped = list()
website_scraped = list()
count=1
total = 0

# Calculation of total urls to scrap:
for key in kw_dict.keys():
    for city in kw_dict[key].keys():
        total += len(kw_dict[key][city])

row_list = []
for kw in kw_dict.keys():
    for city in kw_dict[kw].keys():
        for url in kw_dict[kw][city]:
            progressBar("scraping result urls...", count, total, bar_length = 50, width = 20)
            if url not in result_dict.keys():
                print("url not in result_dict")
                
                result = x.scrape(url).copy()
                x.reset_location_data()
                # print(result)
                if not unique_websites or result['website'] not in website_scraped:
                # if result['website'] not in website_scraped:
                    result_dict[url] = {"url" : url,
                                        "city": city,
                                        "kw" : kw,
                                        "name" : result['name'],
                                        "website" : result['website'],
                                        "category" : result['category'],
                                        "contact" : result['contact'],
                                        "location" : result['location'],
                                        "avg rating" : result["avg rating"],
                                        "count rating" : result["count rating"],
                                        "iframe" : result["iframe"]}
                    website_scraped.append(result['website'])
                url_scraped.append(url)
            count+=1

x.driver.quit()
results_df = pd.DataFrame().from_dict(result_dict, orient = "index")

if unique_websites:
    results_df.drop_duplicates(subset="website", inplace = True)

results_df.reset_index(drop = True, inplace = True)
                        #   ).drop_duplicates(subset="website"

end = time.time()

ct = datetime.datetime.now()
print("current time: ", ct)
results_df['timestamp'] = ct

results_df['date'] = get_date()
results_df['duration'] = get_duration(start, end)
new_cols = results_df.columns.tolist()[1:]+results_df.columns.tolist()[:1]
results_df = results_df[new_cols] ## Move first column to last position

result_file_name = f"results/{country}_{keywords_list[0]}_{datetime.date.strftime(datetime.datetime.now(),'%Y-%m-%d-%H-%M-%S')}.csv"
results_df.to_csv(result_file_name, index=False)

print("-"*30)
print(f"Duration : {get_duration(start, end)}")
print(f"Results : {len(results_df)}")
print(f"Unique websites : {results_df['website'].nunique()}")
print(f"Results file location : {result_file_name}")
print("-"*30)

