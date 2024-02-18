def to_boolean(variables):
    for i in range(len(variables)):
        for j in range(len(variables[i])):
            if variables[i][j].find("-") != -1:
                variables[i][j] = 0
            else:
                variables[i][j] = 1
    return variables


def solve(number_of_variables, dnf):
    variables = to_boolean([i.split(" & ") for i in dnf.split(" | ")])
    d = {}
    for i in variables:
        temp = d.get(sum(i))
        if temp:
            temp.append(i)
            d[sum(i)] = temp
        else:
            d[sum(i)] = [i]
    d = dict(sorted(d.items(), reverse=True))
    flags = {False: [],
             True: []}
    for i in d.values():
        for j in i:
            flags[False].append(j)
    next1, ans = [], []
    for key in d.keys():
        for i in d.get(key):
            next1.append(i)
    while True:
        next_step = []
        for i in range(len(next1) - 1):
            for j in range(i + 1, len(next1)):
                l1, l2 = next1[i], next1[j]
                equals, add = 0, []
                for k in range(number_of_variables):
                    if l1[k] == l2[k]:
                        add.append(l1[k])
                        equals += 1
                    else:
                        add.append("_")
                if equals == number_of_variables - 1:
                    if l1 in flags.get(False):
                        flags[True].append(l1)
                        flags[False].remove(l1)
                    if l2 in flags.get(False):
                        flags[True].append(l2)
                        flags[False].remove(l2)
                    next_step.append(add)
        next1 = next_step
        if flags.get(False):
            ans.append(flags.get(False))
        flags = {False: [i for i in next1],
                 True: []}
        if not next_step:
            break
    anss = []
    for i in ans:
        for j in i:
            t = []
            for k in range(number_of_variables):
                if k == 0:
                    if j[k] == 1:
                        t.append("a")
                    elif j[k] == 0:
                        t.append("-a")
                elif k == 1:
                    if j[k] == 1:
                        t.append("b")
                    elif j[k] == 0:
                        t.append("-b")
                elif k == 2:
                    if j[k] == 1:
                        t.append("c")
                    elif j[k] == 0:
                        t.append("-c")
                elif k == 3:
                    if j[k] == 1:
                        t.append("d")
                    elif j[k] == 0:
                        t.append("-d")
            anss.append(t)
    ans = []
    for i in anss:
        if i not in ans:
            ans.append(i)
    value = ''
    for i in ans:
        value += ' & '.join(i)
        value += ' | '
    print(value[:-3])


if __name__ == '__main__':
    n = int(input("num of variables: "))
    s = input("dnf: ")
    solve(n, s)
# a & b | -a & b | a & -b
# p & q & r | p & q & -r | p & -q & r | -p & q & -r | p & -q & -r
#