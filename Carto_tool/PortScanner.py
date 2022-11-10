import socket
from threading import Thread

class PortScanner:
    def __init__(self, ip: str, ports: list):
        self.ip = ip
        self.ports = ports
        self.opened_port = []

    def scan_one_port(self,port) -> bool:
        try:
            print("Trying port : {port}".format(port=port))
            s = socket.socket()
            s.settimeout(0.5)
            result = s.connect((self.ip, port))
            self.opened_port.append(port)
        except Exception as e:
            return False
        else:
            s.close()
            return True

    def retrieve_hostname(self):
        try:
            hostname = socket.gethostbyaddr(self.ip)
        except:
            return False
        else:
            return hostname[0]

    def process(self):
        current_hostname = self.retrieve_hostname()
        threads = []
        for port in self.ports:
            x = Thread(target=self.scan_one_port, args=(port,))
            x.start()
            threads.append(x)
        for thread in threads:
            thread.join()

        result = {
            "ip":self.ip,
            "hostname":current_hostname if current_hostname != False else None,
            "opened_ports":self.opened_port
        }
        return result


ps = PortScanner("194.30.173.4", range(1,500))
result = ps.process()
print(str(result))