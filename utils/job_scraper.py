
from playwright.async_api import async_playwright

async def extract_job_from_url(url:str):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url,wait_until="networkidle")
        title=await page.locator("h1").inner_text()
        company = await page.locator("a[href*='/company/']").first.inner_text()
        description = await page.locator(
            "div.show-more-less-html__markup"
        ).inner_text()
        await browser.close()

        return {
            "title": title,
            "company":company,
            "description": description
        }

