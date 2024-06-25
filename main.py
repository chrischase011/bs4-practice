from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import psutil

def is_driver_running():
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if 'chromedriver.exe' in proc.name() or 'geckodriver.exe' in proc.name():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

def close_driver():
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if 'chromedriver' in proc.info['name'] or 'geckodriver' in proc.info['name']:
                pid = proc.pid
                driver_process = psutil.Process(pid)
                driver_process.terminate()
                driver_process.wait(timeout=5)  # Wait for the process to terminate
                print(f"Closed existing WebDriver process with PID {pid}.")
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

def run_scraper(): 
    if is_driver_running():
        close_driver()
    
    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    driver.get('https://github.com/chrischase011')

    page_source = driver.page_source

    soup = BeautifulSoup(page_source, 'lxml')

    # Example: Find the title of the page
    title = soup.find('title').get_text()
    print(title)

    userName = soup.find('span', class_='p-name vcard-fullname d-block overflow-hidden').get_text()
    print("Github Username: ", userName)

    # print(soup.prettify())

    input("Press Enter to close the browser...")

    # Close the WebDriver
    driver.quit()

if __name__ == '__main__':
    run_scraper()
