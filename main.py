"""
<main class="vacancy-serp-content">
<div class="serp-item" data-qa="vacancy-serp__vacancy vacancy-serp__vacancy_standard_plus">
<h3 data-qa="bloko-header-3" class="bloko-header-section-3">
<span data-page-analytics-event="vacancy_search_suitable_item">
<a class="serp-item__title" data-qa="serp-item__title" target="_blank" href="https://spb.hh.ru/vacancy/87592497?from=vacancy_search_list&amp;hhtmFrom=vacancy_search_list&amp;query=python+flask+django">Middle backend Python</a>

<div class="vacancy-serp-item__info">
<a data-qa="vacancy-serp__vacancy-employer" class="bloko-link bloko-link_kind-tertiary" href="/employer/4747821?hhtmFrom=vacancy_search_list">ООО&nbsp;РА Дельта</a>
<div data-qa="vacancy-serp__vacancy-address" class="bloko-text">Москва</div>

"""


import json
from unicodedata import normalize
import requests
import bs4
import fake_headers
import time
from pprint import pprint

keywords = ['Django', 'Flask']

headers_gen = fake_headers.Headers(browser='chrome', os='win')
response = requests.get('https://spb.hh.ru/search/vacancy?ored_clusters=true&hhtmFrom=vacancy_search_list&search_field=name&search_field=company_name&search_field=description&enable_snippets=false&L_save_area=true&area=1&area=2&text=python+flask+django',
                        headers=headers_gen.generate())
main_html = response.text
main_soup = bs4.BeautifulSoup(main_html, features='lxml')

aplication_list_tag = main_soup.find('main', class_ = 'vacancy-serp-content')
aplication_tags = aplication_list_tag.find_all('div', class_ = 'serp-item')


parsed_data = []

for aplication_tag in aplication_tags:
    h3_tag = aplication_tag.find('h3')
    span_tag = h3_tag.find('span')
    a_tag = span_tag.find('a', class_ = 'serp-item__title')

    company_block_info_tag = aplication_tag.find('div', class_ = 'vacancy-serp-item__info')
    company_name_tag = company_block_info_tag.find('a', class_ = 'bloko-link bloko-link_kind-tertiary')

    city_name_tag = company_block_info_tag.find('div', {'data-qa': 'vacancy-serp__vacancy-address'})

    salary_tag = aplication_tag.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})


    headers = h3_tag.text
    link = a_tag['href']
    company_name = normalize('NFKD', company_name_tag.text)
    city_name = city_name_tag.text
    
    if salary_tag:
        salary = normalize('NFKD', salary_tag.text)
    else:
        salary = 'Не указана'
    time.sleep(0.1)
    parsed_data.append({
        'link': link,
        'header': headers,
        'company-name': company_name,
        'city': city_name,
        'salary': salary
        })

if __name__ == '__main__':
    with open ('parsed-data.json', 'w', encoding='utf-8') as file:
        json.dump(parsed_data, file, ensure_ascii=False)
