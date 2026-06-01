
from playwright.async_api import async_playwright

async def extract_job_from_url(url:str):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        page = await browser.new_page()
        await page.goto(url, wait_until="domcontentloaded", timeout=60000)
        
        await page.wait_for_timeout(2000)
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

