import requests
import re
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0"
}
import threading

# def print_hi(name):
#     # 在下面的代码行中使用断点来调试脚本。
#     print(f'Hi, {name}')  # 按 Ctrl+F8 切换断点。


# 按间距中的绿色按钮以运行脚本。
# if __name__ == '__main__':
#     print_hi('PyCharm')

# 访问 https://www.jetbrains.com/help/pycharm/ 获取 PyCharm 帮助


url = 'https://cailiao.xcu.edu.cn/xsky/13.htm'


def grt_next(url):
    response = requests.get(url, headers=header)
    response.encoding = response.apparent_encoding
    text = response.text
    # try:
    #     res = re.findall(r'''上页</a><a href="(.*?)" class="Next">下页''', text)[0]
    #     print(res)
    #     grt_next('https://cailiao.xcu.edu.cn/xsky/' + res)
    #
    # except IndexError:
    #     print('遍历结束')
    while re.findall(r'''上页</a><a href="(.*?)" class="Next">下页''', text):
        res = re.findall(r'''上页</a><a href="(.*?)" class="Next">下页''', text)[0]
        response = requests.get('https://cailiao.xcu.edu.cn/xsky/' + res, headers=header)
        response.encoding = response.apparent_encoding
        text = response.text
        yield res

if __name__ == '__main__':
    # for i in grt_next(url):
    #     pass
    pass