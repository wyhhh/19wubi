from openpyxl import load_workbook
from itertools import islice

# ----- 1. 初始化词频字典和编码字典 --------------------------------------------------
总表 = load_workbook('191五笔词库映射.xlsx', data_only=True)['总表']

词频字典 = {}
编码to词集字典 = {}
优先字集 = set()

for row in islice(总表.values, 1, None):
    词, 词频, 编码, 优先 = row[1], row[2] if row[2] != '#N/A' else 0, row[11], row[12]

    词频字典[词] = 词频
    编码to词集字典.setdefault(编码, []).append(词)
    if 优先:
        优先字集.add(词)


# 初始化完毕
码表 = []
已加的词 = set()

def 添加码表并记录已加词(编码, 词集):
    码表.append((编码, 词集))
    已加的词.update(词集)


# ----- 2. 加入一简 ----------------------------------------------------------------------------------------------------
一简篮子 = [[] for i in range(26)]
for 编码, 词集 in 编码to词集字典.items():
    if len(编码) == 4: continue
    第一码 = 编码[0]
    for 词 in 词集:
        # 一简只能有单字，即词长度==1
        if len(词) == 1:
            一简篮子[ord(第一码) - 97].append(词)

# 排序篮子的每个子篮子
for i, 子篮子 in enumerate(一简篮子):
    子篮子.sort(key=词频字典.get, reverse=True)
    前三个 = 子篮子[:3]
    添加码表并记录已加词(chr(97 + i), 前三个)

# 一简加入完毕

# ----- 3. 加入二简 ---------------------------------------------------------------
二简篮子 = {}
for 编码, 词集 in 编码to词集字典.items():
    if len(编码) == 4: continue
    前两码 = 编码[:2]
    for 词 in 词集:
        if 词 in 已加的词 or len(词) == 3: continue
        二简篮子.setdefault(前两码, []).append(词)


def sorter(字):
    字频 = 词频字典[字]
    if 字 in 优先字集:
        字频 += 2000_0000
    return 字频


for 二码, 字集 in 二简篮子.items():
    字集.sort(key=sorter, reverse=True)
    前三个 = sorted(字集[:3], key=词频字典.get, reverse=True)

    添加码表并记录已加词(二码, 前三个)


# ------ 4. 加入三简 ----------------------------------------------------------------------------
def sorter(词):
    词频 = 词频字典[词]
    if len(词) == 3:
        词频 += 2000_0000
    return 词频


for 编码, 词集 in 编码to词集字典.items():
    if len(编码) == 3:
        l = []
        for 词 in 词集:
            if 词 in 已加的词: continue
            l.append(词)
        if l:
            l.sort(key=sorter, reverse=True)
            码表.append((编码, l))

# ------- 5. 加入四简 ---------------------------------------------------------
for 编码, 词集 in 编码to词集字典.items():
    if len(编码) == 4:
        词集.sort(key=词频字典.get, reverse=True)
        码表.append((编码, 词集))


# ------ 6. 排序码表并输出文件 ----------------------------------------------------
def sorter(tup):
    编码 = tup[0]
    sum = 0
    radix_exp = 0
    for 字母 in 编码[::-1]:
        sum += (ord(字母) - 97 + 1) * 26 ** radix_exp
        radix_exp += 1
    return sum


码表.sort(key=sorter)

out_path = '191五笔码表.txt'

with open(out_path, 'w') as f:
    for 编码, 词集 in 码表:
        f.write(编码)
        for 词 in 词集:
            f.write('\t' + 词)
        f.write('\n')
    with open('emoji.txt') as emj:
        f.write(emj.read())
