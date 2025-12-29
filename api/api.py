from flask import Flask, request, jsonify, render_template
import random
import numpy as np
import copy

app = Flask(__name__)

ROWS = 3
COLS = 3

board = ["", "", "", "", "", "", "", "", ""]
curr_player = "X"
history = {"X": [], "O": []}

def check_winner(state):
    wins = [
        (0,1,2), (3,4,5), (6,7,8),
        (0,3,6), (1,4,7), (2,5,8),
        (0,4,8), (2,4,6)
    ]
    for a, b, c in wins:
        if state[a] and state[a] == state[b] == state[c]:
            return state[a]
    return None

@app.route('/api/state')
def get_state():
    return jsonify({
        "board": board,
        "currPlayer": curr_player,
        "winner": check_winner(board)
    })


@app.route('/api/move', methods=["POST"])
def make_move():
    global curr_player
    data = request.json
    index = data.get("index")
    if board[index] != "":
        return jsonify({"error": "Invalid move"}), 400

    board[index] = curr_player
    history[curr_player].append(index)
    winner = check_winner(board)
    if not winner:
        curr_player = "O" if curr_player == "X" else "X"
        if len(history[curr_player]) > 3:
            oldest = history[curr_player].pop(0)
            board[oldest] = ""
    return jsonify({
        "board": board,
        "currPlayer": curr_player,
        "winner": winner
    })

def has_diagonal_fork(board, opp):
    """
    check if opponent has a diagonal or antidiagonal fork trap setup
    :param board: board state
    :param opp: opponent
    :return: whether it has a diagonal/antidiagonal fork set up or not
    """
    if (board[0] == opp and board[8] == opp) or (board[2] == opp and board[6] == opp):
        return True
    return False

def positional_eval(board_state, player):
    """
    :param board_state: negamax board state
    :param player: current player
    :return: score that is used as tiebreaker. prioritizes centre control
    """
    score = 0
    opp = "O" if player == "X" else "X"
    if board_state[4] == player:
        score += 3

    if has_diagonal_fork(board_state, opp):
        for i in [0, 2, 6, 8]:
            if board_state[i] == player:
                score += 1   # get middles next if possible
        for i in [1, 3, 5, 7]:
            if board_state[i] == player:
                score += 2
    else:
        for i in [0, 2, 6, 8]:
            if board_state[i] == player:
                score += 2   # get corners next if possible
        for i in [1, 3, 5, 7]:
            if board_state[i] == player:
                score += 1
    return score

def simulate_move(board, history, player, move):
    board = board.copy()
    history = {p: history[p].copy() for p in history}
    board[move] = player
    history[player].append(move)
    removed = None
    winner = check_winner(board)
    if len(history[player]) > 3 and not winner:   # or == 3  DANGER EDIT
        removed = history[player].pop(0)
        board[removed] = ""
    return board, history, removed

def opp_can_win(board, history, opp):
    for i in range(9):
        if board[i] == "":
            b, h, _ = simulate_move(board, history, opp, i)
            if check_winner(b) == opp:
                return True
    return False

def negamax_recursive(board, history, player):
    opp = "O" if player == "X" else "X"
    winning_moves = []
    safe_moves = []
    losing_moves = []

    for i in range(9):
        if board[i] != "":
            continue

        board_copy, history_copy, _ = simulate_move(board, history, player, i)
        if check_winner(board_copy) == player:
            winning_moves.append(i)
            continue
        if opp_can_win(board_copy, history_copy, opp):
            losing_moves.append(i)
        else:
            safe_moves.append(i)

    print("winning moves")
    for j in range(len(winning_moves)):
        print(f"move: {winning_moves[j]}")
    for j in range(len(safe_moves)):
        print(f"move: {safe_moves[j]}")
    for j in range(len(losing_moves)):
        print(f"move: {losing_moves[j]}")

    if winning_moves:
        return winning_moves[0]
    if safe_moves:
        return max(safe_moves, key=lambda m:
                   positional_eval(
                       simulate_move(board, history, player, m)[0],
                       player
                   ))
    return max(losing_moves, key=lambda m:
               positional_eval(
                   simulate_move(board, history, player, m)[0],
                   player
               ))
    if history[opp] > 2:
        opp_oldest_move = history[opp].pop(0)
    if history[player] > 2:
        player_oldest_move = history[player].pop(0)



@app.route('/api/negamax', methods=["POST"])
def negamax(depth=5):
    global board, history, curr_player

    best_move = negamax_recursive(board, history, curr_player)
    opp = "O" if curr_player == "X" else "X"

    if best_move is not None:
        board[best_move] = curr_player
        history[curr_player].append(best_move)

        if len(history[opp]) > 3:
            oldest = history[opp].pop(0)
            board[oldest] = ""

        winner = check_winner(board)
        if not winner:
            curr_player = opp

        return jsonify({
            "board": board,
            "currPlayer": curr_player,
            "winner": winner
        })

    return jsonify({"error": "No valid move"}), 400



@app.route('/api/reset', methods=["POST"])
def reset():
    global board, curr_player, history
    board = [""] * 9
    curr_player = "X"
    history = {"X": [], "O": []}
    return jsonify({"status": "reset"})

if __name__ == "__main__":
    app.run(debug=True)