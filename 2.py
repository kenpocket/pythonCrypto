# import random, sys, os, cryptomath
# import rabinMiller
#
#
# def main():
#     print('生成密钥对.....')
#     # 把字符串al_sweigart'和整数1024传给makeKeyFiles()调用
#     # 公钥私钥保存在al_sweigart-pubkey.txt和al_sweigart-privkey.txt
#     makeKeyFiles('al_sweigart', 1024)
#     print('密钥对制作完成')
#
#
# def generateKey(keysize):
#     print('生成随机大质数p......')
#     p = rabinMiller.generateLargePrime(keysize)
#     print('生成随机大质数q......')
#     q = rabinMiller.generateLargePrime(keysize)
#     # 生成公钥和私钥的公有部分n
#     n = q * p
#     # 创建随机数e，它与q-1和p-1的积互质
#     print('创建随机数e......')
#     while True:
#         # 创建随机数e
#         e = random.randrange(2 ** (keysize - 1), 2 ** (keysize))
#         # 检测e与q - 1和p - 1的积是否互质
#         # 不互质则继续循环，反之则跳出
#         if cryptomath.gcd(e, (p - 1) * (q - 1)) == 1: break
#     print('计算e的逆模d......')
#     d = cryptomath.findModInverse(e, (p - 1) * (q - 1))
#     # 以元组形式进行保存公钥和私钥对
#     publicKey = (n, e)
#     privateKey = (n, d)
#     # 打印操作
#     print('PublicKey:', publicKey)
#     print('PrivateKey', privateKey)
#     return (publicKey, privateKey)
#
#
# # 将公钥私钥保存到txt文件
# def makeKeyFiles(name, keySize):
#     # 如有同名的密钥文件存在，则发出更改名称的警告
#     if os.path.exists('%s_pubkey.txt' % name) or os.path.exists('%s_privkey.txt' % name):
#         sys.exit('WARNING')
#     # 返回一个元组，他包含两个元组，都一样保存在publicKey和privateKey中
#     publicKey, privateKey = generateKey(keySize)
#     # 密钥文件格式：密钥大小整数，n整数，e/d整数
#     # 公钥信息
#     print()
#     print('The public key is a %s and a %s digit number.' % (len(str(publicKey[0])), len(str(publicKey[1]))))
#     print('Writing public key to file %s_pubkey.txt...' % (name))
#     fo = open('%s_pubkey.txt' % (name), 'w')
#     fo.write('%s,%s,%s' % (keySize, publicKey[0], publicKey[1]))
#     fo.close()
#     # 私钥信息
#     print()
#     print('The private key is a %s and a %s digit number.' % (len(str(publicKey[0])), len(str(publicKey[1]))))
#     print('Writing private key to file %s_privkey.txt...' % (name))
#     fo = open('%s_privkey.txt' % (name), 'w')
#     fo.write('%s,%s,%s' % (keySize, privateKey[0], privateKey[1]))
#     fo.close()
#
#
# if __name__ == '__main__':
#     main()
import re
import threading
import pymysql
import requests
import time

uel = 'https://yxy.xcu.edu.cn/xyxw.htm'
uel2 = 'https://yxy.xcu.edu.cn/xyxw/'
harf = []
har = []  # 新闻第一个页面链接(页)
title = []  # 包含新闻第二页面链接(条)
author = []  # 作者以及发表时间
content = []  # 全部返回值(首先包含了作者和时间)
content1 = []  # 文章题目
content2 = []  # 正文
test = []  # url+作者+时间+标题+正文
title1 = []
title2 = []
test1 = []
test2 = []
test3 = []


def resule(url):
    heads = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/99.0.4844.51 Mobile Safari/537.36 '
    }
    res = requests.get(url, headers=heads)
    res.encoding = res.apparent_encoding
    return res.text


def findall(str):
    return re.findall(r''' <li><a href="(.*?)"><span>(.*?)</span>(.*?)</a></li>''', str)


def findharf(str):
    HarfNext = re.findall(r'''上页</a><a href="(.*?)" class="Next">下页''', str)
    return HarfNext


def findContent(str):
    content = re.findall(r'''<h5>(.*?)&nbsp;&nbsp;(.*?)&nbsp;&nbsp;''', str)
    content1 = re.findall(r'''<h4>(.*?)</h4>''', str)
    content2 = re.findall(r'''>(.*?)[。!)>]</p>''', str)  # 文章包含多段
    if not content2:
        content2 = re.findall(r'''>(.*?)[。!)]</span></p>''', str)
    content = ListChang(content, content1)
    content.insert(3, [i for i in content2])
    return content


def ListChang(list1, list2):
    list3 = []
    for i in list1:
        for j in i:
            list3.append(j)
    list3.append(list2[0])
    return list3


for i in range(0, 1):
    if harf:
        harf = findharf(resule(uel2 + harf[0]))
        har.append(uel2 + harf[0])
        harf.append(harf)
    else:
        harf = findharf(resule('https://yxy.xcu.edu.cn/xyxw/34.htm'))
        har.append(uel2 + harf[0])
findall(resule(uel))
for i in har:
    title.append(findall(resule(i)))
for i in title:
    for j in i:
        test.append(uel2 + j[0])
title1 = test[0:int((len(test) - 1) / 2)]
title2 = test[int((len(test) - 1) / 2):len(test)]
title1, title2 = tuple(title1), tuple(title2)


def findtest(lists):
    for i in lists:
        flag = True
        for j in findContent(resule(i)):
            if flag:
                test3.append(i)
                test3.append(j)
                flag = False
            else:
                test3.append(j)


t1 = threading.Thread(target=findtest, args=(title1,))
t1.start()
t2 = threading.Thread(target=findtest, args=(title2,))
t2.start()
test4 = test3
connect = pymysql.connect(host="", user='', password='')
cursor = connect.cursor()
try:
    cursor.execute('''create database reptile;use reptile;''')
    cursor.execute('''Create table if not exists total (_id int auto_increment primary key  ,url varchar(120),author varchar(120),
    ctime varchar(120),title varchar(120),content text);''')
    print('数据库建立成功')
except Exception as e:
    print(e)
while True:
    if not t1.is_alive() and not t2.is_alive():
        break
    else:
        print('有进程尚未完成运行，请稍等')
        time.sleep(0.5)
for i in range(0, len(test4), 5):  # 步长为5
    test4[i + 4] = "".join(test4[i + 4])
    try:
        insert_url = '''insert into reptile.total(url,author,ctime,title,content) value('{}','{}','{}','{}','{}');'''
        print(insert_url)
        a = insert_url.format(test4[i], test4[i + 1], test4[i + 2], test4[i + 3], test4[i + 4])
        cursor.execute(a)
        connect.commit()
        print(a)
    except Exception as e:
        print(e)
