from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

driver_path = 'C:/Users/ncare/edgedriver_win64/msedgedriver.exe'

# Initialize the web driver
service = Service(driver_path)
options = webdriver.EdgeOptions()
options.add_argument('--headless')  
driver = webdriver.Edge(service=service, options=options)

# URL of the website to scrape
url = 'https://www.foratravel.com/advisors?destination='

list_of_countries = [("austria", "Austria"), ("belgium", "Belgium"),
                     ("croatia", "Croatia"), ("czech-republic", "Czech Republic"), ("denmark", "Denmark"), ("finland", "Finland"),
                     ("france", "France"), ("germany", "Germany"), ("greece", "Greece"), ("hungary", "Hungary"), ("iceland", "Iceland"),
                     ("ireland", "Ireland"), ("italy", "Italy"), ("malta", "Malta"), ("montenegro", "Montenegro"), ("netherlands", "Netherlands"), 
                     ("norway","Norway"), ("poland", "Poland"), ("portugal","Portugal"), 
                     ("slovenia", "Slovenia"), ("spain", "Spain"),("sweden", "Sweden"), ("switzerland", "Switzerland"), ("turkiye", "Türkiye")
                     ]


advisors = []
countries = []
eu_countries = []

def scrape_page(country, eu):
    try:
        list_of_advisors = driver.find_elements(By.XPATH, "//h5[contains(@class, 'fora-text-h')]")

        for item in list_of_advisors:
            advisors.append(item.text)
            countries.append(country)
            eu_countries.append(eu)

    except Exception as e:
        print(f"Error finding venue list items: {e}")


def pagination(country, eu):
    while True:
        scrape_page(country, eu)
        try:
            next_button = driver.find_element(By.XPATH, "/html/body/div[1]/div/main/section[2]/ol/li[2]/a")

            print(f"Found 'Next' button for {country}. Clicking it.")
            print(next_button)
            
            next_button.click()
            time.sleep(5)  # Wait for the next page to load
        except Exception as e:
            print(f"No more pages to scrape for {country}. Moving to next country")
            break

for country in list_of_countries:
    driver.get(url+country[0])
    driver.implicitly_wait(5)
    pagination(country[0], country[1])

driver.quit()


data = pd.DataFrame({
    'Advisor': advisors,
    'Country': countries,
    'EU-Country': eu_countries
})

# Save the data to a CSV file
data.to_csv('travel_advisors.csv', index=False)

print("Scraping completed and data saved")

