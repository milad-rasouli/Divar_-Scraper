import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        # Launch a browser (you can use 'firefox', 'webkit', or 'chrome')
        browser = await p.chromium.launch(headless=False)  # Set headless=True to run without a GUI
        page = await browser.new_page()

        # Navigate to the URL
        url = 'https://divar.ir/v/%D9%BE%D8%B1%D8%A7%DB%8C%D8%AF-111%D9%81%D9%88%D9%84-%DB%B1%DB%B3%DB%B9%DB%B3/wZPgVDV2'
        await page.goto(url)

        # Wait for the specific content to load
        await page.wait_for_selector('article')

        # Extract the desired information
        title = await page.locator('.kt-page-title__title').inner_text()
        subtitle = await page.locator('.kt-page-title__subtitle').inner_text()
        
        # Extract details from the table
        mileage = await page.locator('table.kt-group-row tbody tr td:nth-child(1)').inner_text()
        model_year = await page.locator('table.kt-group-row tbody tr td:nth-child(2)').inner_text()
        color = await page.locator('table.kt-group-row tbody tr td:nth-child(3)').inner_text()

        # Print the extracted information
        print(f'Title: {title}')
        print(f'Subtitle: {subtitle}')
        print(f'Mileage: {mileage}')
        print(f'Model Year: {model_year}')
        print(f'Color: {color}')

        # Close the browser
        await browser.close()

# Run the async main function
asyncio.run(main())
