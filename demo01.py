import re
import threading
import requests
import pymysql

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0"}
URL = 'https://waiyu.xcu.edu.cn/'
click_url = 'https://waiyu.xcu.edu.cn/system/resource/code/news/click/dynclicks.jsp?clickid={}&owner={}&clicktype={}'
connect = pymysql.connect(host='120.27.162.128', user='ggs', password='ggs001',database='spider')
cursor = connect.cursor()
ins_sql = '''insert into datas (content, author, title, url, times, shenHe, click) values'''
ins_sql_part = '''('{}', '{}','{}', '{}', '{}', '{}',{})'''


def parse_news(values):
    return_d = []
    for news_url, title in values:
        if 'http' not in news_url:
            news_url = URL+news_url
        response = requests.get(news_url, headers=headers)
        if 'xcu.edu' not in news_url:
            print("Invalid url:", news_url)
            continue
        response.encoding = response.apparent_encoding
        text = response.text
        if '撤销' in text:
            print('empty url:', news_url)
            continue
        content = re.findall(r'''<span.*?>(.*?)</span>''', text, re.S)
        content = re.sub(r'''<.*?>''', '', ''.join(content)).replace('&nbsp;', '').replace(' ', '')
        content = content.replace('\r\n', '\n').replace('\n\n', '\n').replace('\n\n', '\n')
        comp = re.compile(r'''([\u4e00-\u9fa5]|\d+)\s+([\u4e00-\u9fa5]|\d+)''')
        content = comp.sub(r'\1\2', content)
        comp = re.compile(r'''([\u4e00-\u9fa5]|\d+)\s+([\u4e00-\u9fa5]|\d+)''')
        content = comp.sub(r'\1\2', content)
        try:
            author, shenHe, times, clicktype, owner, clickid = \
                re.findall(r'''作者：(.*?)审核：(.*?)时间：(.*?)    点击数：<script>_showDynClicks\("(.*?)", (\d+), (\d+)\)</script>''',
                        text)[0]
        except Exception as e:
            print(e)
            print(text)
            print(news_url)
            break
        author = re.sub(r' ', '', author)
        shenHe = re.sub(r' ', '', shenHe)
        times = re.sub(r' ', '', times)
        if author.isspace():
            author = 'unknown'
        if shenHe.isspace():
            shenHe = 'unknown'
        if times.isspace():
            times = 'unknown'
        url = click_url.format(clickid, owner, clicktype)
        click = requests.get(url, headers=headers).text  # type:str
        return_d.append((content, author, title, news_url, times, shenHe, int(click)))
    return_d = list(set(return_d))
    if insert_sql(connect, return_d):
        print('本线程插入完成')
    else:
        print('数据库插入失败')


def insert_sql(connect: pymysql.Connection, tuples):
    connect = pymysql.connect(host='120.27.162.128', user='ggs', password='ggs001', database='spider')
    cursor = connect.cursor()
    sql = ''
    for i in tuples:
        sql += ins_sql_part.format(*i)
        sql += ','
    sql = ins_sql + sql + ';'
    sql = sql.replace(',;', ';')
    try:
        cursor.execute(sql)
        connect.commit()
        return True
    except Exception as e:
        print(e)
        return False


def get_content_title(url):
    response = requests.get(url, headers=headers)
    response.encoding = response.apparent_encoding
    text = response.text
    test = re.findall(r'''<li id=".*?"><a href="(.*?)"><span>.*?</span><em>(.*?)</em></a></li>''', text)
    test = [tuple([re.sub(r'\.\./\.\./', URL, i[0]), i[1]]) for i in test]
    return test


def get_more(url):  # 第一步
    a = {}
    response = requests.get(url, headers=headers)
    response.encoding = response.apparent_encoding
    matches = re.findall(r'''<h2>([\u4e00-\u9fa5]+)</h2><span><a href="(.*?)".*?><img src=".*?more.png"></a></span>''',
                         response.text, re.I)
    for i in matches:
        a[i[0]] = i[1] if 'index' in i[1] or 'https' in i[1] else i[1].split('/')[0] + '.htm'
        a[i[0]] = a[i[0]] if 'https:' in a[i[0]] else URL + a[i[0]]
    return a


def get_pages(url):  # 第二步
    response = requests.get(url, headers=headers)
    response.encoding = response.apparent_encoding
    text = response.text
    _, page = re.findall(r'''共(\d+)条&nbsp;&nbsp;1/(\d+)&nbsp;''', text, re.I)[0]
    page1 = get_content_title(url)
    for x in range(int(page) - 1, 0, -1):
        url_2 = re.sub(r'\.htm', '/' + str(x) + '.htm', url)
        print(url_2)
        page1 += get_content_title(url_2)
    return page1


if __name__ == '__main__':
    a = get_more(URL)
    for i in a:
        values = get_pages(a[i])
        locals()[i] = threading.Thread(target=parse_news, args=(values,))
        locals()[i].start()

