from datetime import date
from threading import Thread
from playwright.sync_api import sync_playwright
import time


class ScreenshotScanner:
    def __init__(self, assets: list):
        self.assets = assets

    def scan_one_page(self, asset: str):
        try:
            print("Trying asset : {asset}".format(asset=asset))
            with sync_playwright() as p:
                browser = p.chromium.launch()
                context = browser.new_context(ignore_https_errors=True)
                page_https = context.new_page()
                page_http = context.new_page()

                page_https.goto(
                    "https://{asset}".format(asset=asset), timeout=5000)
                page_https.screenshot(
                    path="screenshots/{date}/https/{asset}.png".format(date=date.today(), asset=asset), full_page=True, timeout=5000)

                page_http.goto(
                    "http://{asset}".format(asset=asset), timeout=5000)
                page_http.screenshot(
                    path="screenshots/{date}/http/{asset}.png".format(date=date.today(), asset=asset), full_page=True, timeout=5000)
                context.close
        except Exception as e:
            print(str(e))
            return False
        else:
            return True

    def process(self):
        threads = []
        start = time.time()
        for asset in self.assets:
            x = Thread(target=self.scan_one_page, args=(asset.strip(),))
            x.start()
            threads.append(x)
        for thread in threads:
            thread.join()
        end = time.time()
        print(format(end-start))


with open("iptest.txt", "r") as file:
    assets = file.readlines()
d = ScreenshotScanner(assets)
d.process()
