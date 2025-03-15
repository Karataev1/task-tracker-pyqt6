import logging
from colorama import init, Fore, Back, Style

logging.basicConfig(
    filename='debug_log.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


class Debug:

    def __init__(self,prog_name,prog_ver,status=True,sql_conn=None):
        self.prog_name = prog_name
        self.prog_ver = prog_ver
        self.sql_data_base = sql_conn
        self.status = status

        self.send('Debug enabled')
        self.send(f'{self.prog_name} started! Version {self.prog_ver}')

    def send(self,mess:str):
        if self.status:
            print(f'{Fore.BLUE}[debug]{Style.RESET_ALL} {mess}')
            logging.debug(mess)

    def error(self,mess:str):
        if self.status:
            print(f'{Fore.RED}[debug] [error]{Style.RESET_ALL} {mess}')
            logging.error(mess)

    def send_task_list(self):
        if self.status:
            task_list = self.sql_data_base.get_task_data()
            for idd, item in enumerate(task_list['TaskList']):
                self.send(f'[{idd}] [dbID:{item['id']}] '
                                    f'[name:`{item['name']}`]'
                                    f'\t\t[type:{item['type']}]'
                                    f'\t\t[text:{item['text']}]'
                                    f'\t\t[date:{item['date']}]')