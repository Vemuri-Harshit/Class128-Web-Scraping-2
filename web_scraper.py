from selenium import webdriver;
from bs4 import BeautifulSoup;
import requests;
import time;
import csv;

url = 'https://exoplanets.nasa.gov/discovery/exoplanet-catalog/';
browser = webdriver.Chrome('/Users/dell/OneDrive/Documents/harshit/Coding/White hat junior downloads/Python/Class 128 - We Scraping/chromedriver')
browser.get(url);
headers = ['name', 'light_years_from_earth', 'planet_mass', 'stellar_magnitude', 'discovery_date', 'hyperlink', 'planet_type', 'planet_radius', 'orbital_radius', 'orbital_period', 'eccentricity']
planet_data = [];
complete_planet_data = [];
time.sleep(10);

def scrape(): 

    for i in range(0, 458):
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        for ul_tag in soup.find_all('ul', attrs={'class', 'exoplanet'}): 
            li_tags = ul_tag.find_all('li')
            temp_list = []
            for index, li_tag in enumerate(li_tags):
                if index == 0: 
                    temp_list.append(li_tag.find_all('a')[0].contents[0])
                else: 
                    try :
                        temp_list.append(li_tag.contents[0]) 
                    except:
                        temp_list.append('') ;
            hyperlink_li_tag = li_tags[0]
            temp_list.append('https://exoplanets.nasa.gov' + hyperlink_li_tag.find_all('a', href = True)[0]['href']);          

            planet_data.append(temp_list)

        browser.find_element_by_xpath('//*[@id="primary_column"]/div[1]/div[2]/div[1]/div/nav/span[2]/a')

def scrape_of_planets(hyperlink):
    try:
        page = requests.get(hyperlink)
        soup = BeautifulSoup(page.content, 'html.parser')
        temp_list = []

        for tr_tag in soup.find_all('tr', attrs={'class', 'fact_row'}):
            td_tags = tr_tag.find_all('td');
            for td_tag in td_tags: 
                try:
                    temp_list.append(td_tag.find_all('div', attes = {'class', 'value'})[0].contents[0])
                except:  
                    temp_list.append('') ;

        complete_planet_data.append(temp_list)            
    
    except:
        time.sleep(1);
        scrape_of_planets(hyperlink)   

scrape();        

for index,data in enumerate(planet_data): 
    scrape_of_planets(planet_data[5])

final_data  = [];

for index,data in enumerate(planet_data):
    new_element = complete_planet_data[index] 
    new_element = [elm.replace('\n', '') for elm in new_element]
    new_element = new_element[:7];
    final_data.append(data + new_element);

with open('scraper.csv', 'w') as f:
    writer = csv.writer(f);
    writer.writerow(headers);
    writer.writerows(final_data);