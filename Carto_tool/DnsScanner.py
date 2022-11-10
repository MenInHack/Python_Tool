import dns.resolver
from threading import Thread


class DNSScanner:
    def __init__(self, domain: str):
        self.domain = domain
        self.dns_type_list = ["A","TXT","AAAA","NS","CNAME","MX","SRV","DNAME","SOA","DNSKEY"]
        self.dns_record = {}
        # {"A":[],"TXT":[]}

    def scan_one_dns(self,dns_type) :
        try:
            resolver = dns.resolver.Resolver()
            resolver.nameservers = ['8.8.8.8']
            answers = resolver.resolve(self.domain, dns_type)
            self.dns_record[dns_type] = []
            entries = []
            
            for d in answers:
                entries.append(d.to_text())
            self.dns_record.append(entries)
        except Exception as e:
            print(e)
            return False
        else:
            return True

    def process(self):
        threads = []
        for dns_type in self.dns_type_list:
            x = Thread(target=self.scan_one_dns, args=(dns_type,))
            x.start()
            threads.append(x)
        for thread in threads:
            thread.join()
        result = {
            "domain":self.domain,
            "dns_record":self.dns_record
        }
        return result

ds = DNSScanner("ajouter ici le domaine")
result = ds.process()
print(str(result))

