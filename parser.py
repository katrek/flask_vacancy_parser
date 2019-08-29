import requests
from bs4 import BeautifulSoup as bs
import time

headers = {
    'accept' : '*/*',
    'user-agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
}

base_url = 'https://kiev.hh.ua/search/vacancy?L_is_autosearch=false&area=115&clusters=true&currency_code=UAH&enable_snippets=true&text=python&page=0'

def Parser(base_url, headers):
    parse_time_start = time.time()
    jobs = []
    urls = []
    urls.append(base_url)
    session = requests.Session()
    request = session.get(base_url, headers=headers)
    if request.status_code == 200:
        soup = bs(request.content, 'html.parser')
        try:
            pagination = soup.find_all('a', attrs={'data-qa' : 'pager-page'})
            count = int(pagination[-1].text)
            for i in range(count):
                url = f'https://kiev.hh.ua/search/vacancy?L_is_autosearch=false&area=115&clusters=true&currency_code=UAH&enable_snippets=true&text=python&page={i}'
                if url not in urls:
                    urls.append(url)
        except:
            pass
    for url in urls:
        request = session.get(url, headers=headers)
        soup = bs(request.content, 'html.parser')
        divs = soup.find_all('div', attrs={'data-qa' : 'vacancy-serp__vacancy'})
        for div in divs:
            title = div.find('a', attrs={'data-qa' : 'vacancy-serp__vacancy-title'}).text
            href = div.find('a', attrs={'data-qa' : 'vacancy-serp__vacancy-title'})['href']
            company = div.find('a', attrs={'data-qa' : 'vacancy-serp__vacancy-employer'}).text
            text1 = div.find('div', attrs={'data-qa' : 'vacancy-serp__vacancy_snippet_responsibility'}).text
            text2 = div.find('div', attrs={'data-qa' : 'vacancy-serp__vacancy_snippet_requirement'}).text
            content = text1 + ' ' + text2
            jobs.append({
                'title' : title,
                'href' : href,
                'company' : company,
                'content' : content,
            })
            vacancies_found = len(jobs)
            print('Vacancies scanned: ', vacancies_found)
    else:
        if request.status_code is not 200:
            print('ERROR!!!', request.status_code)
        else:
            parse_time_finish = time.time()
            parse_time_result = parse_time_finish - parse_time_start
            print('Parsing done.')
            print('Parsed in ', str(parse_time_result), 'seconds')
    return jobs

