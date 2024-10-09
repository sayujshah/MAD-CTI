from requests_tor import RequestsTor
from bs4 import BeautifulSoup

urls = [
    'http://ransomwr3tsydeii4q43vazm7wofla5ujdajquitomtd47cxjtfgwyyd.onion',
    'http://xssforumv3isucukbxhdhwz67hoa5e2voakcfkuieq4ch257vsburuid.onion/'
        ]
request = RequestsTor(tor_ports=(9050,), tor_cport=9051, password='16:12024A6F8EFF852F6078995623DF4921E40F1972E1EA6135D87F52C0D6')

for url in urls:
    response = request.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        '''
        links = soup.find_all('a')
        for link in links:
            print(link.get('href'))
        '''
        print(soup.get_text())
    else:
        print(f'Failed to retrieve {url}')