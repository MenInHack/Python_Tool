from datetime import date
from threading import Thread
from playwright.sync_api import sync_playwright


class ScreenshotScanner:
    def __init__(self, assets: list):
        self.assets = assets

    def scan_one_page(self, asset: str):
        try:
            print("Trying asset : {asset}".format(asset=asset))
            with sync_playwright() as p:
                browser = p.chromium.launch()
                page = browser.new_page()
                page.goto("https://{asset}".format(asset=asset))
                page.screenshot(
                    path="screenshots/{date}/{asset}.png".format(date=date.today(), asset=asset), full_page=True)
                browser.close
        except Exception as e:
            print(str(e))
            return False
        else:
            return True

    def process(self):
        threads = []
        for asset in self.assets:
            x = Thread(target=self.scan_one_page, args=(asset,))
            x.start()
            threads.append(x)
        for thread in threads:
            thread.join()


ss = ScreenshotScanner(["ici.com", "facebook.com", "google.com"])
ss.process()
