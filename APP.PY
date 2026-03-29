from flask import Flask, render_template, jsonify, request
import random

app = Flask(__name__)

SIZE = 4

def new_board():
    board = [[0]*SIZE for _ in range(SIZE)]
    add_tile(board)
    add_tile(board)
    return board

def add_tile(board):
    empty = [(i,j) for i in range(SIZE) for j in range(SIZE) if board[i][j]==0]
    if empty:
        i,j = random.choice(empty)
        board[i][j] = 2 if random.random()<0.9 else 4

def slide(row):
    row = [x for x in row if x != 0]
    for i in range(len(row)-1):
        if row[i] == row[i+1]:
            row[i] *= 2
            row[i+1] = 0
    row = [x for x in row if x != 0]
    return row + [0]*(SIZE-len(row))

def rotate(board):
    return [list(row) for row in zip(*board[::-1])]

def move(board, direction):
    rotations = {"left":0, "up":1, "right":2, "down":3}
    times = rotations[direction]

    for _ in range(times):
        board = rotate(board)

    board = [slide(row) for row in board]

    for _ in range((4-times)%4):
        board = rotate(board)

    add_tile(board)
    return board

board = new_board()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/state")
def state():
    return jsonify(board)

@app.route("/move", methods=["POST"])
def move_api():
    global board
    direction = request.json.get("direction")
    if direction in ["left","right","up","down"]:
        board = move(board, direction)
    return jsonify(board)

@app.route("/reset")
def reset():
    global board
    board = new_board()
    return jsonify(board)

if __name__ == "__main__":
    app.run(debug=True)