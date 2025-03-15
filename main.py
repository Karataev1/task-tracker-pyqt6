from application import Application
from sql_connect import WorkWithSqlDataBase
from debug import Debug

from PySide6.QtWidgets import QApplication
from user_interface import Ui
import sys

if __name__ == '__main__':
    appp = QApplication(sys.argv)
    debug = Debug(prog_name='TaskTracker', prog_ver='4.0',status=True)
    work_with_sql_database = WorkWithSqlDataBase(
        database='task_tracker',
        user='docker',
        password='docker',
        host='localhost',
        debug=debug
    )
    if work_with_sql_database.db_connected():

        ui = Ui(work_with_sql_database,debug)
        debug.sql_data_base = work_with_sql_database
        app = Application(
            work_with_sql_database,
            ui,
            debug
        )

        app.start()
        sys.exit(appp.exec())





