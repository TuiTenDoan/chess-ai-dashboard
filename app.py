from flask import Flask, render_template, request, jsonify
import chess
import math
import os

app = Flask(__name__)

# =========================
# CẤU HÌNH AI
# =========================

DEFAULT_DEPTH = 3

# Giới hạn độ sâu tối đa để tránh web bị đơ khi chọn mức quá khó
# Nếu frontend gửi depth = 4 thì backend vẫn tự ép về 3
MAX_DEPTH = 3
MIN_DEPTH = 1

PIECE_VALUES = {
    chess.PAWN: 100,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 20000,
}


# =========================
# ROUTE GIAO DIỆN
# =========================

@app.route("/")
def home():
    return render_template("index.html")


# =========================
# API: TẠO VÁN MỚI
# =========================

@app.route("/api/new", methods=["POST"])
def new_game():
    board = chess.Board()

    return jsonify(
        make_response(
            board,
            message="Ván mới đã bắt đầu. Bạn cầm quân Trắng."
        )
    )


# =========================
# API: NGƯỜI CHƠI ĐI
# =========================

@app.route("/api/move", methods=["POST"])
def player_move():
    data = request.get_json(silent=True)

    if not data:
        board = chess.Board()
        return jsonify(make_response(board, message="Dữ liệu gửi lên không hợp lệ.")), 400

    fen = data.get("fen")
    move_uci = data.get("move")
    depth = get_safe_depth(data.get("depth", DEFAULT_DEPTH))

    if not fen:
        board = chess.Board()
        return jsonify(make_response(board, message="Thiếu trạng thái bàn cờ.")), 400

    if not move_uci:
        board = chess.Board(fen)
        return jsonify(make_response(board, message="Thiếu nước đi.")), 400

    try:
        board = chess.Board(fen)
    except Exception:
        board = chess.Board()
        return jsonify(make_response(board, message="Trạng thái bàn cờ không hợp lệ.")), 400

    if board.is_game_over():
        return jsonify(make_response(board, message="Ván cờ đã kết thúc."))

    # Người chơi chỉ được đi khi tới lượt Trắng
    if board.turn != chess.WHITE:
        return jsonify(make_response(board, message="Chưa tới lượt của bạn.")), 400

    move = parse_move(board, move_uci)

    if move is None or move not in board.legal_moves:
        return jsonify(make_response(board, message="Nước đi không hợp lệ.")), 400

    # Người chơi đi
    player_san = board.san(move)
    board.push(move)

    if board.is_game_over():
        return jsonify(
            make_response(
                board,
                message="Bạn vừa đi: " + player_san,
                player_move=player_san
            )
        )

    # AI đi quân Đen
    ai_move = find_best_move(board, depth)

    if ai_move is not None and ai_move in board.legal_moves:
        ai_san = board.san(ai_move)
        board.push(ai_move)
    else:
        ai_san = None

    return jsonify(
        make_response(
            board,
            message="Bạn đi: " + player_san + (" | AI đi: " + ai_san if ai_san else ""),
            player_move=player_san,
            ai_move=ai_san
        )
    )


# =========================
# HÀM PHỤ TRỢ
# =========================

def get_safe_depth(raw_depth):
    """
    Nhận depth từ frontend và ép trong khoảng an toàn.
    Mục đích: tránh người dùng chọn depth quá cao làm server bị đơ.
    """
    try:
        depth = int(raw_depth)
    except Exception:
        depth = DEFAULT_DEPTH

    if depth < MIN_DEPTH:
        depth = MIN_DEPTH

    if depth > MAX_DEPTH:
        depth = MAX_DEPTH

    return depth


def parse_move(board, move_uci):
    """
    Chuyển nước đi dạng UCI thành chess.Move.
    Ví dụ:
    e2e4
    g1f3

    Nếu tốt phong cấp thì tự động phong Hậu.
    Ví dụ:
    e7e8 -> e7e8q
    """
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


# =========================
# AI: MINIMAX + ALPHA-BETA
# =========================

def find_best_move(board, depth):
    """
    AI cầm quân Đen.
    Điểm dương: Trắng lợi.
    Điểm âm: Đen lợi.

    Vì AI là Đen nên AI chọn nước đi có điểm nhỏ nhất.
    """
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
    """
    Thuật toán Minimax kết hợp Alpha-Beta Pruning.
    """
    if depth <= 0 or board.is_game_over():
        return evaluate_board(board)

    legal_moves = order_moves(board, list(board.legal_moves))

    # Trắng là bên tối đa hóa điểm
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

    # Đen là bên tối thiểu hóa điểm
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
    """
    Sắp xếp nước đi để Alpha-Beta cắt tỉa tốt hơn.
    Bỏ random.shuffle để AI không bị cảm giác đi ngẫu nhiên lung tung.
    """

    def move_score(move):
        score = 0

        # Ưu tiên nước ăn quân
        if board.is_capture(move):
            captured_piece = board.piece_at(move.to_square)
            moving_piece = board.piece_at(move.from_square)

            if captured_piece:
                score += PIECE_VALUES[captured_piece.piece_type]

            if moving_piece:
                score -= PIECE_VALUES[moving_piece.piece_type] // 10

            score += 1000

        # Ưu tiên nước chiếu vua
        if board.gives_check(move):
            score += 500

        # Ưu tiên phong cấp
        if move.promotion:
            score += 800

        return score

    return sorted(moves, key=move_score, reverse=True)


# =========================
# HEURISTIC: ĐÁNH GIÁ BÀN CỜ
# =========================

def evaluate_board(board):
    """
    Heuristic đánh giá bàn cờ.

    Điểm dương: Trắng lợi thế.
    Điểm âm: Đen lợi thế.
    AI cầm quân Đen nên sẽ chọn nước đi làm điểm nhỏ nhất.
    """

    # Nếu chiếu hết
    if board.is_checkmate():
        # Nếu tới lượt Trắng mà Trắng bị chiếu hết => Đen thắng
        if board.turn == chess.WHITE:
            return -999999

        # Nếu tới lượt Đen mà Đen bị chiếu hết => Trắng thắng
        return 999999

    # Nếu hòa
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

    # Đánh giá trạng thái chiếu
    if board.is_check():
        if board.turn == chess.WHITE:
            # Trắng đang bị chiếu => tốt cho Đen
            score -= 30
        else:
            # Đen đang bị chiếu => tốt cho Trắng
            score += 30

    return score


def center_control_bonus(file_index, rank_index):
    """
    Cộng điểm nếu quân đứng gần trung tâm.
    """
    # 4 ô trung tâm chính
    if file_index in [3, 4] and rank_index in [3, 4]:
        return 20

    # Vùng trung tâm mở rộng
    if file_index in [2, 3, 4, 5] and rank_index in [2, 3, 4, 5]:
        return 10

    return 0


# =========================
# RESPONSE
# =========================

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


# =========================
# CHẠY APP
# =========================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)