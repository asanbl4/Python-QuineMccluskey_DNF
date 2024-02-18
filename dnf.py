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
        if arr[i] == "&":
            arr[i] = "|"
        elif arr[i] == "|":
            arr[i] = "&"
        # (-a
        elif "-" in arr[i]:
            found = arr[i].find("-")
            # (-a or -a
            if found == len(arr[i]) - 2:
                arr[i] = arr[i][:found] + arr[i][found + 1:]
            # ((-(a
            else:
                # if s is for instance (-(a | b) & (a & b))
                opening, closing, j = arr[i][found:].count("("), 0, i + 1
                while opening > closing:
                    opening += arr[j].count("(")
                    closing += arr[j].count(")")
                    j += 1
                i = j
                continue
        # (a
        elif "-" not in arr[i]:
            counted = arr[i].count('(')
            arr[i] = arr[i][:counted] + '-' + arr[i][counted:]

    return ' '.join(arr) + ' '


def dnf(number_of_variables, expression):
    ans, table = '', get_table(number_of_variables)
    for i in range(len(expression)):
        # -()
        if expression.find("-(", i, len(expression) - 1) != -1:
            found = expression.find("-(", i, len(expression) - 1)
            opening_parenthesis, closing_parenthesis = 0, 0
            current_open, current_close = found, 0
            for j in range(found, len(expression)):
                if expression[j] == "(":
                    opening_parenthesis += 1
                elif expression[j] == ")":
                    current_close = j
                    closing_parenthesis += 1
                if opening_parenthesis == closing_parenthesis != 0:
                    break
            expression = expression[:found] + expression[found:].replace("-(", "(", 1)
            current_close -= 1
            expression = expression[:found + 1] + negation(expression[current_open + 1:current_close]) + expression[current_close:]
        # arrow
        if expression.find("r", i, len(expression) - 1) != -1:
            found = expression.find("r", i)
            expression = expression.replace("r", "|", 1)
            temp = expression[:found - 1]
            start, end, opening_parenthesis, closing_parenthesis = 0, 0, 0, 0
            current_open, current_close = 0, 0
            # print(temp)
            for j in range(len(temp) - 1, -1, -1):
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
                expression = expression[:current_open] + negation(expression[current_open: current_close + 1]) + expression[current_close + 1:]
            else:
                expression = expression[:current_open] + negation(expression[current_open:found]) + expression[found:]
    print(f"Our converted function: {expression}")
    # last step with | and & and paranthesis
    for i in table:
        temp = expression
        # replacing letters with 0's and 1's from the truth table
        for j in range(len(i)):
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
        # checking if the result is 1, then adding it to the final answer
        if eval(temp):
            if number_of_variables == 1:
                ans += f' | {"a" if i[0] else "-a"}'
            elif number_of_variables == 2:
                ans += f' | {"a" if i[0] else "-a"}{" & b" if i[1] else " & -b"}'
            elif number_of_variables == 3:
                ans += f' | {"a" if i[0] else "-a"}{" & b" if i[1] else " & -b"}{" & c" if i[2] else " & -c"}'
            elif number_of_variables == 4:
                ans += f' | {"a" if i[0] else "-a"}{" & b" if i[1] else " & -b"}{" & c" if i[2] else " & -c"}{" & d" if i[3] else " & -d"}'

    return ans[3:]


if __name__ == '__main__':
    n = int(input("Enter the number of variables: "))
    s = input("Your boolean expression: ")
    print(dnf(number_of_variables=n, expression=s))
    # 2
    # (-(a | b) & (a & b))
