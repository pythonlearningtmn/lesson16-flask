from sqlite3 import connect
# Создание баз данных в файле
crsr = connect('hh_parser.db').cursor()

crsr.executescript('''
    create table vacancy (
    id integer primary key,
    name_vac varchar(50) not null,
    count_vac real,
    salary_down real,
    salary_up real
    );

    create table skill (
    id integer primary key,
    name_skill varchar(255)
    );

    create table vacancyskill (
    id integer primary key,
    id_vacancy integer,
    id_skill integer,
    count real,
    percent real,
    foreign key (id_vacancy) references vacancy (id)
    foreign key (id_skill) references skill (id)
    );
''')

crsr.close()
