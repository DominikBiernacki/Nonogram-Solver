import copy

file = open("input.txt", "r")
x, y = file.readline().split(" ")
x = int(x)
y = int(y)

cols = []
for i in range(x):
    cols.append(list(map(int, file.readline().split(" "))))

rows = []
for i in range(y):
    rows.append(list(map(int, file.readline().split(" "))))

file.close()

board = []
for i in range(x):
    line = []
    for j in range(y):
        line.append(-1)
    board.append(line)

blanks = x * y


def get_domain(length, dists):
    def true_get_domain(length, dists, current=0, results=None):
        if results is None:
            results = []
        if len(dists) == 0:
            return [tuple(results)]
        total_needed = len(dists) - 1
        for dist in dists:
            total_needed += dist
        if total_needed > length:
            return []
        return true_get_domain(length - 1, dists, current + 1, results) + \
            true_get_domain(length - dists[0] - 1, dists[1:], current + dists[0] + 1, results + [(current, dists[0])])

    domains = true_get_domain(length, dists)
    strings = []
    for i in range(len(domains)):
        s = "0" * length
        for block in domains[i]:
            s = s[:block[0]] + "1" * block[1] + s[block[0] + block[1]:]
        strings.append(s)
    return strings


rows_domains = []
for row in rows:
    rows_domains.append(get_domain(x, row))

cols_domains = []
for col in cols:
    cols_domains.append(get_domain(y, col))

backtrack = []


def backtrack_step():
    global backtrack, rows_domains, cols_domains, blanks, board
    while backtrack[-1][0] == 0:
        backtrack.pop()
    backtrack[-1][0] = 0
    rows_domains = backtrack[-1][3]
    cols_domains = backtrack[-1][4]
    blanks = backtrack[-1][5]
    board = backtrack[-1][6]
    temp_x = backtrack[-1][1]
    temp_y = backtrack[-1][2]
    board[temp_x][temp_y] = 0
    blanks -= 1
    k = 0
    while k < len(cols_domains[temp_x]):
        if cols_domains[temp_x][k][temp_y] != "0":
            cols_domains[temp_x].remove(cols_domains[temp_x][k])
        else:
            k += 1
    while k < len(rows_domains[temp_y]):
        if rows_domains[temp_y][k][temp_x] != "0":
            rows_domains[temp_y].remove(rows_domains[temp_y][k])
        else:
            k += 1


while blanks > 0:
    changed = False
    for i in range(x):
        for j in range(y):
            if board[i][j] == -1:
                state = rows_domains[j][0][i]
                good = True
                for domain in rows_domains[j]:
                    if domain[i] != state:
                        good = False
                        break
                if good:
                    board[i][j] = int(state)
                    blanks -= 1
                    changed = True
                    k = 0
                    while k < len(cols_domains[i]):
                        if cols_domains[i][k][j] != state:
                            cols_domains[i].remove(cols_domains[i][k])
                        else:
                            k += 1
                    if len(cols_domains[i]) == 0:
                        backtrack_step()
                else:
                    state = cols_domains[i][0][j]
                    good = True
                    for domain in cols_domains[i]:
                        if domain[j] != state:
                            good = False
                            break
                    if good:
                        board[i][j] = int(state)
                        blanks -= 1
                        changed = True
                        k = 0
                        while k < len(rows_domains[j]):
                            if rows_domains[j][k][i] != state:
                                rows_domains[j].remove(rows_domains[j][k])
                            else:
                                k += 1
                        if len(cols_domains[i]) == 0:
                            backtrack_step()
    if not changed:
        chosen = False
        for i in range(x):
            for j in range(y):
                if board[i][j] == -1:
                    temp_x = i
                    temp_y = j
                    chosen = True
                    break
            if chosen:
                break
        backtrack.append([1, temp_x, temp_y, copy.deepcopy(rows_domains),
                          copy.deepcopy(cols_domains), blanks, copy.deepcopy(board)])
        board[temp_x][temp_y] = 1
        blanks -= 1
        k = 0
        while k < len(cols_domains[temp_x]):
            if cols_domains[temp_x][k][temp_y] != "1":
                cols_domains[temp_x].remove(cols_domains[temp_x][k])
            else:
                k += 1
        while k < len(rows_domains[temp_y]):
            if rows_domains[temp_y][k][temp_x] != "1":
                rows_domains[temp_y].remove(rows_domains[temp_y][k])
            else:
                k += 1


def to_char(number):
    if number == 0:
        return "."
    return "#"


file = open("output.txt", "w")
for i in range(x):
    line = ""
    for j in range(y):
        line += to_char(board[i][j])
    file.write(line + "\n")
    print(line)
