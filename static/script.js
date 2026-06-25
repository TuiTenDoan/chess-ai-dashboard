let currentFen = "";
let selectedSquare = null;
let legalMoves = [];
let moveHistory = [];

// Khóa bàn cờ khi AI đang tính
let isThinking = false;

// Dùng để chống request cũ ghi đè request mới
let gameVersion = 0;

const pieceMap = {
    "P": { symbol: "♙", color: "white" },
    "N": { symbol: "♘", color: "white" },
    "B": { symbol: "♗", color: "white" },
    "R": { symbol: "♖", color: "white" },
    "Q": { symbol: "♕", color: "white" },
    "K": { symbol: "♔", color: "white" },

    "p": { symbol: "♟", color: "black" },
    "n": { symbol: "♞", color: "black" },
    "b": { symbol: "♝", color: "black" },
    "r": { symbol: "♜", color: "black" },
    "q": { symbol: "♛", color: "black" },
    "k": { symbol: "♚", color: "black" }
};

window.onload = () => {
    newGame();
};

async function newGame() {
    // Tăng phiên ván cờ để bỏ qua response cũ nếu có
    gameVersion++;

    isThinking = false;
    selectedSquare = null;
    moveHistory = [];

    setMessage("Đang tạo ván mới...");

    try {
        const res = await fetch("/api/new", {
            method: "POST",
            headers: { "Content-Type": "application/json" }
        });

        const data = await res.json();

        currentFen = data.fen;
        legalMoves = data.legal_moves;
        selectedSquare = null;
        moveHistory = [];

        updateUI(data);

    } catch (error) {
        console.error(error);
        setMessage("Không thể tạo ván mới. Vui lòng kiểm tra server.");
    }
}

async function sendMove(move) {
    if (isThinking) {
        return;
    }

    isThinking = true;
    selectedSquare = null;

    const thisGameVersion = gameVersion;
    const depth = document.getElementById("depthSelect").value;

    setMessage("AI đang tính toán nước đi...");
    renderBoard();

    try {
        const res = await fetch("/api/move", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                fen: currentFen,
                move: move,
                depth: depth
            })
        });

        const data = await res.json();

        // Nếu trong lúc AI đang tính mà người dùng bấm ván mới,
        // response cũ sẽ bị bỏ qua, không được ghi đè bàn cờ mới.
        if (thisGameVersion !== gameVersion) {
            return;
        }

        if (!res.ok) {
            setMessage(data.message || "Nước đi không hợp lệ.");
            selectedSquare = null;
            return;
        }

        currentFen = data.fen;
        legalMoves = data.legal_moves;
        selectedSquare = null;

        if (data.player_move) {
            moveHistory.push("Người chơi: " + data.player_move);
        }

        if (data.ai_move) {
            moveHistory.push("AI: " + data.ai_move);
        }

        updateUI(data);

    } catch (error) {
        console.error(error);
        setMessage("Lỗi kết nối server. Vui lòng thử lại.");

    } finally {
        if (thisGameVersion === gameVersion) {
            isThinking = false;
            selectedSquare = null;
            renderBoard();
        }
    }
}

function updateUI(data) {
    document.getElementById("statusText").innerText = data.status;
    document.getElementById("messageText").innerText = data.message;

    renderHistory();
    renderBoard();
}

function setMessage(message) {
    const messageText = document.getElementById("messageText");

    if (messageText) {
        messageText.innerText = message;
    }
}

function renderHistory() {
    const box = document.getElementById("moveHistory");

    if (!box) {
        return;
    }

    if (moveHistory.length === 0) {
        box.innerHTML = "<div>Chưa có nước đi.</div>";
        return;
    }

    box.innerHTML = moveHistory
        .map((item, index) => `<div>${index + 1}. ${item}</div>`)
        .join("");

    box.scrollTop = box.scrollHeight;
}

function renderBoard() {
    const boardElement = document.getElementById("chessBoard");

    if (!boardElement) {
        return;
    }

    boardElement.innerHTML = "";

    if (!currentFen) {
        return;
    }

    const boardData = parseFen(currentFen);
    const legalTargets = getLegalTargetsFromSelected();

    for (let rank = 8; rank >= 1; rank--) {
        for (let file = 0; file < 8; file++) {
            const squareName = fileRankToSquare(file, rank);
            const square = document.createElement("div");

            const isLight = (rank + file) % 2 === 0;
            square.className = "square " + (isLight ? "light" : "dark");
            square.dataset.square = squareName;

            if (isThinking) {
                square.classList.add("locked");
            }

            if (selectedSquare === squareName) {
                square.classList.add("selected");
            }

            if (legalTargets.includes(squareName)) {
                const pieceOnTarget = boardData[squareName];

                if (pieceOnTarget) {
                    square.classList.add("capture");
                } else {
                    square.classList.add("legal");
                }
            }

            const piece = boardData[squareName];

            if (piece && pieceMap[piece]) {
                const span = document.createElement("span");
                span.className = "piece " + (pieceMap[piece].color === "white" ? "white-piece" : "black-piece");
                span.innerText = pieceMap[piece].symbol;
                square.appendChild(span);
            }

            square.addEventListener("click", () => handleSquareClick(squareName, boardData));
            boardElement.appendChild(square);
        }
    }
}

function handleSquareClick(squareName, boardData) {
    // Khi AI đang tính thì khóa bàn cờ, không cho click
    if (isThinking) {
        return;
    }

    const clickedPiece = boardData[squareName];

    if (selectedSquare === null) {
        if (clickedPiece && isWhitePiece(clickedPiece)) {
            selectedSquare = squareName;
            renderBoard();
        }
        return;
    }

    if (selectedSquare === squareName) {
        selectedSquare = null;
        renderBoard();
        return;
    }

    if (clickedPiece && isWhitePiece(clickedPiece)) {
        selectedSquare = squareName;
        renderBoard();
        return;
    }

    const move = selectedSquare + squareName;

    if (isLegalMove(move)) {
        sendMove(move);
    } else {
        setMessage("Nước đi không hợp lệ.");
        selectedSquare = null;
        renderBoard();
    }
}

function isLegalMove(move) {
    return legalMoves.some(m => m === move || m.startsWith(move));
}

function getLegalTargetsFromSelected() {
    if (!selectedSquare) {
        return [];
    }

    return legalMoves
        .filter(move => move.startsWith(selectedSquare))
        .map(move => move.substring(2, 4));
}

function isWhitePiece(piece) {
    return piece === piece.toUpperCase();
}

function parseFen(fen) {
    const board = {};
    const boardPart = fen.split(" ")[0];
    const rows = boardPart.split("/");

    for (let rowIndex = 0; rowIndex < 8; rowIndex++) {
        const rank = 8 - rowIndex;
        let file = 0;

        for (const char of rows[rowIndex]) {
            if (!isNaN(char)) {
                file += parseInt(char);
            } else {
                const square = fileRankToSquare(file, rank);
                board[square] = char;
                file++;
            }
        }
    }

    return board;
}

function fileRankToSquare(file, rank) {
    const files = ["a", "b", "c", "d", "e", "f", "g", "h"];
    return files[file] + rank;
}