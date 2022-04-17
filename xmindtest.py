import xmind

w = xmind.load("test.xmind")
s1 = w.getPrimarySheet()  # get the first sheet
s1.setTitle("r3kapig技能栈1.0")  # set its title
r1 = s1.getRootTopic()  # 创建根节点
r1.setTitle("技能")  # 给根节点命名
file = open('c.txt', 'r', encoding='utf-8')
value = [i.replace('"label": ', '').replace('\n', '').replace(',', '') for i in file if 'label' in i]
last_num = 1
for i in value:
    counts = (i.split('"')[0].count(' ') // 4 + 1) // 2 + 1
    print(counts)
    locals()['r' + str(counts)] = locals()['r' + str(counts - 1)].addSubTopic()
    locals()['r' + str(counts)].setTitle(i.replace('"', ''))
    last_num = counts

xmind.save(w, "test.xmind")
