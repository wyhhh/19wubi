emoji_set = set()

with open('../emoji.txt') as f:
    for ln in f:
        sp = ln.split()
        emoji_set.add(sp[1])

with open('../191五笔码表.txt') as f:
    with open('191五笔多多格式码表.txt', 'w', encoding='gbk') as out:
        for ln in f:
            sp = ln.split()
            code = sp[0]
            for ci in sp[1:]:
                if ci in emoji_set: break
                out.write(ci + '\t' + code + '\n')
