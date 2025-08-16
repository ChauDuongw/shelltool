"""sudo apt-get update
sudo apt-get install -y xvfb
sudo apt-get install -y x11-xkb-utils
sudo apt-get install -y xfonts-base
sudo apt-get install -y chromium-browser
pip install playwright
playwright install"""
import asyncio
import logging
import random
import os
import subprocess
from playwright.async_api import Playwright, async_playwright, expect, BrowserContext, Page

# --- Cấu hình trình duyệt ---
def get_random_browser_config_inner():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    DIVERSE_LINUX_CHROME_USER_AGENTS = [
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    ]
    selected_user_agent = random.choice(DIVERSE_LINUX_CHROME_USER_AGENTS)
    FIXED_VIEWPORT = {"width": 1280, "height": 800}
    selected_viewport = FIXED_VIEWPORT
    base_args = [
        "--no-sandbox", "--disable-setuid-sandbox", "--disable-dev-shm-usage",
        "--disable-features=site-per-process", "--disable-accelerated-2d-canvas",
        "--no-first-run", "--no-default-browser-check", "--disable-notifications",
        "--disable-popup-blocking", "--disable-infobars",
        "--disable-blink-features=AutomationControlled", "--disable-background-networking",
        "--disable-background-timer-throttling", "--disable-backgrounding-occluded-windows",
        "--disable-renderer-backgrounding", "--disable-breakpad",
        "--disable-component-update", "--disable-domain-reliability", "--disable-sync",
        "--enable-automation", "--disable-extensions", "--disable-software-rasterizer",
        "--mute-audio", "--autoplay-policy=no-user-gesture-required",
    ]
    chrome_args = base_args + [f"--window-size={selected_viewport['width']},{selected_viewport['height']}"]
    random.shuffle(chrome_args)
    return selected_user_agent, selected_viewport, chrome_args
async def login_gmail(email: str, password: str):
    ua, vp, args = get_random_browser_config_inner()
    async with async_playwright() as p:
        # Chạy trình duyệt với chế độ có GUI
        browser = await p.chromium.launch(headless=False, args=args)
        context: BrowserContext = await browser.new_context(
            user_agent=ua,
            viewport=vp,
            locale='en-US',
            timezone_id="Asia/Ho_Chi_Minh",
            geolocation={"longitude": 106.660172, "latitude": 10.762622, "accuracy": 100},
            permissions=["geolocation"],
            extra_http_headers={"Accept-Language": "en-US,en;q=0.9"}
        )
        await context.add_init_script("""Object.defineProperty(navigator, 'webdriver', { get: () => undefined });""")
        page = await context.new_page()

        async def Dangnhap():
            while True:
                try:
                    await page.goto("https://accounts.google.com")
                    print("🔐 Đang mở trang đăng nhập Gmail...")
                    await page.get_by_role("textbox", name="Email or phone").fill(email, timeout=60000)
                    await page.get_by_role("button", name="Next").click()
                    await page.wait_for_selector('input[type="password"]', timeout=60000)
                    await page.locator('input[type="password"]').fill(password)
                    await page.get_by_role("button", name="Next").click()
                    await asyncio.sleep(5)
                    print("Dang nhap thanh cong")
                    break
                except Exception as e:
                    print(f"Dang nhap that bai. Thuc hien dang nhap lai. Loi: {e}")
        async def ThaoTacCloudShell():
            while True:
                try:
                    print("truy cap trang https://shell.cloud.google.com ")
                    await page.goto("https://shell.cloud.google.com", timeout=500000)
                    async with page.expect_popup() as popup_info:
                        await page.get_by_role("button", name="Authorize").click()
                    page1 = await popup_info.value
                    await asyncio.sleep(3)
                    if page1:
                        try:
                            await page1.wait_for_selector('input[type="password"]', timeout=60000)
                            await page1.locator('input[type="password"]').fill(password)
                            await page1.get_by_role("button", name="Next").click()
                        except:
                           if page1: 
                            await page1.close()
                    print("Đã thực thi lệnh thành công.")
                    await asyncio.sleep(10) 
                    break
                except Exception as e:
                    print(f"Thao tac that bai. Thuc hien lai quy trinh. Loi: {e}")
        await Dangnhap()
        await ThaoTacCloudShell()
        while True:
         await ThaoTacCloudShell()
         await asyncio.sleep(1200)

        await browser.close()
    return
async def main():
    email = "maillll"
    pw = "Lananh255"
    await login_gmail(email, pw)

if __name__ == "__main__":
    asyncio.run(main())
