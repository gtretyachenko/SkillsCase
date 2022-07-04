import requests
from bs4 import BeautifulSoup

url = 'https://www.mobile.de/ru/'
params = {'page': 1}
# задаем число больше номера первой страницы, для старта цикла
pages = 2
n = 1
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}
while params['page'] <= pages:
    response = requests.get(url, params=params, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    print(soup)
    items = soup.find_all('div', class_='col-lg-4 col-md-6 mb-4')

    for n, i in enumerate(items, start=n):
        itemName = i.find('h4', class_='card-title').text.strip()
        itemPrice = i.find('h5').text
        print(f'{n}:  {itemPrice} за {itemName}')

    # [-2] предпоследнее значение, потому что последнее "Next"
    last_page_num = int(soup.find_all('a', class_='page-link')[-2].text)
    pages = last_page_num if pages < last_page_num else pages
    params['page'] += 1