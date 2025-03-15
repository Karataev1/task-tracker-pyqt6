from user_interface import Ui_AddTask
from user_interface import Ui
from colorama import init, Fore, Back, Style

from PySide6.QtCore import QDate


class AddTaskUI:
    def __init__(self,ui:Ui,sql_conn,debug,parent_form):
        self.super_ui = ui
        self.sql_data_base = sql_conn
        self.debug = debug
        self.parent_form = parent_form

        self.ui_form = Ui_AddTask(self.parent_form.ui_form)
        self.ui_form.ui.setModal(True)
        self.button_binding()
        self.install_placeholder()

        today = QDate.currentDate()
        self.ui_form.ui.input_date_task_box.setDate(today)

    def button_binding(self):
        self.ui_form.ui.button_add_task.clicked.connect(self.add_task_button)

    def install_placeholder(self):  # установка подсказок для lineEdit и прочее
        self.ui_form.ui.input_taskname_line.setPlaceholderText('enter a new task')
        self.ui_form.ui.input_addinfo_textline.setPlaceholderText('enter additional information')
        self.ui_form.ui.input_date_task_box.setCalendarPopup(True)

    def add_task_button(self):

        input_name_task, input_text, type_task, date = self.get_data_from_form()
        if input_name_task:

            type_task = self.super_ui.ui_type_task_names[type_task]
            self.sql_data_base.add_task_in_sql_data_base(
                task_name=input_name_task,
                text=input_text,
                type_task=type_task,
                date=date
            )
            self.clear_input_forms()
            self.parent_form.update_list()
            self.ui_form.hide()

        self.debug.send(f'{Fore.CYAN}[UI] Clicked: ui_add_task_button')

    def get_data_from_form(self):
        input_name_task = self.ui_form.ui.input_taskname_line.text()
        input_text = self.ui_form.ui.input_addinfo_textline.toPlainText()
        type_task = self.ui_form.ui.input_type_task_box.currentIndex()
        date = self.ui_form.ui.input_date_task_box.date()
        date = date.toString("yyyy-MM-dd")

        return input_name_task, input_text, type_task, date

    def clear_input_forms(self):
        self.ui_form.ui.input_taskname_line.clear()
        self.ui_form.ui.input_addinfo_textline.clear()