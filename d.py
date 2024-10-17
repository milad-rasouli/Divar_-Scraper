import os
import requests
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def fetch_description(url):
    # print("Starting fetch_description")
    firefox_options = FirefoxOptions()
    firefox_options.add_argument("--headless")  
    firefox_options.add_argument("--no-sandbox")
    firefox_options.add_argument("--disable-dev-shm-usage")
    firefox_options.set_preference("toolkit.telemetry.enabled", False)
    firefox_options.set_preference("toolkit.telemetry.unified", False)

    # Use the installed Geckodriver directly
    driver = webdriver.Firefox(service=FirefoxService(), options=firefox_options)

    image_url = None  # Initialize image_url

    try:
        # print("Navigating to URL:", url)
        driver.get(url)

        # Wait for the title element to be present
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'h1.kt-page-title__title')))

        title = driver.find_element(By.CSS_SELECTOR, 'h1.kt-page-title__title').text
        subtitle = driver.find_element(By.CSS_SELECTOR, 'div.kt-page-title__subtitle').text
        mileage = driver.find_element(By.CSS_SELECTOR, 'td.kt-group-row-item__value:nth-child(1)').text
        model_year = driver.find_element(By.CSS_SELECTOR, 'td.kt-group-row-item__value:nth-child(2)').text
        color = driver.find_element(By.CSS_SELECTOR, 'td.kt-group-row-item__value:nth-child(3)').text
        
        image_element = driver.find_element(By.CSS_SELECTOR, 'figure.kt-base-carousel__figure img.kt-image-block__image')
        image_url = image_element.get_attribute('src') if image_element else None

        description = driver.find_element(By.CSS_SELECTOR, 'div.kt-base-row.kt-description-row div.kt-base-row__start p.kt-description-row__text.kt-description-row__text--primary').text

    except Exception as e:
        print("An error occurred:", e)
    finally:
        print("Closing the driver")
        driver.quit()  # Ensure the driver is closed

    image_path = None
    if image_url:
        image_path = download_image(image_url)

    return color, description, image_path



def download_image(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  

        image_name = os.path.basename(url)

        img_directory = 'img'
        
        if not os.path.exists(img_directory):
            os.makedirs(img_directory)

        image_path = os.path.join(img_directory, image_name)

        with open(image_path, 'wb') as file:
            file.write(response.content)
        
        return os.path.abspath(image_path)
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while downloading the image: {e}")
        return None  

# Example usage
# url = 'https://divar.ir/v/%D8%AA%D9%8A%D8%A8%D8%A7-2-%D9%87%D8%A7%DA%86%D8%A8%D9%83-ex-%D9%85%D8%AF%D9%84-%DB%B1%DB%B3%DB%B9%DB%B3/wZRgD1iF'
# c, d,ip = fetch_description(url)
# print(c, d, ip)