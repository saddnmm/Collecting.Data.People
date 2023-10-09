import requests
from bs4 import BeautifulSoup
import json  
import datetime
import os
from config import KZN_URL

url = KZN_URL
response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    city_name = soup.find('h1').text.strip()

    population = soup.find('span', class_='people-big-1').text.strip()

    rating_place = soup.find('p', class_='check_rating').text.strip()

    age_groups = []
    age_group_elements = soup.find_all('div', class_='table-line-type')
    for age_group_element in age_group_elements:
        age_group_name = age_group_element.find('div', class_='table-text').text.strip()
        try:
            age_group_count = age_group_element.find('div', class_='table-text2').find('span').text.strip()
        except AttributeError:
            age_group_count = "N/A" 

        age_groups.append((age_group_name, age_group_count))

    gender_info = {}
    gender_elements = soup.find_all('div', class_='row table-line-type')
    for gender_element in gender_elements:
        age_group_name = gender_element.find('div', class_='table-text').text.strip()
        try:
            male_count = gender_element.find_all('div', class_='table-text col-4 text-right')[0].text.strip()
        except Exception:
            male_count = "N/A"
        try:
            female_count = gender_element.find_all('div', class_='table-text col-4 text-right')[1].text.strip()
        except Exception:
            female_count = "N/A" 
        gender_info[age_group_name] = {'male': male_count, 'female': female_count}

    employment_info = {}
    employment_elements = soup.find_all('div', class_='row table-line-type')
    for employment_element in employment_elements:
        employment_group_name = employment_element.find('div', class_='table-text').text.strip()
        try:
            employment_count = employment_element.find('div', class_='table-text2').find('span').text.strip()
        except Exception:
            employment_count = "N/A"
        employment_info[employment_group_name] = employment_count

    disability_info = {}
    disability_elements = soup.find_all('div', class_='row table-line-type')
    for disability_element in disability_elements:
        disability_group_name = disability_element.find('div', class_='table-text').text.strip()
        try:
            disability_count = disability_element.find('div', class_='table-text2').find('span').text.strip()
        except Exception:
            disability_count = "N/A"
        disability_info[disability_group_name] = disability_count

    # Создаем словарь для сохранения всех данных
    data = {
        'Город': city_name,
        'Количество людей': population,
        'Место в рейтинге': rating_place,
        'Численность населения по возрастным группам': dict(age_groups),
        'Гендерный состав населения': gender_info,
        'Занятость населения, безработица и пенсионеры': employment_info,
        'Инвалидность': disability_info
    }

    # Сериализуем данные в JSON и сохраняем в файл
    with open(os.path.join(os.path.dirname(__file__), 'static', f'{city_name}.data.json'), 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

    print(f'Данные успешно сохранены в файл "data.json".')
else:
    print('Не удалось получить доступ к странице.')
