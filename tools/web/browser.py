import asyncio
from typing import Optional, Dict, Any, List
import os


class PlaywrightBrowser:
    def __init__(self, headless: bool = False):
        self.headless = headless
        self.browser = None
        self.context = None
        self.page = None

    async def start(self):
        try:
            from playwright.async_api import async_playwright
            self.playwright = await async_playwright().start()
            self.browser = await self.playwright.chromium.launch(headless=self.headless)
            self.context = await self.browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            )
            self.page = await self.context.new_page()
        except ImportError:
            print("请先安装: pip install playwright")
            print("然后运行: playwright install")
            raise

    async def goto(self, url: str, wait_until: str = 'networkidle'):
        if not self.page:
            await self.start()
        await self.page.goto(url, wait_until=wait_until)

    async def screenshot(self, path: str, full_page: bool = False):
        if not self.page:
            return
        await self.page.screenshot(path=path, full_page=full_page)

    async def get_text(self, selector: str) -> Optional[str]:
        if not self.page:
            return None
        try:
            return await self.page.inner_text(selector)
        except:
            return None

    async def click(self, selector: str):
        if not self.page:
            return
        await self.page.click(selector)

    async def fill(self, selector: str, value: str):
        if not self.page:
            return
        await self.page.fill(selector, value)

    async def get_html(self) -> Optional[str]:
        if not self.page:
            return None
        return await self.page.content()

    async def evaluate(self, script: str) -> Any:
        if not self.page:
            return None
        return await self.page.evaluate(script)

    async def close(self):
        if self.browser:
            await self.browser.close()
        if hasattr(self, 'playwright'):
            await self.playwright.stop()


def run_browser_task(task):
    loop = asyncio.get_event_loop_policy().get_event_loop()
    return loop.run_until_complete(task)
