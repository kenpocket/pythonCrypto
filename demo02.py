import requests
import re
url = 'http://news.sohu.com/'  # 搜狐主页
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0"
}
response = requests.get(url, headers=headers)
response.encoding = "utf-8"  # 设置编码方式
# print(response.text)
res = re.findall(r'''<a data-param=".*?" title="(.*?)" href="//(.*?)"''', response.text)  # 提取标题（title）和链接（href）
for i in res:
    title = i[0]
    src = "https://" + i[1]  # 链接补全，加上https头
    response_art = requests.get(src)
    response_art.encoding = "utf-8"
    # print(response_art.text)
    title = re.findall(r'<title>(.*?)</title>', response_art.text)[0]
    time = re.findall(r'''<meta itemprop="dateUpdate" content="(.*?)" />''', response_art.text)[0]
    author = re.findall(r'''<meta name="mediaid" content="(.*?)"/>''', response_art.text)[0]
    ress = re.findall(r'''<p.*?>(.*?)</p>''', response_art.text)
    print(src)
    result = "\n".join(ress)
    result1 = re.sub(r'<img.*?/>', "", result)
    result2 = re.sub(r'<iframe.*?iframe>', "", result1).replace('<strong>', '#').replace('</strong>', '#').split('<a')[
        0]  # 去掉图片链接，字体加粗用#替代，匹配到的内容部分有非正文内容，分割并舍弃
    with open(title + '.txt', 'w', encoding='utf-8') as fp:
        fp.write(result2)  # 将内容打印至txt，标题即为文件名
    print("标题：" + title)
    print("时间：" + time)
    print("作者：" + author)
