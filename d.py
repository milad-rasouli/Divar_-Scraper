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

        description = page.query_selector('div.kt-base-row__start p.kt-description-row__text').inner_text()

        print(f'Title: {title}')
        print(f'Subtitle: {subtitle}')
        print(f'Mileage: {mileage}')
        print(f'Model Year: {model_year}')
        print(f'Color: {color}')
        print(f'Description: {description}')

        browser.close()
        return color,description

# url = 'https://divar.ir/v/%D9%BE%D8%B1%D8%A7%DB%8C%D8%AF-111%D9%81%D9%88%D9%84-%DB%B1%DB%B3%DB%B9%DB%B3/wZPgVDV2'
# c,d = fetch_description(url)
# print(c,d)
