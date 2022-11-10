from threading import Thread
import requests


class DomainScanner:
    def __init__(self, domain: list, subdomains: list):
        requests.packages.urllib3.disable_warnings()
        self.domain = domain
        self.subdomains = subdomains
        self.discovered_subdomains = []

    def scan_one_subdomain(self, subdomain) -> bool:
        url = "http://{subdomain}.{domain}".format(
            subdomain=subdomain, domain=self.domain)
        try:
            #print("Trying subdomain : {url}".format(url=url))
            requests.get(url)
            self.discovered_subdomains.append(subdomain)
        except Exception as e:
            # print(str(e))
            return False
        else:
            print(subdomain)
            return True

    def process(self):
        threads = []
        for subdomain in self.subdomains:
            x = Thread(target=self.scan_one_subdomain,
                       args=(subdomain.strip(),))
            x.start()
            threads.append(x)
        for thread in threads:
            thread.join()

        result = {
            "domain": self.domain,
            "subdomains": self.discovered_subdomains
        }
        return result


with open("domains.txt", "r") as file:
    subdomains = file.readlines()
    ds = DomainScanner(
        ["malteurop.com", "vivescia.com", "google.com"], subdomains)
    result = ds.process()
    print(str(result))
