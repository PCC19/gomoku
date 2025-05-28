
def read_gomoku_board(file_path, board):
    black_pieces = []
    white_pieces = []

    with open(file_path, 'r') as file:
        for row_index, line in enumerate(file):
            for col_index, char in enumerate(line.strip()):
                if char == '@':
                    black_pieces.append((col_index, row_index))
                    board[col_index][row_index] = '@'
                elif char == 'O':
                    white_pieces.append((col_index, row_index))
                    board[col_index][row_index] = 'O'
    return black_pieces, white_pieces, board

def draw_gomoku_board(board_size, black_pieces, white_pieces, board, highlight_coord=None):
    RED = '\033[91m'
    RED = '\033[34m'
    RESET = '\033[0m'

    # Prepare labels with 3 digits, starting from 1
    col_labels = [f"{i-1 +1:2}" for i in range(board_size)]
    row_labels = [f"{i-1 +1:2}" for i in range(board_size)]

    # Create an empty board
    board = [['.' for _ in range(board_size)] for _ in range(board_size)]

    # Place black pieces
    for x, y in black_pieces:
        if 0 <= x < board_size and 0 <= y < board_size:
            board[x][y] = '@'

    # Place white pieces
    for x, y in white_pieces:
        if 0 <= x < board_size and 0 <= y < board_size:
            board[x][y] = 'O'

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

def is_empty (x, y, white_pieces, black_pieces):
    if ((x,y) not in black_pieces and (x,y) not in white_pieces):
        return True
    return False

def update_board(x, y, color, white_pieces, black_pieces, board):
    if color == "WHITE":
        white_pieces.append((x,y))
        white_pieces.sort()
        board[x][y] = "O"
    if color == "BLACK":
        black_pieces.append((x,y))
        black_pieces.sort()
        board[x][y] = "@"
    return white_pieces, black_pieces, board

def toggle_turn(color):
    if color == "WHITE":
        return "BLACK"
    if color == "BLACK":
        return "WHITE"
    return "ERROR"

def get_bounds(coord_list):
    xs, ys = zip(*coord_list)
    return min(xs), max(xs), min(ys), max(ys)

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
        dic = {"size":size, "dir":(dx,dy), "f": (xf, yf), "l": (xl, yl), "kind": kind, "ini":ini, "fin":fin}
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

def main():
    # INITIALIZE
    board_size = 19
    board = [['.' for _ in range(board_size)] for _ in range(board_size)]
    #black_pieces = [(7, 7), (8, 7), (9, 7)]
    #white_pieces = [(7, 8), (8, 8), (9, 8)]
    highlight_coord = (8, 7)  # This cell will be printed in red
    board_file = "board1"
    black_pieces, white_pieces, board = read_gomoku_board(board_file, board)
    draw_gomoku_board(board_size, black_pieces, white_pieces, board, highlight_coord)

    # GAME LOOP
    old = []
    all_lines = []
    turn_is = 'BLACK'
    while (True):
        # UPDATE MOVE
        coords = input(f'\n{turn_is} input move [x y]: ')
        old = all_lines;
        x, y = map(int, coords.split())
        if (is_valid(x,y, board_size) and is_empty(x,y, white_pieces, black_pieces)):
            print("Valid move !")
            white_pieces, black_pieces, board = update_board(x, y, turn_is, white_pieces, black_pieces, board)
            turn_is = toggle_turn(turn_is)
        else:
            print("Invalid move !")

        #DRAW BOARD
        draw_gomoku_board(board_size, black_pieces, white_pieces, board, (x,y))
        
        all_lines = scan('@',board, board_size)
        for line in all_lines:
            print(line)
        save_list('old', old)
        save_list('new', all_lines)




if __name__ == "__main__":
    main()
