from colorama import Fore

class Application:

    def __init__(self,
                 sql_data_base:object,
                 ui: object,
                 debug: object):

        self.sql_data_base = sql_data_base
        self.ui = ui
        self.debug = debug

        self.debug.send(f'{Fore.GREEN}[Application] self.sql_data_base: {self.sql_data_base}')
        self.debug.send(f'{Fore.GREEN}[Application] self.ui: {self.ui}')


    def start(self):

        self.ui.show_form('task_list')
        self.ui.task_list.update_list()
        self.debug.send_task_list()




