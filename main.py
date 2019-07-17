import requests
import logging
import os
from dotenv import load_dotenv
from terminaltables import AsciiTable

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] - %(message)s')

def get_headhunter_area_id(city):
    url = 'https://api.hh.ru/suggests/areas'
    params = {'text': city}
    response = requests.get(url, params=params)
    response.raise_for_status()
    items = response.json().get('items')
    if items:
        return int(items[0]['id'])
    else:
        raise requests.exceptions.HTTPError


def predict_rub_salary(salary_from, salary_to):
    if all((salary_from, salary_to)):
        return int((salary_from + salary_to)/2)
    elif salary_from and (not salary_to):
        return int(salary_from*1.2)
    else:
        return int(salary_to*0.8)


def get_hh_vacancies(language, area_id):   
    logging.info(f'Search <{language}> vacancies...')
    url = 'https://api.hh.ru/vacancies'
    page = 0
    salary = 0

    while True:
        params = {'text': f'Программист {language}',
                'per_page': 100,
                'area': area_id,
                'only_with_salary': 'true',
                'period': 30,
                'currency': 'RUR',
                'page': page}

        response = requests.get(url, params=params)
        response.raise_for_status()

        response_json = response.json()

        pages = response_json.get('pages')
        found = response_json.get('found')
        items = response_json.get('items')

        if all((pages, found, items)):
            logging.info(f'Page: {page+1}/{pages}')
            page += 1
            salary += int(sum(predict_rub_salary(item['salary']['from'], item['salary']['to']) for item in items))
        else:
            raise requests.exceptions.HTTPError

        if page == response_json['pages']:
            break

    return {'vacancies_found': found if found else 0,
            'average_salary': int(salary/found) if found else 0}


def get_superjob_vacancies(api_key, city, language, catalogues_id):
    logging.info(f'Search <{language}> vacancies...')
    url = 'https://api.superjob.ru/2.0/vacancies'
    page = 0
    salary = 0

    count = 100

    while True:
        params = {'town': city,
                    'no_agreement': 1,
                    'catalogues': catalogues_id,
                    'page': page,
                    'count': count,
                    'keyword': language}
        headers = {'X-Api-App-Id': api_key}
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()

        response_json = response.json()
        found = response_json.get('total')
        pages = found//count + 1
        vacancies = response_json.get('objects')

        if all((found, vacancies)):
            logging.info(f'Page: {page+1}/{pages}')
            for vacancy in vacancies:
                payment_from = vacancy['payment_from']
                payment_to = vacancy['payment_to']
                salary += int(predict_rub_salary(payment_from, payment_to))
            
            page += 1
        else:
            raise requests.exceptions.HTTPError
        
        if not response_json['more']:
            break
    
    return {'vacancies_found': found if found else 0,
            'average_salary': int(salary/found) if found else 0}
    

def print_table(title, vacancies_dict, city):
    columns = ['Язык программирования', 'Найдено вакансий', 'Средняя зарплата']
    vacancies = [[language, 
                vacancies_dict[language]['vacancies_found'],
                vacancies_dict[language]['average_salary']] for language in vacancies_dict]

    vacancies = sorted(vacancies, key=lambda x: x[2], reverse=True)

    title = f'{title} {city}'

    vacancies.insert(0, columns)
    table_instance = AsciiTable(vacancies, title)
    print()
    print(table_instance.table)


def main():
    load_dotenv()
    superjob_key = os.getenv('SUPERJOB_KEY')

    languages = ('Python', 'Java', 'Kotlin',
                'C', 'C++', 'C#', 'Ruby', 'Go',
                '1С', 'JS', 'Php', 'R', 'Swift',
                'Scala', 'SQL', 'Lua', 'Haskell',
                'Bash', 'Pascal', 'Erlang')

    city = 'Москва'
    city_headhunter_id = get_headhunter_area_id(city)

    print('[*] Собираем данные с HeadHunter')
    hh = {}
    for language in languages:
        hh[language] = get_hh_vacancies(language, city_headhunter_id)
    
    print('[*] Собираем данные с SuperJob')
    sj = {}
    catalogues_id = 48
    for language in languages:
        sj[language] = get_superjob_vacancies(superjob_key, city, language, catalogues_id)
    
    print_table('HeadHunter', hh, city)
    print_table('SuperJob', sj, city)


if __name__ == '__main__':
    try:
        main()
    except (requests.exceptions.ConnectionError, requests.exceptions.HTTPError) as error:
        logging.error(error)
