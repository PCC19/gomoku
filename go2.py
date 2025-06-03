import copy

def read_gomoku_board(file_path, board):
    black_pieces = []
    white_pieces = []

    with open(file_path, 'r') as file:
        for row_index, line in enumerate(file):
            for col_index, char in enumerate(line.strip()):
                if char == '@':
                    board[col_index][row_index] = '@'
                elif char == 'O':
                    board[col_index][row_index] = 'O'
    return board

def draw_gomoku_board(board_size, board, highlight_coord=None):
    RED = '\033[91m'
    RED = '\033[34m'
    RESET = '\033[0m'

    # Prepare labels with 3 digits, starting from 1
    col_labels = [f"{i-1 +1:2}" for i in range(board_size)]
    row_labels = [f"{i-1 +1:2}" for i in range(board_size)]

    # Draw the board
    print('  ' + ' '.join(col_labels))
    for y in range(board_size):
        row_str = f"{row_labels[y]} "
        for x in range(board_size):
            cell = board[x][y]
            if highlight_coord[0] == x and highlight_coord[1] == y:
                cell = f"{RED}{cell}{RESET}"
            row_str += cell + '  '
        print(row_str.rstrip())

def is_valid (x, y, board_size):
    if (x in range(0, board_size)) and (y in range(0, board_size)):
        return True
    return False

def is_empty (x, y, board):
    if board[x][y] == '.':
        return True
    return False

def update_board(x, y, color, board):
    if color == "WHITE":
        board[x][y] = "O"
    if color == "BLACK":
        board[x][y] = "@"
    return board

def toggle_turn(color):
    if color == "WHITE":
        return "BLACK"
    if color == "BLACK":
        return "WHITE"
    return "ERROR"

def go_first(x, y, char, board, dx, dy, board_size):
    while (is_valid(x, y, board_size)):
        if (board[x][y] == char):
            return x, y
        x += dx
        y += dy
    return None, None

def go_last(x, y, char, board, dx, dy, board_size):
    while (board[x][y] == char):
        x += dx
        y += dy
        if (not is_valid(x, y, board_size)):
            return x - dx, y - dy
    return x - dx, y - dy

def get_ini(x, y, dx, dy, board, board_size):
    ini = ()
    if (not is_valid(x,y, board_size)):
        return ini
    x_ini = x - dx
    y_ini = y - dy
    if (is_valid(x_ini, y_ini, board_size) and board[x_ini][y_ini] == '.'):
        ini = (x_ini, y_ini)
    return ini

def get_fin(x,y, dx, dy, board, board_size):
    fin = ()
    x_fin = x + dx
    y_fin = y + dy
    if (is_valid(x_fin, y_fin, board_size) and board[x_fin][y_fin] == '.'):
        fin = (x_fin, y_fin)
    return fin

def get_lines(x, y, char, board, dx, dy, board_size):
    # faz loop a partir do ponto de partida ate final do bound ou board
    lines = []
    while(is_valid(x, y, board_size)):
        # vai ate primeria peca
        xf, yf = go_first(x,y,char, board, dx, dy, board_size)
        if (not is_valid(xf, yf, board_size)):
            return lines
        # pega coordenada da antecessora se tiver
        ini = get_ini(xf, yf, dx, dy, board, board_size)
        # vai ate ultima peca
        xl, yl = go_last(xf, yf, char, board, dx, dy, board_size)
        # calcula tamanho
        size = max(xl - xf, yl - yf) + 1
        # pega coordenada da sucessora se houver
        fin = get_fin(xl, yl, dx, dy, board, board_size)
        kind = 2;
        if not ini:
            kind -= 1
        if not fin:
            kind -= 1
        dic = {"p": char, "size":size, "dir":(dx,dy), "f": (xf, yf), "l": (xl, yl), "kind": kind, "ini":ini, "fin":fin}
        # append dic na lista
        lines.append(dic)
        x = xl + dx
        y = yl + dy
    return lines

def scan(char, board, board_size):
    all_lines = []
    # vertical scan
    dx = 0
    dy = 1
    for x in range(0,board_size):
        line = get_lines(x, 0, char, board, dx, dy, board_size) 
        if line:
            all_lines += line
    # horizontal scan
    dx = 1
    dy = 0
    for y in range(0,board_size):
        line = get_lines(0, y, char, board, dx, dy, board_size) 
        if line:
            all_lines += line
    # diagonal up scan
    dx = 1
    dy = -1
    for y in range(0, board_size):
        line = get_lines(0, y, char, board, dx, dy, board_size) 
        if line:
            all_lines += line
    for x in range(1, board_size):
        line = get_lines(x, board_size - 1, char, board, dx, dy, board_size) 
        if line:
            all_lines += line
    # diagonal down scan
    dx = 1
    dy = 1
    for y in range(0, board_size):
        line = get_lines(0, y, char, board, dx, dy, board_size) 
        if line:
            all_lines += line
    for x in range(1, board_size):
        line = get_lines(x, 0, char, board, dx, dy, board_size) 
        if line:
            all_lines += line

    return all_lines

