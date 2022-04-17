import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import sys


def bing_search(site, pages):
    Subdomain = []
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/75.0.3770.100 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,'
                  'application/signed-exchange;v=b3',
        'Referer': 'https:www.baidu.com',
        'Cookie': 'JSESSIONID=5D18610FD1F6A76EE1D8B6704A0687B6'
    }
    for i in range(1, int(pages) + 1):
        url = "https://cn.bing.com/search?q=site%3a" + site + "&go=Search&qs=ds&first=" + str(
            (int(i) - 1) * 10) + "&FROM=PERE"
        html = requests.get(url, headers=headers)
        soup = BeautifulSoup(html.content, 'lxml')
        jpb_bt = soup.findAll('h2')
        for i in jpb_bt:
            link = i.a.get('href')
            domain = str(urlparse(link).scheme + "://" + urlparse(link).netloc)
            if domain in Subdomain:
                pass
            else:
                Subdomain.append(domain)
                print(domain)


if __name__ == '__main__':
    if len(sys.argv) == 3:
        site = sys.argv[1]
        page = sys.argv[2]
    else:
        print("usage: %s baidu.com 10" % sys.argv[0])
        sys.exit(-1)
    bing_search(site, page)

