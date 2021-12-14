import sqlite3

try:
    sqlite_connection = sqlite3.connect('dbase.db')
    cursor = sqlite_connection.cursor()
    print('База данных создана и успешно подключена к SQLite')

    sqlite_select_query = 'select sqlite_version();'
    cursor.execute(sqlite_select_query)
    record = cursor.fetchall()
    print('Версия базы данных SQLite: ', record)

    cursor.execute('''PRAGMA foreign_keys=on''')
    
    cursor.execute('''CREATE TABLE TypeEquipment(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name_type varchar(32) not null,
        maskSN varchar(10) not null)''')
    
    cursor.execute('''CREATE TABLE Equipment(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type_code INTEGER not null,
        sn varchar(10) not null,
        FOREIGN KEY (type_code) REFERENCES TypeEquipment(id),
        UNIQUE (sn))''')
    
    _SQL = '''insert into TypeEquipment
            (name_type, maskSN)
            values
            (?, ?)'''
    
    cursor.execute(_SQL, ('TP-Link TL-WR74', 'XXAAAAAXAA',))
    cursor.execute(_SQL, ('D-Link DIR-300', 'NXXAAXZXaa',))
    cursor.execute(_SQL, ('D-Link DIR-300 S', 'NXXAAXZXXX',))
    
    sqlite_connection.commit()
    
    cursor.close()
    
except sqlite3.Error as error:
    print('Ошибка при подключении к sqlite', error)
finally:
    if (sqlite_connection):
        sqlite_connection.close()
        print('Соединение с SQLite закрыто, таблицы созданы и наполнены.')