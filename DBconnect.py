import sqlite3

'''Контекстный менеджер подключения к базе данных'''

class UseDatabase:
    try:
        def __init__(self, config) -> None:
            self.configuration = config
        

        def __enter__(self):
            self.conn = sqlite3.connect(self.configuration)
            self.cursor = self.conn.cursor()
            return self.cursor


        def __exit__(self, exec_type, exc_value, exc_trace):
            self.conn.commit()
            self.cursor.close()
            self.conn.close()

    except sqlite3.Error as err:
        print(err)