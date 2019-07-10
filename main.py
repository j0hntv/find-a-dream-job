import requests
import logging
import os
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] - %(message)s')

def get_area_id(city):
    url = 'https://api.hh.ru/suggests/areas'
    params = {'text': city}
    response = requests.get(url, params=params)
    items = response.json()['items']
    return int(items[0]['id'])


def predict_rub_salary(salary_from, salary_to):
    if all((salary_from, salary_to)):
        return int((salary_from + salary_to)/2)
    elif salary_from and (not salary_to):
        return int(salary_from*1.2)
    else:
        return int(salary_to*0.8)


def get_hh_vacancies(language, area_id):   
    logging.info(f'HeadHunter: search <{language}> vacancies...')
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
        response = response.json()

        logging.info(f'Page: {page+1}/{response["pages"]}')

        found = response['found']
        items = response.get('items')
        page += 1
        salary += int(sum(predict_rub_salary(item['salary']['from'], item['salary']['to']) for item in items))

        if page == response['pages']:
            break

    return {'vacancies_found': found,
            'average_salary': int(salary/found) if found else 'Нет вакансий'
            }


def get_superjob_vacancies(api_key, language, city):
    logging.info(f'SuperJob: search <{language}> vacancies...')
    url = 'https://api.superjob.ru/2.0/vacancies'
    page = 0
    salary = 0

    count = 100

    while True:
        params = {'town': city,
                    'no_agreement': 1,
                    'catalogues': 48,
                    'page': page,
                    'count': count,
                    'keyword': language}
        headers = {'X-Api-App-Id': SUPERJOB_KEY}
        response = requests.get(url, headers=headers, params=params)
        response = response.json()
        found = response['total']

        pages = found//count + 1
        logging.info(f'Page: {page+1}/{pages}')

        vacancies = response['objects']
        for vacancy in vacancies:
            payment_from = vacancy['payment_from']
            payment_to = vacancy['payment_to']
            salary += int(predict_rub_salary(payment_from, payment_to))
        
        page += 1
        
        if not response['more']:
            break
    
    return {'vacancies_found': found,
            'average_salary': int(salary/found) if found else 'Нет вакансий'
            }
    

if __name__ == '__main__':
    load_dotenv()
    SUPERJOB_KEY = os.getenv('SUPERJOB_KEY')
    languages = ('Python', 'Java', 'Kotlin', 'C', 'C++', 'C#', 'Ruby', 'Go', '1С', 'JS', 'R', 'Swift', 'Scala', 'SQL')

    city = 'Москва'
    area_id = get_area_id(city)

    #=====HeadHunter======

    hh = {}
    for language in languages:
        hh[language] = get_hh_vacancies(language, area_id)
    
    for language, info in hh.items():
        print(f'{language:8s} {info["average_salary"]}')

    #=====SuperJob======
    
    
    sj = {}
    for language in languages:
        sj[language] = get_superjob_vacancies(SUPERJOB_KEY, language, city)

    for language, info in sj.items():
        print(f'{language:8s} {info["average_salary"]}')
