import requests
import execjs
import re
import json
url = 'https://r3kapig.com/assets/js/tree.js'
response = requests.get(url)
response.encoding = response.apparent_encoding
value = re.findall(r'''var a=e.*?;''', response.text)[0]
value = value.replace('a=e(l),', '')
a = execjs.compile(value)
b = a.eval('b')
t = a.eval('t')
i = a.eval('i')
r = a.eval('r')
n = a.eval('n')
values = {'label': '技能树', 'children': [b, t, i, r, n]}
values = json.dumps(values,ensure_ascii=False)
file = open('res.json', 'w', encoding='utf-8')
file.write(values)
file.close()
