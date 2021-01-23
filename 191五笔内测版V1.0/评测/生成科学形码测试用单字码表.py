res = ''

with open('191五笔码表.txt') as f:
    for ln in f:
        sp = ln.split()
        code = sp[0]
        for ci in sp[1:]:
            if len(ci) == 1:
                res += ci + '\t' + code + '\n'

with open('191五笔单字评测用码表.txt', 'w') as f:
    f.write(res)
