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

    age_gender_data = []

    age_group_elements = soup.find_all('div', class_='row table-line-type')
    for age_group_element in age_group_elements:
        age_group_name_element = age_group_element.find('div', class_='col-xl-3 table-text col-3')
        if age_group_name_element:
            age_group_name = age_group_name_element.text.strip()
        else:
            age_group_name = "N/A"

        male_count_element = age_group_element.find('div', class_='col-xl-3 table-text col-4 text-right')
        if male_count_element:
            male_count_text = male_count_element.text.strip()
            male_count = male_count_text.split('/')[0].strip()
        else:
            male_count = "N/A"

        female_count_element = age_group_element.find_all('div', class_='col-xl-3 table-text col-4 text-right')
        if len(female_count_element) > 1:
            female_count_text = female_count_element[1].text.strip()
            female_count = female_count_text.split('/')[0].strip()
        else:
            female_count = "N/A"

        female_percentage_element = age_group_element.find('div', class_='col-xl-3 table-text ip_hide text-right')
        if female_percentage_element:
            female_percentage_text = female_percentage_element.text.strip()
            female_percentage = female_percentage_text[:-1]
        else:
            female_percentage = "N/A"

        age_gender_data.append({
            'Возраст': age_group_name,
            'Мужчины': male_count,
            'Женщины': female_count,
            'Процент женщин': female_percentage
        })

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
        'Численность населения по возрастным группам': age_gender_data,
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
