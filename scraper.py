from time import sleep
from selenium import webdriver
import pandas as pd
import glob
import os

pd.set_option('display.max_columns', None)

# User config:
city_to_scrape = 'chicago'
min_sf = 500
max_sf = 1000
start_page = 1  # Start scraping from this page number
save_page_interval = 12  # Create csv after scraping these many number of pages


class Driver:
    """
    path: Web driver path, eg: Chrome, Firefox
    options: list of web driver options
    This creates a webdriver object with options.
    """

    def __init__(self, path, options=()):
        self.path = path
        self.options = options
        # self.driver_options = webdriver.ChromeOptions()
        # for option in self.options:
        # self.driver_options.add_argument(option)
        self.driver = webdriver.Firefox(executable_path=path)

    def click_button_xpath(self, tag_value):
        """Finds the element using xpath. If found, clicks it."""
        button = self.driver.find_elements_by_xpath(tag_value)
        if len(button) > 0:
            self.driver.execute_script("arguments[0].click();", button[0])

    def get_element_list(self, tag_value):
        """Get a list of elements from an xpath"""
        return self.driver.find_elements_by_xpath(tag_value)

    def execute_script(self, code, element):
        """Executes script"""
        return self.driver.execute_script(code, element)

    def current_url(self):
        """Gets current URL"""
        return self.driver.current_url

    def page_source(self):
        """Gets page source"""
        return self.driver.page_source

    def back(self):
        """Takes the driver 1 page back"""
        return self.driver.back()

    def close(self):
        """closes the driver"""
        return self.driver.close()


web_driver_path = '/Users/khugel01/Downloads/geckodriver'
driver_options = ('--ignore-certificate-errors',
                  # '--incognito',
                  # '--headless'
                  )
driver = Driver(web_driver_path, driver_options)

username = 'lu.han@rotman.utoronto.ca'
password = 'Toronto123'

# Upwork Login
driver.driver.get('https://product.costar.com')
driver.driver.maximize_window()
sleep(3)
driver.get_element_list("//input[@id='username']")[0].send_keys(username)
driver.get_element_list("//input[@id='password']")[0].send_keys(password)
driver.get_element_list("//button[@id='loginButton']")[0].click()

sleep(6)

# Get search results
driver.driver.get('http://product2.costar.com/LeaseComps/Search/Index/US')
sleep(10)
driver.get_element_list("//span[text()='Market']")[0].click()
sleep(1)
driver.get_element_list("//input[@id='geographySearchFilter']")[0].send_keys(city_to_scrape)
sleep(1)
driver.get_element_list("//a[@id='addAllGeography']")[0].click()
sleep(1)
driver.get_element_list("//a[@id='applyGeographySelection']")[0].click()
sleep(10)
# driver.get_element_list("//a[@id='clear-criteria-top']")[0].click()
driver.get_element_list("//input[@id='AreaLeasedRangemin-clone']")[0].click()
sleep(1)
driver.get_element_list("//input[@id='AreaLeasedRangemin']")[0].send_keys(min_sf)
driver.get_element_list("//input[@id='AreaLeasedRangemax-clone']")[0].click()
sleep(1)
driver.get_element_list("//input[@id='AreaLeasedRangemax']")[0].send_keys(max_sf)
driver.get_element_list("//a[@id='view-results-top']")[0].click()

sleep(20)

# Parse Data
num_of_pages = int(driver.get_element_list("//span[@class='label pages']")[0].text)

print('Manually Resize all columns manually to fit all columns in screen')
sleep(130)

column_elements = driver.driver.find_element_by_xpath("//div[@id='contentleaseCompsGrid']").find_element_by_xpath(
    ".//div[@id='columntableleaseCompsGrid']").find_elements_by_xpath(".//div[@role='columnheader']")

column_names = []
for i in range(len(column_elements)):
    if i > 0:
        column_names.append(column_elements[i].find_element_by_xpath(".//span").text)

df = pd.DataFrame(columns=column_names)

csv_count = 0
driver.get_element_list("//input[@class='page' and @type='text']")[0].clear()
driver.get_element_list("//input[@class='page' and @type='text']")[0].send_keys(start_page)
driver.get_element_list("//button[@class='jump']")[0].click()
sleep(8)

if not os.path.exists(f'leasecomps_{city_to_scrape}_sf_{min_sf}_{max_sf}'):
    os.makedirs(f'leasecomps_{city_to_scrape}_sf_{min_sf}_{max_sf}')

for page_count in range((num_of_pages - (start_page - 1)) + 1):
    if page_count > 0:
        for k in range(5):
            rows = driver.driver.find_elements_by_xpath(
                ".//div[contains(@id,'row') and contains(@id,'leaseCompsGrid')]")
            for i in range(len(rows) - 2):
                id_value = 'row' + str(i) + 'leaseCompsGrid'
                # for j in range(len(column_names)):
                entry = {}
                for j in range(len(column_names)):
                    entry[column_names[j]] = \
                        rows[i].find_elements_by_xpath(".//div[contains(@class,'cellContent')]")[j].text
                df = df.append(entry, ignore_index=True)
            if k == 4:
                break
            scroll_down = driver.get_element_list("//div[@id='jqxScrollBtnDownverticalScrollBarleaseCompsGrid']")
            for _ in range(20):
                scroll_down[0].click()
                sleep(0.1)
        # Move to next page
        print(page_count)
        if page_count % save_page_interval == 0:
            df.to_csv(
                f'leasecomps_{city_to_scrape}_sf_{min_sf}_{max_sf}/leasecomps_{start_page + (csv_count * save_page_interval)}_{(page_count - 1) + start_page}.csv')
            df = df[0:0]  # Empty dataframe
            csv_count = csv_count + 1
        if page_count == num_of_pages - (start_page - 1):
            df.to_csv(
                f'leasecomps_{city_to_scrape}_sf_{min_sf}_{max_sf}/leasecomps_{start_page}_{(page_count - 1) + start_page}.csv')
            break
        driver.get_element_list("//input[@class='page' and @type='text']")[0].clear()
        driver.get_element_list("//input[@class='page' and @type='text']")[0].send_keys(page_count + start_page)
        # driver.execute_script("arguments[0].click();", driver.get_element_list("//button[@class='jump']")[0])
        driver.get_element_list("//button[@class='jump']")[0].click()
        sleep(8)

        # For safety scroll back up fully, before scraping that page.
        scroll_up = driver.get_element_list("//div[@id='jqxScrollBtnUpverticalScrollBarleaseCompsGrid']")
        for _ in range(105):
            scroll_up[0].click()
            sleep(0.1)

# Combine all csv into 1 final csv

path = f'leasecomps_{city_to_scrape}_sf_{min_sf}_{max_sf}/'
all_files = glob.glob(path + "/*.csv")

li = []

for filename in all_files:
    df = pd.read_csv(filename, index_col=0)
    li.append(df)

frame = pd.concat(li, axis=0, ignore_index=True)
frame.drop_duplicates(ignore_index=True).to_csv(f'leasecomps_{city_to_scrape}_sf_{min_sf}_{max_sf}/final.csv')
