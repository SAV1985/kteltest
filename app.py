from flask import Flask, render_template, request, redirect, url_for
from DBconnect import UseDatabase
from maskchecker import mask_check
from sqlite3 import IntegrityError

app = Flask(__name__)

app.config['dbconfig'] = 'dbase.db'


'''Начальная страница со списком записанного оборудования'''
@app.route('/')
def view_the_db():
    with UseDatabase(app.config['dbconfig']) as logDB:
        _SQL = '''SELECT Equipment.id, TypeEquipment.name_type, Equipment.sn
            FROM TypeEquipment, Equipment
            WHERE TypeEquipment.id=Equipment.type_code'''
        logDB.execute(_SQL)
        contents = logDB.fetchall()
    titles = ['№', 'Тип оборудования', 'Серийный номер']
    return render_template('index.html',
                        the_title = 'View DB',
                        the_row_titles = titles,
                        the_data = contents,)
    
@app.route('/index')
def index():
    return view_the_db()

'''Вызов страницы добавления оборудования'''
@app.route('/entry')
def entry():
    with UseDatabase(app.config['dbconfig']) as logDB:
        _SQL = """select * from TypeEquipment"""
        logDB.execute(_SQL)
        contents = logDB.fetchall()
    return render_template('entry.html',
                        the_title='Запись оборудования в базу',
                        the_data=contents,)

'''Функция проверки добавляемых серийных номеров'''
@app.route("/vsearch", methods = ["POST"])
def do_search():
    errors = []                                             #Переменная для записи найденных ошибок
    sn = (request.form['sn']).split()                       #Переменная со списком введенных серийных номеров
    typesn = request.form['typeEquipment']                 #Переменная с id в базе типа оборудования
    with UseDatabase(app.config['dbconfig']) as logDB:
        _SQL = """select * from TypeEquipment where id = ?"""
        logDB.execute(_SQL, typesn)
        contents = logDB.fetchall()
        for i in sn:
            x, y = mask_check(contents[0][2], i)            #Функция проверки на соответствие шаблону
            if x != True:                                   #Проверка на полученные ошибки
                errors.append(y)
                continue
            try:
                with UseDatabase(app.config['dbconfig']) as log:
                    _SQL = """insert into Equipment
                            (type_code, sn)
                            values
                            (?, ?)"""
                    log.execute(_SQL, (contents[0][0], y))
            except IntegrityError as err:
                if str(err) == 'UNIQUE constraint failed: Equipment.sn':
                    errors.append('Серийный номер \"{}\" уже существует'.format(i))
                continue
    if errors:
        return render_template('error.html', errors = errors)
    return  redirect('/')
               
    


if __name__ == '__main__':
    app.run(debug = True)