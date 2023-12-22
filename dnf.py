def get_table(n):
    table = []
    for i in range(1, 2 ** n + 1):
        temp = [i <= 2 ** (n - 1)]
        # 4
        if n == 2:
            temp.append(i % 2 == 1)
        elif n == 3:
            temp.append(1 <= i % 2 ** (n - 1) <= 2)
            temp.append(i % 2 ** (n - 2) == 1)
        elif n == 4:
            temp.append(1 <= i % 2 ** (n - 1) <= 4)
            temp.append(1 <= i % 2 ** (n - 2) <= 2)
            temp.append(i % 2 ** (n - 3) == 1)
        table.append(temp)
    return table

def negation(s):
    arr = s.split()
    for i in range(len(arr)):
        #(-a) or -a
        if ("-" in arr[i] and n == 1) or ("-" in arr[i] and len(arr[i]) == 2):
            found = arr[i].find("-")
            arr[i] = arr[i][:found] + arr[i][found+1:]
        #(a) or a
        elif ("-" not in arr[i] and n == 1) or ("-" not in arr[i] and len(arr[i]) == 1 and arr[i].isalpha()):
            counted = arr[i].count('(')
            arr[i] = arr[i][:counted] + '-' + arr[i][counted:]

        elif arr[i] == "&":
            arr[i] = "|"
        elif arr[i] == "|":
            arr[i] = "&"

        # ((((a
        elif "(" in arr[i]:
            if "-" not in arr[i]:
                if arr[i].count("(") != len(arr[i]):
                    arr[i] = arr[i][:-1] + '-' + arr[i][-1]
            #(((-a
            elif arr[i][-2] == "-":
                arr[i] = arr[i][:-2] + arr[i][-1]
            # ((-((a | b) | b))) or -(((a
            elif "-" in arr[i]:
                found = arr[i].find("-")
                # print(arr[i])
                opening_parenthesis, closing_parenthesis = 0, 0
                current_open, current_close = found+1, 0
                for j in range(found+1, len(s)):
                    if s[j] == "(":
                        opening_parenthesis += 1
                    elif s[j] == ")":
                        closing_parenthesis += 1
                        current_close = j
                    if opening_parenthesis == closing_parenthesis != 0:
                        break
                x = s[:found] + negation(s[current_open: current_close+1])[:-1] + s[current_close+1:]
                # print(x)
                if n != 1:
                    return negation(x)
                else:
                    arr[i] = x.split()[0]
        #a))))
        elif ")" in arr[i]:
            if "-" not in arr[i]:
                if arr[i].count(")") != len(arr[i]):
                    arr[i] = '-' + arr[i]
            #-a))))
            elif "-" in arr[i]:
                arr[i] = arr[i][1:]
    return ' '.join(arr) + ' '


def dnf(n, s):
    ans, table = '', get_table(n)
    for i in range(len(s)):
        # -(((a | b))) ((-(a | b)))
        #arrow
        if s.find("r", i, len(s) - 1) != -1:
            found = s.find("r", i)
            s = s.replace("r", "|", 1)
            # print(s)
            temp = s[:found-1]
            start, end, opening_parenthesis, closing_parenthesis = 0, 0, 0, 0
            current_open, current_close = 0, 0
            # print(temp)
            for j in range(len(temp)-1, -1, -1):
                # print(temp[j])
                if temp[j] == ")":
                    closing_parenthesis += 1
                    current_close = j
                elif temp[j] == "(":
                    opening_parenthesis += 1
                    current_open = j
                if opening_parenthesis == closing_parenthesis != 0:
                    break
            if current_close != 0:
                s = s[:current_open] + negation(s[current_open: current_close+1]) + s[current_close+1:]
            else:
                s = s[:current_open] + negation(s[current_open:found]) + s[found:]
            # -()
            if s.find("-(", i, len(s) - 1) != -1:
                found = s.find("-(", i, len(s) - 1)
                opening_parenthesis, closing_parenthesis = 0, 0
                current_open, current_close = found, 0
                for j in range(found, len(s)):
                    if s[j] == "(":
                        opening_parenthesis += 1
                    elif s[j] == ")":
                        current_close = j
                        closing_parenthesis += 1
                    if opening_parenthesis == closing_parenthesis != 0:
                        break
                s = s[:found] + s[found:].replace("-(", "(", 1)
                # print(s, current_close)
                current_close -= 1
                print(s[current_close], s[current_open + 1:current_close])
                s = s[:found + 1] + negation(s[current_open + 1:current_close]) + s[current_close:]
    print(s)
    # last step with | and & and paranthesis
    for i in table:
        temp = s
        for j in range(len(i)):
            # print(t)
            if j == 0:
                temp = temp.replace("-a", str(int(not i[j])))
                temp = temp.replace("a", str(int(i[j])))
            elif j == 1:
                temp = temp.replace("-b", str(int(not i[j])))
                temp = temp.replace("b", str(int(i[j])))
            elif j == 2:
                temp = temp.replace("-c", str(int(not i[j])))
                temp = temp.replace("c", str(int(i[j])))
            elif j == 3:
                temp = temp.replace("-d", str(int(not i[j])))
                temp = temp.replace("d", str(int(i[j])))
        # print(i, end=' ')
        # print(temp)
        # print(eval(temp))

        if eval(temp):
            if n == 1:
                ans += f' | {"a" if i[0] else "-a"}'
            elif n == 2:
                ans += f' | {"a" if i[0] else "-a"}{" & b" if i[1] else " & -b"}'
            elif n == 3:
                ans += f' | {"a" if i[0] else "-a"}{" & b" if i[1] else " & -b"}{" & c" if i[2] else " & -c"}'
            elif n == 4:
                ans += f' | {"a" if i[0] else "-a"}{" & b" if i[1] else " & -b"}{" & c" if i[2] else " & -c"}{" & d" if i[3] else " & -d"}'

    return ans[3:]





if __name__ == '__main__':
    n = int(input("num of variables: "))
    s = input("expression: ")
    print(dnf(n, s))