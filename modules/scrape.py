from requests import Session
from csv import reader

# -----------------------------------------------

class Scraper(Session):
    def __init__(self: object) -> None:
        super().__init__()
        self.list_ips: list = []
        self.urlhaus()

    def urlhaus(self: object) -> None:
        cache: list = []

        for endpoint in ('recent', 'online'):
            mirai_list: list = reader(self.get(url = f'https://urlhaus.abuse.ch/downloads/csv_{endpoint}/').text.split('\n'))

            for line in mirai_list:
                try:
                    line_str: str = ','.join(line)
                    if (len(line) != 0) and ('mirai' in line_str or 'x86' in line_str or 'bins.sh' in line_str or 'botnetofthings' in line_str):
                        ip: str = str(line).split('/')[2]
                        arch: str = f'{str(line).split("/")[3]}/{str(line).split("/")[4]}'.split("',")[0]
                        
                        if ip.count('.') == 3:
                            if not ip in cache:
                                cache.append(ip)
                                
                                if ':' in ip:
                                    data: dict = {'ip': ip[:ip.index(':')], 'arch': arch}
                                else:
                                    data: dict = {'ip' : ip, 'arch': arch}
                                    
                                if not data in self.list_ips:
                                    self.list_ips.append(data)
                except:
                    continue