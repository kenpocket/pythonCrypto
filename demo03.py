import requests, re

URL = "https://www.southcn.com/"
response = requests.get(URL)
response.encoding = response.apparent_encoding
a = re.findall(r'''<a href="(.*?)" data-pubtime='(.*?)' data-cat=''\n.*?target="_blank" title="(.*?)">(.*?)</a>''',
               response.text)
for i in a:
    print(i)