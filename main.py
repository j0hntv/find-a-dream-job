import requests

def get_area_id(city):
    url = 'https://api.hh.ru/suggests/areas'
    params = {'text': city}
    response = requests.get(url, params=params)
    items = response.json()['items']
    return int(items[0]['id'])


if __name__ == '__main__':
    area = get_area_id('Москва')
    print(area)