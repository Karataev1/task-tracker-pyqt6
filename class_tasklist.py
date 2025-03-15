from user_interface import Ui_TaskList
from user_interface import Ui
from datetime import datetime

from PySide6.QtCore import (QCoreApplication, Qt)
from PySide6.QtWidgets import QListWidgetItem
from colorama import init, Fore, Back, Style

class TaskListUI:
    def __init__(self,ui:Ui,sql_conn,debug):
        self.super_ui = ui
        self.sql_data_base = sql_conn
        self.debug = debug

        self.ui_form = Ui_TaskList()

        self.button_binding()
        self.install_placeholder()

    def button_binding(self):
        self.ui_form.ui.button_add_new_task.clicked.connect(lambda: self.super_ui.show_form(form='add_task'))
        self.ui_form.ui.del_button.clicked.connect(self.del_task_button)
        self.ui_form.ui.comboBox.currentIndexChanged.connect(lambda: self.update_list())
        self.ui_form.ui.comboBox_2.currentIndexChanged.connect(lambda: self.update_list())

    def install_placeholder(self):
        self.ui_form.ui.comboBox.setCurrentText('Все')
        self.ui_form.ui.comboBox_2.setCurrentText('Все')


    def del_task_button(self):

        select_item = self.get_data_from_form()

        if select_item is not None:

            task_id = self.super_ui.task_ids_from_the_database['ItemTaskId'][select_item]['id']
            self.sql_data_base.delete_task_in_sql_data_base(task_id)
            self.update_list()

        self.debug.send(f'{Fore.CYAN}[UI] Clicked: ui_del_task_button')

    def get_data_from_form(self):
        current_item = self.ui_form.ui.listWidget.currentItem()
        if current_item is not None:
            return self.ui_form.ui.listWidget.row(current_item)
        return None

    def update_list(self):

        get_type_select, get_timeframe_select = self.get_data_from_comboBox()
        type_select = self.super_ui.ui_type_task_names[get_type_select]
        timeframe = self.super_ui.ui_filter_timeframe[get_timeframe_select]
        end_date = self.super_ui.filter_timeframe(timeframe)
        today_start, today_end, now = self.super_ui.set_start_and_end_today()

        task_list = self.sql_data_base.get_task_data()

        self.ui_form.ui.listWidget.clear()
        self.super_ui.task_ids_from_the_database['ItemTaskId'] = list('')


        for idd, item in enumerate(task_list['TaskList']):
            is_task_type_valid = (type_select == 'all' or item['type'] == type_select)
            is_due_date_valid = (end_date is None or
                                 datetime.combine(item['date'], datetime.min.time()) <= end_date)
            is_timeframe_valid = (timeframe != 'today' or
                                  (today_start.date() <= item['date'] <= today_end.date()))

            if is_task_type_valid and is_due_date_valid and is_timeframe_valid:
                task_id = dict()
                task_id['id'] = item['id']
                self.super_ui.task_ids_from_the_database['ItemTaskId'].append(task_id)
                newtask_item = QListWidgetItem(self.ui_form.ui.listWidget)
                newtask_item.setCheckState(Qt.Unchecked)

                newtask_item.setText(QCoreApplication.translate("MainWindow", f"{item['name']}", None))

        self.debug.send(f'{Fore.CYAN}[UI] call: update_list()')

    def get_data_from_comboBox(self):
        selected = self.ui_form.ui.comboBox.currentIndex()
        selected_2 = self.ui_form.ui.comboBox_2.currentIndex()

        return selected, selected_2
