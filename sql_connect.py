import psycopg2
from psycopg2 import OperationalError
from colorama import init, Fore, Back, Style


class WorkWithSqlDataBase:

    def __init__(self,database:str,user:str,password:str,host:str,debug):
        self.database = database
        self.user = user
        self.password = password
        self.host = host
        self.debug = debug
        self.cur = None

        try:
            self.conn = psycopg2.connect(
                database=self.database,
                user=self.user,
                password=self.password,
                host=self.host
            )
            self.cur = self.conn.cursor()
            self.debug.send(f"{Fore.MAGENTA}[SQL] Successful connection to the database | db_name = '{self.database}'")
        except OperationalError as e:
            self.debug.error(f'{Fore.MAGENTA}[SQL] [Except] no connection to bd | Error: {Fore.GREEN}{e}')

    def db_connected(self) -> bool:
        return self.cur


    def task_list_convert_into_dict(self, rows:list):
        dict_structure: dict[str, list] = {"TaskList": []}

        for item in rows:
            new_dict = dict()
            new_dict['id'] = item[0]
            new_dict['name'] = item[1]
            new_dict['type'] = item[2]
            new_dict['date'] = item[3]
            new_dict['text'] = item[4]

            dict_structure['TaskList'].append(new_dict)

        return dict_structure


    def get_task_data(self, selection=None):

        if not selection:
            query = 'SELECT * FROM task_list'
            self.cur.execute(query)
            rows = self.cur.fetchall()
            dict_rows = self.task_list_convert_into_dict(rows)

            self.debug.send(f'{Fore.MAGENTA}[SQL] {query}')

            return dict_rows

        query = "SELECT * FROM task_list WHERE id = %s;"
        params = (selection,)
        self.cur.execute(query, params)
        rows = self.cur.fetchall()

        dict_rows = self.task_list_convert_into_dict(rows)

        final_query = query.replace('%s', f"'{selection}'")
        self.debug.send(f'{Fore.MAGENTA}[SQL] {final_query}')

        return dict_rows['TaskList'][0]


    def add_task_in_sql_data_base(self,task_name:str,text='',date='2000-01-19',type_task='home'):

        query = "INSERT INTO task_list (name, text, type, date) VALUES (%s, %s, %s, %s);"
        params = (task_name, text, type_task, date)

        final_query = query % params
        self.debug.send(f'{Fore.MAGENTA}[SQL] {final_query}')
        self.cur.execute(query, params)
        self.conn.commit()


    def update_data_task(self,task_id:int,name='',text='',date='2000-01-19',type_task='home'):
        query = "UPDATE task_list SET name = %s, text = %s, type = %s, date = %s WHERE id = %s"
        params = (name, text, type_task, date, task_id)
        self.cur.execute(query,params)
        self.conn.commit()

        final_query = query % params
        self.debug.send(f'{Fore.MAGENTA}[SQL] {final_query}')

    def delete_task_in_sql_data_base(self,task_id:int):

        query = f"SELECT name FROM task_list WHERE id='{task_id}'"
        self.cur.execute(query)
        old_task = self.cur.fetchall()[0][0]

        self.debug.send(f'{Fore.MAGENTA}[SQL] {query}')

        query = f"DELETE FROM task_list WHERE id={task_id}"
        self.cur.execute(query)
        self.conn.commit()

        self.debug.send(f'{Fore.MAGENTA}[SQL] {query}')

        return old_task

    def get_id_from_sql_table(self,task_id:int): # Метод для получения настоящего ID из sql таблицы
        task_list = self.get_task_data()
        for idd, item in enumerate(task_list['TaskList']):
            if idd+1 == task_id:
                return item['id']

    def get_number_of_tasks(self):
        task_list = self.get_task_data()
        return len(task_list['TaskList'])