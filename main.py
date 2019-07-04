import requests
import logging

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] - %(message)s')


def get_area_id(city):
    url = 'https://api.hh.ru/suggests/areas'
    params = {'text': city}
    response = requests.get(url, params=params)
    items = response.json()['items']
    return int(items[0]['id'])


def predict_rub_salary(salary_dict):
    salary_from = salary_dict.get('from')
    salary_to = salary_dict.get('to')
    if all((salary_from, salary_to)):
        return int((salary_from + salary_to)/2)
    elif salary_from and (not salary_to):
        return int(salary_from*1.2)
    else:
        return int(salary_to*0.8)


def get_hh_vacancies(language, area_id):   
    logging.info(f'HeadHunter search <{language}> starts...')
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

        logging.info(f'Page: {page}, total: {response["pages"]}')

        found = response['found']
        items = response.get('items')
        page += 1
        salary += int(sum(predict_rub_salary(item["salary"]) for item in items))

        if page == response['pages']:
            break

    return {'vacancies_found': found,
            'average_salary': int(salary/found)
            }


if __name__ == '__main__':
    languages = ('Python', 'Java', 'C++')
    area = get_area_id('Москва')

    hh = {}
    for language in languages:
        hh[language] = get_hh_vacancies(language, area)
    
    for language, info in hh.items():
        print(f'{language:8s} {info["average_salary"]}')