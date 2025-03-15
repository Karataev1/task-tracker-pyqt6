from form_tasklist import Ui_MainWindow
from form_addtask import Ui_AddTaskForm
from form_edittask import Ui_EditTaskForm
from datetime import datetime, timedelta
from PySide6.QtWidgets import QMainWindow
from colorama import init, Fore, Back, Style

class Ui:
    def __init__(self,sql_conn,debug):

        self.sql_data_base = sql_conn
        self.debug = debug

        self.ui_selected_task_index = None # Держит в себе ID выбранного элемента для изменения задачи
        self.task_ids_from_the_database : dict[str, list] = {"ItemTaskId": []} # Хранит ID задач из базы данных
        self.ui_type_task_names = {0:'everyday',
                                   1:'home',
                                   2:'job',
                                   3:'all'}
        self.ui_type_task_names_reverse = {v: k for k, v in self.ui_type_task_names.items()}

        self.ui_filter_timeframe = {0:'today',
                                    1:'week',
                                    2:'month',
                                    3:'all'}

        from class_tasklist import TaskListUI
        self.task_list = TaskListUI(self, sql_conn, debug)

        from class_addtask import AddTaskUI
        self.add_task = AddTaskUI(self, sql_conn, debug, self.task_list)

        from class_edittask import EditTaskUI
        self.edit_task = EditTaskUI(self, sql_conn, debug, self.task_list)


    def show_form(self,form='task_list'):

        form_name = {
            'task_list': lambda: self.task_list.ui_form.show(),
            'add_task': lambda: self.add_task.ui_form.show(),
            'edit_task': lambda: self.edit_task.ui_form.show()

        }
        show_form = form_name.get(form)
        show_form()

        self.debug.send(f'{Fore.CYAN}[UI] Show form: `{form}`')


    def filter_timeframe(self,timeframe:str):

        n, today_end, now = self.set_start_and_end_today()
        if timeframe == 'week':
            end_date = now + timedelta(weeks=1)
        elif timeframe == 'month':
            end_date = now + timedelta(weeks=4)
        elif timeframe == 'today':
            end_date = today_end
        elif timeframe == 'all':
            end_date = None

        return end_date

    def set_start_and_end_today(self):
        now = datetime.now()
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = now.replace(hour=23, minute=59, second=59, microsecond=999999)

        return today_start, today_end, now



class Ui_TaskList(QMainWindow):
    def __init__(self):
        super(Ui_TaskList, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)


class Ui_AddTask(QMainWindow):
    def __init__(self,parent=None):
        super(Ui_AddTask, self).__init__(parent)
        self.ui = Ui_AddTaskForm()
        self.ui.setupUi(self)


class Ui_EditTask(QMainWindow):
    def __init__(self,parent=None):
        super(Ui_EditTask, self).__init__(parent)
        self.ui = Ui_EditTaskForm()
        self.ui.setupUi(self)



