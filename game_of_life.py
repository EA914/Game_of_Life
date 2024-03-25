import numpy as np
from flask import Flask, render_template, jsonify

app = Flask(__name__)

def update_board(board):
    new_board = np.zeros(board.shape)
    for i in range(board.shape[0]):
        for j in range(board.shape[1]):
            neighbors = np.sum(board[max(0, i-1):min(board.shape[0], i+2), max(0, j-1):min(board.shape[1], j+2)]) - board[i, j]
            if board[i, j] == 1 and (neighbors < 2 or neighbors > 3):
                new_board[i, j] = 0
            elif board[i, j] == 0 and neighbors == 3:
                new_board[i, j] = 1
            else:
                new_board[i, j] = board[i, j]
    return new_board

def generate_initial_board(size):
    return np.zeros((size, size))

board_size = 50
initial_state = np.array([
    [0, 1, 0, 0, 0],
    [0, 0, 1, 0, 0],
    [1, 1, 1, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0]
])

board = np.zeros((board_size, board_size))
board[:initial_state.shape[0], :initial_state.shape[1]] = initial_state

@app.route('/')
def index():
    return render_template('index.html', initial_state=board.tolist())

@app.route('/get_board')
def get_board():
    global board
    board = update_board(board)
    serialized_board = board.tolist()
    return jsonify(serialized_board)

if __name__ == "__main__":
    app.run(port=8000)
