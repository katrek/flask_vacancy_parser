import requests
from bs4 import BeautifulSoup as bs
import time

headers_work = {
    'accept' : '*/*',
    'user-agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
}

base_url_work = 'https://www.work.ua/jobs-kyiv-front/?page=1'
def Parser_work_ua(base_url_work, headers_work):
    parse_time_start = time.time()
    jobs = []
    urls = []
    urls.append(base_url_work)
    session = requests.Session()
    request = session.get(base_url_work, headers=headers_work)
    if request.status_code == 200:
        soup = bs(request.content, 'html.parser')
        try:
            pagination = soup.find('span', attrs={'class' : 'text-default'}).text
            pagination_id = list(pagination)
            count = int(pagination_id[-1]) + 1
            for i in range(1, count):
                url = f'https://www.work.ua/jobs-kyiv-front/?page={i}'
                if url not in urls:
                    urls.append(url)
        except:
            pass
    for url in urls:
        request = session.get(url, headers=headers_work)
        soup = bs(request.content, 'html.parser')
        divs = soup.find_all('div', attrs={'class' : 'card card-hover card-visited wordwrap job-link'})
        for div in divs:
            title = div.find('a').text
            href = 'http://work.ua' + div.find('a')['href']
            info = div.find('p', attrs={'class' : 'overflow'}).text
            date = div.find('span', attrs={'class' : 'text-muted'}).text
            jobs.append({
                'title' : title,
                'href' : href,
                'info' : info,
                'date' : date,
            })
        print(len(jobs))
        print(jobs)
    else:
        if request.status_code is not 200:
            print('ERROR!!!', request.status_code)
        else:
            parse_time_finish = time.time()
            parse_time_result = parse_time_finish - parse_time_start
            print('Parsing done.')
            print('Parsed in ', str(parse_time_result), 'seconds')
    return jobs


