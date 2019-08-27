import requests
from bs4 import BeautifulSoup as bs
import time

headers_rabota = {
    'accept' : '*/*',
    'user-agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
}

base_url_rabota = 'https://rabota.ua/zapros/python/%d0%ba%d0%b8%d0%b5%d0%b2/pg1'

def Parser_rabota(base_url_rabota, headers_rabota):
    parse_time_start = time.time()
    jobs = []
    urls = []
    session = requests.Session()
    request = session.get(base_url_rabota, headers=headers_rabota)
    if request.status_code == 200:
        soup = bs(request.content, 'html.parser')
        try:
            pagination = soup.find('dl', attrs={'id': 'ctl00_content_vacancyList_gridList_ctl23_pagerInnerTable'}).text
            pagination_id = list(pagination)
            count = int(pagination_id[-10])
            for i in range(count):
                url = f'https://rabota.ua/zapros/python/%d0%ba%d0%b8%d0%b5%d0%b2/pg{i}'
                if url not in urls:
                    urls.append(url)
        except:
            pass
    for url in urls:
        request = session.get(url, headers=headers_rabota)
        soup = bs(request.content, 'html.parser')
        divs = soup.find_all('article', attrs={'class' : 'f-vacancylist-vacancyblock'})
        for div in divs:
            title = div.find('a')['title']
            href = 'https://rabota.ua' + div.find('a')['href']
            company = div.find('a', attrs={'class' : 'f-text-dark-bluegray f-visited-enable'}).text
            info = div.find('p', attrs={'class' : 'f-vacancylist-shortdescr f-text-gray fd-craftsmen'}).text
            jobs.append({
                'title' : title,
                'href' : href,
                'company' : company,
                'info' : info,
            })
        print(len(jobs))
    else:
        if request.status_code is not 200:
            print('ERROR!!!', request.status_code)
        else:
            parse_time_finish = time.time()
            parse_time_result = parse_time_finish - parse_time_start
            print('Parsing done.')
            print('Parsed in ', str(parse_time_result), 'seconds')
    return jobs

