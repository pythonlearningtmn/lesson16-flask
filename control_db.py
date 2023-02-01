from sqlite3 import connect


def add_vacancy(cur, new):
    """
    Добавление или редактирование записи в таблице со специализациями
    :param cur: передача курсора доступа к базе данных
    :param new: словарь с данными по результатам поиска вакансий
    :return: курсор доступа к базе данных
    """
    cur.execute('select * from vacancy where vacancy.name_vac = ?', (new['a_workpost'],))
    res = cur.fetchone()
    print(res)
    if res:
        if res[2] < new['count']:
            # обновление записи таблицы
            cur.execute('update vacancy set count_vac = ?, salary_down = ?, salary_up = ? where vacancy.id = ?',
                        (new['count'], new['salary_down'], new['salary_up'], res[0]))
            print('Таблица специализаций - запись обновлена')
        else:
            print('Таблица специализаций без редактирования')
    else:
        # добавление записи в таблице
        cur.execute('insert into vacancy values (null, ?, ?, ?, ?)',
                    (new['a_workpost'], new['count'], new['salary_down'], new['salary_up']))
        print('Таблица специализаций - запись выполнена')
    return cur


def add_skill(cur, new):
    """
    Добавление записи в таблицу навыков
    :param cur: передача курсора доступа к базе данных
    :param new: словарь с данными по результатам поиска вакансий
    :return: курсор доступа к базе данных
    """
    for item in new['navyki']:
        res = cur.execute('select * from skill where skill.name_skill = ?', (item['a_navyk'],))
        if not res.fetchone():
            print(item['a_navyk'])
            cur.execute('insert into skill values (null, ?)', (item['a_navyk'],))
    return cur


def add_vacancyskill(cur, new):
    """
    Добавление записи в сводную таблицу
    :param cur: передача курсора доступа к базе данных
    :param new: словарь с данными по результатам поиска вакансий
    :return: курсор доступа к базе данных
    """
    cur.execute('select id, count_vac from vacancy where vacancy.name_vac = ?', (new['a_workpost'],))
    vac_id, vac_count = cur.fetchone()
    for item in new['navyki']:
        cur.execute('select id from skill where skill.name_skill = ?', (item['a_navyk'],))
        skill_id = cur.fetchone()[0]
        print(vac_id, skill_id)
        cur.execute('select * from vacancyskill as vs where vs.id_vacancy = ? and vs.id_skill = ?',
                    (vac_id, skill_id))
        res = cur.fetchone()
        if not res:
            cur.execute('insert into vacancyskill values (null, ?, ?, ?, ?)',
                        (vac_id, skill_id, item['count'], item['percent']))
            print('Сводная таблица - запись выполнена')
        elif vac_count < new['count']:
            cur.execute('update vacancyskill as vs set count = ?, percent = ? where vs.id_vacancy = ? '
                        'and vs.id_skill = ?', (item['count'], item['percent'], vac_id, skill_id))
            print('Сводная таблица обновлена')
        else:
            print('Сводная таблица без редактирования')
    return cur


def add_record(res):
    """
    Добавление новых записей в таблицы.
    :param res: словарь с данными по результатам поиска вакансий
    """
    cnct = connect('hh_parser.db')
    crsr = cnct.cursor()
    crsr = add_vacancy(crsr, res)
    crsr = add_skill(crsr, res)
    crsr = add_vacancyskill(crsr, res)
    cnct.commit()
    cnct.close()
