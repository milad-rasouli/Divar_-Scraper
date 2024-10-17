import os
import requests
from playwright.sync_api import sync_playwright

def fetch_description(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        page.goto(url)
        page.wait_for_selector('article')

        title = page.query_selector('h1.kt-page-title__title').inner_text()
        subtitle = page.query_selector('div.kt-page-title__subtitle').inner_text()
        mileage = page.query_selector('td.kt-group-row-item__value:nth-child(1)').inner_text()
        model_year = page.query_selector('td.kt-group-row-item__value:nth-child(2)').inner_text()
        color = page.query_selector('td.kt-group-row-item__value:nth-child(3)').inner_text()
        # Extract the image URL
        image_element = page.query_selector('figure.kt-base-carousel__figure img.kt-image-block__image')
        image_url = image_element.get_attribute('src') if image_element else None

        # description = page.query_selector('div.kt-base-row__start p.kt-description-row__text.kt-description-row__text--primary').inner_text()        
        description = page.query_selector('div.kt-base-row.kt-description-row div.kt-base-row__start p.kt-description-row__text.kt-description-row__text--primary').inner_text()

        # print(f"d1: {description}")
        # print(f"d1: {description2}")

        # print(f'Title: {title}')
        # print(f'Subtitle: {subtitle}')
        # print(f'Mileage: {mileage}')
        # print(f'Model Year: {model_year}')
        # print(f'Color: {color}')
        # print(f'Description: {description}')
        # print("image url ", image_url)
        browser.close()

        image_path = None
        if image_url:
            image_path = download_image(image_url)
            # print(f"Image saved at: {image_path}")

        print("image path ", image_path)
        return color,description,image_path

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
        
        # print(f"Image downloaded: {image_path}")
        return os.path.abspath(image_path)
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while downloading the image: {e}")
        return None  

# Example usage
# url = "https://example.com/image.jpg"
# absolute_path = download_image(url)
# print(f"Image saved at: {absolute_path}")

# url = 'https://divar.ir/v/%D8%AA%DB%8C%D8%A8%D8%A7-2-%D9%87%D8%A7%DA%86%D8%A8%DA%A9-ex-%D9%85%D8%AF%D9%84-%DB%B1%DB%B3%DB%B9%DB%B3/wZRgD1iF'
# c,d = fetch_description(url)
# print(c,d)
