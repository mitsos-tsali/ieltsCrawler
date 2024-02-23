from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from apscheduler.schedulers.background import BlockingScheduler
from typing import Final
import traceback

seconds: Final[int] = 1200

options = Options()
# options.add_argument('--disable-dev-shm-usage')
# options.add_argument("--headless=new")
options.add_argument("--start-minimized")
sched = BlockingScheduler()

try:
    def checkDates():
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get("https://ieltsregistration.britishcouncil.org/ors/find-test")
        
        cookies_accept = WebDriverWait(driver,6).until(EC.presence_of_element_located((By.XPATH, '//*[@id="onetrust-accept-btn-handler"]')))
        cookies_accept.click()
        academic_ielts = WebDriverWait(driver,4).until(EC.presence_of_element_located((By.ID, 'select-ac')))
        academic_ielts.click()
        book_ielts = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="app-container"]/div/article/div[2]/div/div/div[3]/button')))
        book_ielts.click()
        click_country = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, '//*[@id="select-country"]/div[2]/ul/li[44]/button')))
        click_country.click()
        city_input = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, '//*[@id="select-location"]/div[2]/ul/li[7]/button')))
        city_input.click()
        all_dates = WebDriverWait(driver,2).until(EC.presence_of_element_located((By.XPATH, '//*[@id="app-container"]/div/article/div[2]/div/div/div/div[5]/div[2]/label/input')))
        all_dates.click()
        show_dates = WebDriverWait(driver,2).until(EC.presence_of_element_located((By.XPATH,'//*[@id="app-container"]/div/article/div[2]/div/div/div/div[6]/button')))
        show_dates.click()
        dates_table = WebDriverWait(driver,2).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'css-1gklrnv')))
        print("===== Length: %2d =====" % (len(dates_table)))
        
        if int(dates_table[0].get_attribute("data-examid")) < 6106484:
            print("DATE FOUND")
            exit(2)
        driver.quit()
        
    sched = BlockingScheduler()
    sched.add_job(checkDates, trigger='interval', seconds=seconds)
    sched.start()
except Exception as e:
    traceback.print_exc(e)
    exit(400)