def save_list(file_name, list_to_save):
    with open(file_name, 'w') as file:
        for item in list_to_save:
            file.write(f"{item}\n")


def update_state(x, y, turn_is, board, board_size):
    board = update_board(x, y, turn_is, board)
    black_lines = scan('@', board, board_size)
    white_lines = scan('O', board, board_size)
    lines = black_lines + white_lines
    return board, lines

def capture(x, y, turn_is, board, lines, score):
    if turn_is == 'BLACK':
        p = 'O'
    else:
        p = '@'
    duplas = [d for d in lines if d['p'] == p and d['size'] == 2 and d['kind'] == 1 and (d['ini'] == (x,y) or d['fin'] == (x,y))]
    print("duplas:\n")
    for line in duplas:
        print(line)
    if duplas:
        for line in duplas:
            remove_piece(line['f'], board)
            remove_piece(line['l'], board)
            score[turn_is] += 2
    return board, score

def remove_piece(piece, board):
    x, y = piece
    board[x][y] = '.'

def check_free3(x, y, turn_is, board, board_size):
    count = 0
    _ , lines =  update_state(x, y, turn_is, copy.deepcopy(board), board_size)
    # CASE 3 ========================================================================
    case3 = []
    # Find lines with size 3
    temp = [line for line in lines if line['size'] == 3 and line['kind'] == 2]
    for linha in temp:
        x1, y1 = linha['f']
        x2, y2 = linha['l']
        # Check if x,y belongs to the line
        if x >= x1 and x<= x2 and y >= y1 and y <= y2:
            case3.append(linha)
    count += len(case3)
    print("case3:", count)
    for linha in case3:
        print(linha)
    # CASE 1 ========================================================================
    case1 = []
    # find lines size = 1 and kind = 2 containing the piece x,y
    temp = [line for line in lines if line['f'] == (x,y) and line['kind'] == 2 and line['size'] == 1]
    # for each size 1 line find size 2 lines in the same dir and adjacent
    for linha in temp:
        d = linha['dir']
        fin = linha['fin']
        ini = linha['ini']
        temp2 = [line for line in lines if (line['ini'] == fin or line['fin'] == ini) and line['dir'] == d and line['size'] == 2]
        if temp2:
            case1.append(temp2)
    count += len(case1)
    print("temp:", count)
    for linha in temp:
        print(linha)
    print("case1:", count)
    for linha in case1:
        print(linha)
    # CASE 2 ========================================================================
    case2 = []
    # find lines size = 2 and kind = 2 containing the piece x,y
    temp = [line for line in lines if line['size'] == 2 and line['kind'] == 2 and (line['f'] == (x,y) or line['l'] == (x,y))]
    # for each size 2 line find size 1 lines in the same dir and adjacent
    for linha in temp:
        d = linha['dir']
        fin = linha['fin']
        ini = linha['ini']
        temp2 = [line for line in lines if (line['ini'] == fin or line['fin'] == ini) and line['dir'] == d and line['size'] == 1]
        if temp2:
            case2.append(temp2)
    count += len(case2)
    print("temp:", count)
    for linha in temp:
        print(linha)
    print("case2:",count) 
    for linha in case2:
        print(linha)

    if count > 1:
        print("Invalid move: 2 free-3 !")
        return False

    return True


def main():
    # INITIALIZE
    board_size = 19
    board = [['.' for _ in range(board_size)] for _ in range(board_size)]
    highlight_coord = (8, 7)  # This cell will be printed in red
    board_file = "board3"
    board = read_gomoku_board(board_file, board)
    draw_gomoku_board(board_size, board, highlight_coord)
    score = {"WHITE":0 , "BLACK": 0}

    # GAME LOOP
    old = []
    lines = []
    duplas = []
    turn_is = 'BLACK'
    while (True):
        # UPDATE MOVE
        coords = input(f'\n{turn_is} input move [x y]: ')
        old = lines;
        x, y = map(int, coords.split())
        if (is_valid(x,y, board_size) and is_empty(x,y, board) and check_free3(x, y, turn_is, copy.deepcopy(board), board_size)):
            # CHECK 2 free-three
            print("Valid move !")
            # CHECK CAPTURE
            board, score = capture(x, y, turn_is, copy.deepcopy(board), lines, score)
            # UPDATE STATE
            board, lines =  update_state(x, y, turn_is, board, board_size)
            turn_is = toggle_turn(turn_is)
        else:
            print("Invalid move !")

        #DRAW BOARD
        draw_gomoku_board(board_size, board, (x,y))
        print("Score", score)
        
#        for line in lines:
#            print(line)
        save_list('old', old)
        save_list('new', lines)

if __name__ == "__main__":
    main()
