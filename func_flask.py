"""
Назначение системы

Система будет находить на сайте https://api.hh.ru/ наиболее актуальные навыки для вакансий
 со следующими параметрами: специалист - "Python developer", регион - Москва

Принцип работы системы

Система будет получать данные по вакансиям используя заданные параметры.
После того как получены описания всех вакансий по заданным параметрам,
система будет проводит следующий анализ:

1. Сколько всего вакансий
2. Средняя заработная плата
3. Все требования к данному типу вакансий
4. В скольких вакансиях указано данное требование (сортируем по убыванию)

"""

import requests
import pprint
import json
from pycbrf import ExchangeRates
from collections import Counter


def new_parser(vacancy, city='Москва'):
    count_vacs = 0
    salar = {'from': [], 'to': []}
    skill = []
    results = {'a_workpost': vacancy, 'count': count_vacs}

    url = 'https://api.hh.ru/vacancies'
    rate = ExchangeRates()
    params = {'text': vacancy}
    dict_res = requests.get(url, params=params).json()
    num_of_pages = dict_res['pages']

    print('Контролируем ход обработки загружаемых страниц:')
    for page in range(num_of_pages):
        if page > 10:
            break
        else:
            print(f"Обрабатывается страница {page}")
        par = {'text': vacancy, 'page': page}
        result = requests.get(url, params=par).json()
        for res in result['items']:
            city_vac = res['area']['name']
            if city_vac == city:
                results['count'] += 1
                url_vac = res['url']
                res_vac = requests.get(url_vac).json()

                for skl in res_vac['key_skills']:
                    skill.append(skl['name'].lower())

                if res_vac['salary']:
                    code = res_vac['salary']['currency']
                    if rate[code] is None:
                        code = 'RUR'
                    if code == 'RUR':
                        k = 1
                    else:
                        k = float(rate[code].value)
                    if res['salary']['from']:
                        if (k * res_vac['salary']['from']) < 1000000:
                            salar['from'].append(k * res_vac['salary']['from'])
                    else:
                        if (k * res_vac['salary']['to']) < 1000000:
                            salar['from'].append(k * res_vac['salary']['to'])
                    if res['salary']['to']:
                        if (k * res_vac['salary']['to']) < 1000000:
                            salar['to'].append(k * res_vac['salary']['to'])
                    else:
                        if (k * res_vac['salary']['from']) < 1000000:
                            salar['to'].append(k * res_vac['salary']['from'])

    if results['count'] != 0:
        skll = Counter(skill)
        salar_down = round(sum(salar['from']) / len(salar['from']), 2)
        salar_up = round(sum(salar['to']) / len(salar['to']), 2)
        results.update({'salary_down': round(salar_down, 2),
                        'salary_up': round(salar_up, 2)})
        navyki = []
        for name, count in skll.most_common(10):
            navyki.append({'a_navyk': name,
                           'count': count,
                           'percent': round((count / results['count']) * 100, 1)})
        results['navyki'] = navyki
        with open('results.json', mode='w') as f:
            json.dump([results], f)
    else:
        results = 'Данных нет'

    pprint.pprint(results)
    return results


if __name__ == '__main__':
    vac = 'стоматолог'
    new_parser(vac)
