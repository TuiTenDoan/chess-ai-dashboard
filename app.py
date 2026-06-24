from flask import Flask, render_template, request, jsonify
import chess
import math
import random
import os

app = Flask(__name__)

DEFAULT_DEPTH = 3

PIECE_VALUES = {
    chess.PAWN: 100,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 20000,
}


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/new", methods=["POST"])
def new_game():
    board = chess.Board()
    return jsonify(make_response(board, message="Ván mới đã bắt đầu. Bạn cầm quân Trắng."))


@app.route("/api/move", methods=["POST"])
def player_move():
    data = request.get_json()

    fen = data.get("fen")
    move_uci = data.get("move")
    depth = int(data.get("depth", DEFAULT_DEPTH))

    board = chess.Board(fen)

    if board.is_game_over():
        return jsonify(make_response(board, message="Ván cờ đã kết thúc."))

    if board.turn != chess.WHITE:
        return jsonify(make_response(board, message="Chưa tới lượt của bạn.")), 400

    move = parse_move(board, move_uci)

    if move is None or move not in board.legal_moves:
        return jsonify(make_response(board, message="Nước đi không hợp lệ.")), 400

    player_san = board.san(move)
    board.push(move)

    if board.is_game_over():
        return jsonify(make_response(
            board,
            message="Bạn vừa đi: " + player_san,
            player_move=player_san
        ))

    ai_move = find_best_move(board, depth)

    if ai_move is not None:
        ai_san = board.san(ai_move)
        board.push(ai_move)
    else:
        ai_san = None

    return jsonify(make_response(
        board,
        message="Bạn đi: " + player_san + (" | AI đi: " + ai_san if ai_san else ""),
        player_move=player_san,
        ai_move=ai_san
    ))


def parse_move(board, move_uci):
    try:
        move = chess.Move.from_uci(move_uci)

        if move in board.legal_moves:
            return move

        promotion_move = chess.Move.from_uci(move_uci + "q")
        if promotion_move in board.legal_moves:
            return promotion_move

        return None
    except Exception:
        return None


def find_best_move(board, depth):
    legal_moves = list(board.legal_moves)

    if not legal_moves:
        return None

    ordered_moves = order_moves(board, legal_moves)

    best_move = None
    best_score = math.inf

    alpha = -math.inf
    beta = math.inf

    for move in ordered_moves:
        board.push(move)
        score = alpha_beta(board, depth - 1, alpha, beta)
        board.pop()

        if score < best_score:
            best_score = score
            best_move = move

        beta = min(beta, best_score)

    return best_move


def alpha_beta(board, depth, alpha, beta):
    if depth == 0 or board.is_game_over():
        return evaluate_board(board)

    legal_moves = order_moves(board, list(board.legal_moves))

    if board.turn == chess.WHITE:
        max_eval = -math.inf

        for move in legal_moves:
            board.push(move)
            eval_score = alpha_beta(board, depth - 1, alpha, beta)
            board.pop()

            max_eval = max(max_eval, eval_score)
            alpha = max(alpha, eval_score)

            if beta <= alpha:
                break

        return max_eval

    else:
        min_eval = math.inf

        for move in legal_moves:
            board.push(move)
            eval_score = alpha_beta(board, depth - 1, alpha, beta)
            board.pop()

            min_eval = min(min_eval, eval_score)
            beta = min(beta, eval_score)

            if beta <= alpha:
                break

        return min_eval


def order_moves(board, moves):
    def move_score(move):
        score = 0

        if board.is_capture(move):
            score += 10

        if board.gives_check(move):
            score += 8

        if move.promotion:
            score += 6

        return score

    random.shuffle(moves)
    return sorted(moves, key=move_score, reverse=True)


def evaluate_board(board):
    """
    Điểm dương: Trắng lợi thế.
    Điểm âm: Đen lợi thế.
    AI cầm quân Đen nên sẽ chọn nước đi làm điểm nhỏ nhất.
    """

    if board.is_checkmate():
        if board.turn == chess.WHITE:
            return -999999
        return 999999

    if board.is_stalemate() or board.is_insufficient_material():
        return 0

    score = 0

    for square in chess.SQUARES:
        piece = board.piece_at(square)

        if piece is None:
            continue

        value = PIECE_VALUES[piece.piece_type]

        file_index = chess.square_file(square)
        rank_index = chess.square_rank(square)
        center_bonus = center_control_bonus(file_index, rank_index)

        total_value = value + center_bonus

        if piece.color == chess.WHITE:
            score += total_value
        else:
            score -= total_value

    if board.is_check():
        if board.turn == chess.WHITE:
            score -= 30
        else:
            score += 30

    return score


def center_control_bonus(file_index, rank_index):
    if file_index in [3, 4] and rank_index in [3, 4]:
        return 20

    if file_index in [2, 3, 4, 5] and rank_index in [2, 3, 4, 5]:
        return 10

    return 0


def make_response(board, message="", player_move=None, ai_move=None):
    return {
        "fen": board.fen(),
        "turn": "white" if board.turn == chess.WHITE else "black",
        "status": get_status_text(board),
        "message": message,
        "player_move": player_move,
        "ai_move": ai_move,
        "is_game_over": board.is_game_over(),
        "legal_moves": [move.uci() for move in board.legal_moves],
    }


def get_status_text(board):
    if board.is_checkmate():
        winner = "Đen" if board.turn == chess.WHITE else "Trắng"
        return f"Chiếu hết! {winner} thắng."

    if board.is_stalemate():
        return "Hòa do hết nước đi hợp lệ."

    if board.is_insufficient_material():
        return "Hòa do không đủ quân chiếu hết."

    turn = "Trắng" if board.turn == chess.WHITE else "Đen"

    if board.is_check():
        return f"Lượt {turn} - Đang bị chiếu."

    return f"Lượt {turn}."


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)