import math
import random

def check_valid_move(board, move):
    return move in range(len(board)) and board[move] == -1

def make_move(board, move):
    new_board = board.copy()

    if check_valid_move(board, move):
        new_board[move] = max(board) + 1
    
    return new_board

def mcts_make_move(board, nodes, whoami):
    for i in range(100):
        simulate(board, nodes, whoami)
    
    return make_move(board, select(board, nodes))

def check_game_over(board):
    """
    Return:
    -1 --> Game not over
    0 --> X won
    1 --> O won
    2 --> draw
    """
    for i in range(3):
        if all([board[i + 3*n] > -1 for n in range(3)]) and board[i] % 2 == board[i + 3] % 2 == board[i + 6] % 2:
            return board[i] % 2
        if all([board[3*i + n] > -1 for n in range(3)]) and board[3*i] % 2 == board[3*i + 1] % 2 == board[3*i + 2] % 2:
            return board[3*i] % 2
    
    if all([board[x] > -1 for x in [0,4,8]]) and board[0] % 2 == board[4] % 2 == board[8] % 2:
        return board[0] % 2
    if all([board[x] > -1 for x in [2,4,6]]) and board[2] % 2 == board[4] % 2 == board[6] % 2:
        return board[2] % 2
    
    if all([x > -1 for x in board]):
        return 2
    
    return -1

def print_board(board):
    board_rep = [(x % 2) if x > -1 else 2 for x in board]
    board_str = "{} | {} | {}\n---------\n{} | {} | {}\n---------\n{} | {} | {}".format(*board_rep)
    board_str = board_str.replace("2", " ").replace("0", "X").replace("1", "O")
    print(board_str)

def get_valid_moves(board):
    return [x for x in range(len(board)) if check_valid_move(board, x)]

class Node:
    def __init__(self, parent, board):
        self.total = 0
        self.wins = 0
        self.parent = parent
        self.board_state = board
        self.children = list()
    
    def calc_value(self):
        if self.total == 0:
            return float("inf")
        
        return self.wins/self.total + math.sqrt(2*math.log(self.parent.total)/self.total)

def select(board, nodes):
    return max(get_valid_moves(board), key=lambda x : nodes[tuple(make_move(board, x))].calc_value())

def expand(board, nodes):
    moves = get_valid_moves(board)
    for move in moves:
        made_move = make_move(board, move)
        if tuple(made_move) not in nodes:
            parent = nodes[tuple(board)]
            node = nodes[tuple(made_move)] = Node(parent, made_move)
            parent.children.append(node)

def simulate(board, nodes, whoami):
    turn = whoami # 0 is me 1 is opponent
    curr = board

    while check_game_over(curr) == -1:
        expand(curr, nodes)

        if turn == whoami:
            move = select(curr, nodes)
        else:
            move = random.choice(get_valid_moves(curr))
    
        curr = make_move(curr, move)
        turn = (turn + 1) % 2
    
    backprop(nodes[tuple(curr)], comp_reward(curr, whoami))
    return curr

def comp_reward(board, whoami):
    status = check_game_over(board)
    return 1 if status == whoami else -1 if status == (whoami + 1) % 2 else 0

def backprop(node, reward):
    curr = node
    while curr is not None:
        curr.total += 1
        curr.wins += reward
        curr = curr.parent

if __name__ == '__main__':
    board = [-1]*9
    nodes = {tuple(board): Node(None, board)}

    for i in range(1000):
        print(i, end='\r')
        board = [-1]*9
        turn = 0

        while check_game_over(board) == -1:
            if turn == 0:
                board = mcts_make_move(board, nodes, 0)
            else:
                board = make_move(board, random.choice(get_valid_moves(board)))
            
            turn = (turn + 1) % 2
    
    board = [-1]*9
    turn = 0

    while check_game_over(board) == -1:
        print_board(board)
        if turn == 0:
            board = mcts_make_move(board, nodes, 0)
        else:
            board = make_move(board, int(input("your move: ")))
        
        turn = (turn + 1) % 2