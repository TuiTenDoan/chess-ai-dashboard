# Chess AI Dashboard

## Link Trải Nghiệm Game

[Chess AI Dashboard Web App](https://chess-ai-dashboard.onrender.com)

---

## Thông Tin Sinh Viên

* Họ và tên: Nguyễn Tâm Đoan
* Mã số sinh viên: 247060005
* Trường: TDU
* Lớp: CNTT19A
* Giảng viên hướng dẫn: Bùi Xuân Tùng

---

## Tên Đề Tài

Xây dựng website game cờ vua tích hợp trí tuệ nhân tạo sử dụng thuật toán Minimax và Alpha-Beta Pruning.

---

## Công Nghệ Sử Dụng

### Backend

* Python
* Flask
* python-chess
* Gunicorn

### Frontend

* HTML
* CSS
* JavaScript

### Hosting và quản lý mã nguồn

* GitHub
* Render

---

## Chức Năng Chính

* Hiển thị bàn cờ vua 8x8.
* Người chơi điều khiển quân Trắng.
* AI điều khiển quân Đen.
* Kiểm tra nước đi hợp lệ theo luật cờ vua.
* AI tự tính toán nước đi bằng thuật toán Minimax.
* Tối ưu thuật toán bằng Alpha-Beta Pruning.
* Hiển thị trạng thái ván đấu.
* Hiển thị lịch sử nước đi.
* Cho phép chọn độ sâu tìm kiếm của AI.

---

## Cấu Trúc Thư Mục

```text
CoVua/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── render.yaml
│
├── templates/
│   └── index.html
│
└── static/
    ├── style.css
    └── script.js
```

---

## Hướng Dẫn Chạy Local

### Bước 1: Clone source code

```bash
git clone LINK_REPOSITORY_GITHUB
cd chess-ai-dashboard
```

Hoặc mở trực tiếp terminal trong thư mục project nếu đã có sẵn source code.

---

### Bước 2: Tạo môi trường ảo

Trên Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\activate
```

---

### Bước 3: Cài đặt thư viện

```bash
pip install -r requirements.txt
```

---

### Bước 4: Chạy chương trình

```bash
python app.py
```

Sau đó mở trình duyệt và truy cập:

```text
http://127.0.0.1:5000
```

---

## File `requirements.txt`

```txt
flask
python-chess
gunicorn
```

---

## File `render.yaml`

```yaml
services:
  - type: web
    name: chess-ai-dashboard
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn app:app
```

---

# Lý Thuyết Thuật Toán

## 1. Minimax

Minimax là thuật toán tìm kiếm thường dùng trong các trò chơi đối kháng hai người.

Trong cờ vua, mỗi người chơi luôn cố gắng chọn nước đi có lợi nhất cho mình. Thuật toán Minimax giả định rằng cả hai bên đều chơi tối ưu.

Trong project này:

* Người chơi cầm quân Trắng.
* AI cầm quân Đen.
* Điểm dương thể hiện Trắng đang có lợi.
* Điểm âm thể hiện Đen đang có lợi.
* AI cầm quân Đen nên sẽ chọn nước đi làm điểm số nhỏ nhất.

Ví dụ:

```text
+500  => Trắng đang lợi thế.
-500  => Đen đang lợi thế.
0     => Hai bên cân bằng.
```

---

## 2. Alpha-Beta Pruning

Alpha-Beta Pruning là kỹ thuật tối ưu cho Minimax.

Mục đích của Alpha-Beta Pruning là giảm số lượng trạng thái bàn cờ cần duyệt. Khi thuật toán phát hiện một nhánh không thể tạo ra kết quả tốt hơn kết quả hiện có, nhánh đó sẽ bị bỏ qua.

Hai biến chính:

* `alpha`: giá trị tốt nhất hiện tại của bên tối đa hóa.
* `beta`: giá trị tốt nhất hiện tại của bên tối thiểu hóa.

Điều kiện cắt tỉa:

```text
Nếu beta <= alpha thì dừng duyệt nhánh hiện tại.
```

Nhờ đó, AI có thể tính toán nhanh hơn so với Minimax thông thường.

---

# Lý Thuyết Các Hàm Trong Backend `app.py`

## 1. Hàm `home()`

```python
@app.route("/")
def home():
    return render_template("index.html")
```

Hàm `home()` dùng để hiển thị giao diện chính của website.

Khi người dùng truy cập đường dẫn `/`, Flask sẽ gọi hàm này và trả về file `index.html` trong thư mục `templates`.

Vai trò chính:

* Load giao diện web.
* Hiển thị bàn cờ.
* Hiển thị các khu vực thông tin như trạng thái, lịch sử nước đi và nút điều khiển.

---

## 2. Hàm `new_game()`

```python
@app.route("/api/new", methods=["POST"])
def new_game():
    board = chess.Board()
    return jsonify(make_response(board, message="Ván mới đã bắt đầu. Bạn cầm quân Trắng."))
```

Hàm `new_game()` dùng để tạo một ván cờ mới.

Khi người chơi bấm nút "Ván mới", frontend sẽ gửi request đến API `/api/new`. Backend tạo bàn cờ mới bằng:

```python
chess.Board()
```

`chess.Board()` là trạng thái mặc định của bàn cờ vua, gồm đầy đủ quân Trắng và Đen ở vị trí ban đầu.

Vai trò chính:

* Khởi tạo bàn cờ mới.
* Đặt lại trạng thái ván đấu.
* Trả dữ liệu bàn cờ về frontend dưới dạng JSON.

---

## 3. Hàm `player_move()`

```python
@app.route("/api/move", methods=["POST"])
def player_move():
```

Hàm `player_move()` xử lý nước đi của người chơi và nước đi phản hồi của AI.

Quy trình chính:

1. Nhận dữ liệu từ frontend gồm:

   * Trạng thái bàn cờ hiện tại.
   * Nước đi của người chơi.
   * Độ sâu tìm kiếm của AI.

2. Tạo lại bàn cờ từ FEN:

```python
board = chess.Board(fen)
```

3. Kiểm tra ván cờ đã kết thúc chưa.

4. Kiểm tra có đúng lượt của quân Trắng không.

5. Chuyển nước đi người chơi sang dạng hợp lệ bằng hàm `parse_move()`.

6. Nếu nước đi hợp lệ, cập nhật bàn cờ:

```python
board.push(move)
```

7. Gọi AI tìm nước đi tốt nhất:

```python
ai_move = find_best_move(board, depth)
```

8. Cập nhật nước đi của AI.

9. Trả trạng thái mới của bàn cờ về frontend.

Đây là hàm trung tâm của hệ thống vì nó kết nối giữa giao diện người dùng, luật cờ vua và thuật toán AI.

---

## 4. Hàm `parse_move(board, move_uci)`

```python
def parse_move(board, move_uci):
```

Hàm `parse_move()` dùng để chuyển nước đi dạng chuỗi thành đối tượng nước đi của thư viện `python-chess`.

Ví dụ nước đi dạng UCI:

```text
e2e4
g1f3
a7a8
```

Trong đó:

* `e2e4`: quân đi từ ô e2 đến e4.
* `g1f3`: quân đi từ ô g1 đến f3.
* `a7a8`: quân đi từ ô a7 đến a8.

Nếu nước đi là nước phong cấp của Tốt, hệ thống tự động phong Hậu bằng cách thêm chữ `q`.

Ví dụ:

```text
a7a8q
```

Ý nghĩa là Tốt đi từ a7 đến a8 và phong thành Hậu.

Vai trò chính:

* Chuyển chuỗi nước đi thành `chess.Move`.
* Kiểm tra nước đi có nằm trong danh sách nước đi hợp lệ không.
* Xử lý trường hợp phong cấp.

---

## 5. Hàm `find_best_move(board, depth)`

```python
def find_best_move(board, depth):
```

Hàm `find_best_move()` dùng để tìm nước đi tốt nhất cho AI.

Trong project này, AI cầm quân Đen. Theo quy ước của hàm đánh giá:

* Điểm dương là tốt cho Trắng.
* Điểm âm là tốt cho Đen.

Vì AI là quân Đen nên AI sẽ chọn nước đi có điểm thấp nhất.

Quy trình chính:

1. Lấy tất cả nước đi hợp lệ:

```python
legal_moves = list(board.legal_moves)
```

2. Sắp xếp nước đi bằng `order_moves()`.

3. Duyệt từng nước đi.

4. Giả lập nước đi bằng:

```python
board.push(move)
```

5. Gọi hàm `alpha_beta()` để tính điểm.

6. Hoàn tác nước đi bằng:

```python
board.pop()
```

7. Chọn nước đi có điểm nhỏ nhất.

Vai trò chính:

* Là hàm quyết định nước đi của AI.
* Gọi thuật toán Alpha-Beta để đánh giá từng lựa chọn.
* Trả về nước đi tốt nhất cho quân Đen.

---

## 6. Hàm `alpha_beta(board, depth, alpha, beta)`

```python
def alpha_beta(board, depth, alpha, beta):
```

Hàm `alpha_beta()` triển khai thuật toán Minimax kết hợp Alpha-Beta Pruning.

Tham số:

* `board`: trạng thái bàn cờ hiện tại.
* `depth`: độ sâu tìm kiếm còn lại.
* `alpha`: giá trị tốt nhất của bên tối đa hóa.
* `beta`: giá trị tốt nhất của bên tối thiểu hóa.

Cách hoạt động:

### Trường hợp dừng

Nếu `depth == 0` hoặc ván cờ đã kết thúc, hàm gọi:

```python
evaluate_board(board)
```

để trả về điểm đánh giá bàn cờ.

### Nếu đến lượt Trắng

Trắng là bên tối đa hóa điểm số. Vì vậy thuật toán sẽ chọn giá trị lớn nhất.

```python
max_eval = max(max_eval, eval_score)
alpha = max(alpha, eval_score)
```

### Nếu đến lượt Đen

Đen là bên tối thiểu hóa điểm số. Vì vậy thuật toán sẽ chọn giá trị nhỏ nhất.

```python
min_eval = min(min_eval, eval_score)
beta = min(beta, eval_score)
```

### Cắt tỉa

Nếu:

```text
beta <= alpha
```

thì nhánh hiện tại sẽ bị bỏ qua vì không còn ảnh hưởng đến kết quả tối ưu.

Vai trò chính:

* Tính toán các khả năng đi tiếp theo.
* Mô phỏng tư duy đối kháng giữa Trắng và Đen.
* Tối ưu tìm kiếm bằng cách cắt bỏ nhánh không cần thiết.

---

## 7. Hàm `order_moves(board, moves)`

```python
def order_moves(board, moves):
```

Hàm `order_moves()` dùng để sắp xếp danh sách nước đi trước khi đưa vào thuật toán Alpha-Beta.

Về mặt lý thuyết, thứ tự duyệt nước đi không làm thay đổi kết quả cuối cùng của Minimax. Tuy nhiên, nếu các nước đi tốt được xét trước, Alpha-Beta có thể cắt tỉa nhiều nhánh hơn.

Trong project này, các nước đi được ưu tiên:

* Nước ăn quân.
* Nước chiếu vua.
* Nước phong cấp.

Các nước đi này thường có ảnh hưởng lớn đến thế cờ nên được xét trước.

Vai trò chính:

* Tăng hiệu quả cắt tỉa của Alpha-Beta.
* Giúp AI tính toán nhanh hơn.
* Ưu tiên các nước đi quan trọng.

---

# Lý Thuyết Hàm Đánh Giá Bàn Cờ

## 1. Hàm `evaluate_board(board)`

```python
def evaluate_board(board):
```

Hàm `evaluate_board()` dùng để chấm điểm một trạng thái bàn cờ.

Trong cờ vua, không thể duyệt toàn bộ mọi nước đi đến hết ván trong thời gian ngắn. Vì vậy, AI cần một hàm đánh giá để ước lượng bên nào đang có lợi tại một thời điểm nhất định.

Quy ước điểm:

```text
Điểm dương  => Trắng có lợi.
Điểm âm    => Đen có lợi.
Điểm 0     => Hai bên cân bằng.
```

Vì AI cầm quân Đen nên AI sẽ cố gắng chọn nước đi làm điểm số nhỏ nhất.

---

## 2. Kiểm Tra Chiếu Hết

Trong hàm đánh giá có đoạn:

```python
if board.is_checkmate():
    if board.turn == chess.WHITE:
        return -999999
    return 999999
```

Ý nghĩa:

* Nếu đang là lượt Trắng và Trắng bị chiếu hết, Đen thắng.
* Vì AI cầm Đen nên đây là trạng thái rất tốt cho AI.
* Hàm trả về `-999999`.

Ngược lại:

* Nếu đang là lượt Đen và Đen bị chiếu hết, Trắng thắng.
* Đây là trạng thái xấu cho AI.
* Hàm trả về `999999`.

Giá trị rất lớn được dùng để AI ưu tiên trạng thái thắng và tránh trạng thái thua.

---

## 3. Kiểm Tra Hòa

```python
if board.is_stalemate() or board.is_insufficient_material():
    return 0
```

Ý nghĩa:

* `board.is_stalemate()`: hòa do bên đến lượt không còn nước đi hợp lệ nhưng không bị chiếu.
* `board.is_insufficient_material()`: hòa do không đủ quân để chiếu hết.

Khi ván cờ hòa, hàm trả về `0` vì không bên nào có lợi thế rõ ràng.

---

## 4. Giá Trị Quân Cờ

```python
PIECE_VALUES = {
    chess.PAWN: 100,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 20000,
}
```

Bảng giá trị quân cờ dùng để đánh giá sức mạnh vật chất trên bàn cờ.

Ý nghĩa từng quân:

* Tốt: 100 điểm.
* Mã: 320 điểm.
* Tượng: 330 điểm.
* Xe: 500 điểm.
* Hậu: 900 điểm.
* Vua: 20000 điểm.

Khi duyệt bàn cờ:

* Quân Trắng được cộng điểm.
* Quân Đen bị trừ điểm.

Ví dụ:

```text
Trắng hơn một Hậu  => điểm tăng khoảng +900.
Đen hơn một Hậu    => điểm giảm khoảng -900.
```

Điều này giúp AI biết bên nào đang hơn quân hoặc kém quân.

---

## 5. Duyệt Từng Ô Trên Bàn Cờ

```python
for square in chess.SQUARES:
    piece = board.piece_at(square)
```

`chess.SQUARES` là danh sách 64 ô trên bàn cờ.

Hàm sẽ duyệt từng ô để kiểm tra xem ô đó có quân cờ hay không.

Nếu ô có quân:

```python
piece = board.piece_at(square)
```

hệ thống sẽ lấy loại quân và màu quân để tính điểm.

Vai trò chính:

* Kiểm tra toàn bộ bàn cờ.
* Tính tổng giá trị quân Trắng.
* Tính tổng giá trị quân Đen.
* Tạo ra điểm đánh giá tổng thể.

---

## 6. Điểm Kiểm Soát Trung Tâm

Trong cờ vua, trung tâm bàn cờ rất quan trọng. Các quân ở trung tâm thường kiểm soát nhiều ô hơn và có khả năng di chuyển linh hoạt hơn.

Vì vậy hàm đánh giá cộng thêm điểm thưởng cho quân đứng gần trung tâm:

```python
center_bonus = center_control_bonus(file_index, rank_index)
```

Nếu quân đứng ở trung tâm chính, được cộng nhiều điểm hơn. Nếu quân đứng ở vùng trung tâm mở rộng, được cộng ít điểm hơn.

Điều này giúp AI có xu hướng phát triển quân ra các vị trí tích cực.

---

## 7. Hàm `center_control_bonus(file_index, rank_index)`

```python
def center_control_bonus(file_index, rank_index):
```

Hàm này tính điểm thưởng vị trí dựa trên vị trí của quân cờ.

Tham số:

* `file_index`: chỉ số cột, từ 0 đến 7.
* `rank_index`: chỉ số hàng, từ 0 đến 7.

Quy tắc:

```python
if file_index in [3, 4] and rank_index in [3, 4]:
    return 20
```

Nếu quân đứng ở 4 ô trung tâm chính thì cộng 20 điểm.

```python
if file_index in [2, 3, 4, 5] and rank_index in [2, 3, 4, 5]:
    return 10
```

Nếu quân đứng ở vùng trung tâm mở rộng thì cộng 10 điểm.

Nếu quân ở ngoài vùng trung tâm:

```python
return 0
```

Vai trò chính:

* Khuyến khích AI kiểm soát trung tâm.
* Giúp nước đi của AI hợp lý hơn.
* Bổ sung yếu tố vị trí thay vì chỉ tính giá trị quân cờ.

---

## 8. Đánh Giá Trạng Thái Chiếu

```python
if board.is_check():
    if board.turn == chess.WHITE:
        score -= 30
    else:
        score += 30
```

Nếu `board.is_check()` là `True`, nghĩa là bên đến lượt đang bị chiếu.

Trường hợp 1:

* Đang là lượt Trắng.
* Trắng bị chiếu.
* Điều này có lợi cho Đen.
* Điểm bị giảm `-30`.

Trường hợp 2:

* Đang là lượt Đen.
* Đen bị chiếu.
* Điều này có lợi cho Trắng.
* Điểm được cộng `+30`.

Vai trò chính:

* Giúp AI nhận biết trạng thái gây áp lực lên Vua.
* Khuyến khích AI tạo ra các nước chiếu.
* Giúp AI hạn chế đi vào thế bị chiếu nguy hiểm.

---

## 9. Tổng Kết Hàm Đánh Giá

Hàm `evaluate_board()` đánh giá bàn cờ dựa trên các yếu tố chính:

* Trạng thái chiếu hết.
* Trạng thái hòa.
* Tổng giá trị quân cờ.
* Vị trí quân cờ so với trung tâm.
* Trạng thái chiếu Vua.

Công thức tổng quát có thể hiểu như sau:

```text
Điểm bàn cờ =
Tổng giá trị quân Trắng
- Tổng giá trị quân Đen
+ Điểm vị trí
+ Điểm trạng thái chiếu
```

Kết quả cuối cùng được dùng bởi thuật toán Minimax và Alpha-Beta để chọn nước đi phù hợp cho AI.

---

# Lý Thuyết Các Hàm Trong Frontend `script.js`

## 1. Hàm `newGame()`

```javascript
async function newGame()
```

Hàm `newGame()` gửi request đến API `/api/new` để tạo ván cờ mới.

Vai trò chính:

* Gọi backend tạo bàn cờ mới.
* Nhận FEN mới từ server.
* Reset quân đang chọn.
* Reset lịch sử nước đi.
* Render lại bàn cờ.

---

## 2. Hàm `sendMove(move)`

```javascript
async function sendMove(move)
```

Hàm `sendMove()` gửi nước đi của người chơi lên backend.

Tham số `move` là nước đi dạng UCI, ví dụ:

```text
e2e4
g1f3
```

Vai trò chính:

* Gửi FEN hiện tại.
* Gửi nước đi của người chơi.
* Gửi độ sâu tìm kiếm của AI.
* Nhận nước đi phản hồi từ AI.
* Cập nhật bàn cờ và lịch sử nước đi.

---

## 3. Hàm `updateUI(data)`

```javascript
function updateUI(data)
```

Hàm `updateUI()` cập nhật giao diện sau mỗi lần backend trả dữ liệu.

Vai trò chính:

* Cập nhật trạng thái ván đấu.
* Cập nhật thông báo hệ thống.
* Gọi `renderHistory()` để cập nhật lịch sử.
* Gọi `renderBoard()` để vẽ lại bàn cờ.

---

## 4. Hàm `renderHistory()`

```javascript
function renderHistory()
```

Hàm `renderHistory()` hiển thị lịch sử nước đi của người chơi và AI.

Vai trò chính:

* Nếu chưa có nước đi, hiển thị thông báo "Chưa có nước đi".
* Nếu có nước đi, hiển thị danh sách nước đi theo thứ tự.
* Tự động cuộn xuống dòng mới nhất.

---

## 5. Hàm `renderBoard()`

```javascript
function renderBoard()
```

Hàm `renderBoard()` vẽ lại bàn cờ trên giao diện.

Quy trình chính:

1. Xóa bàn cờ cũ.
2. Đọc trạng thái bàn cờ từ FEN.
3. Tạo 64 ô cờ.
4. Gán màu sáng/tối cho từng ô.
5. Hiển thị quân cờ bằng ký tự Unicode.
6. Highlight quân đang chọn.
7. Highlight các nước đi hợp lệ.
8. Gắn sự kiện click cho từng ô.

Đây là hàm quan trọng nhất ở frontend vì nó chịu trách nhiệm hiển thị trạng thái bàn cờ.

---

## 6. Hàm `handleSquareClick(squareName, boardData)`

```javascript
function handleSquareClick(squareName, boardData)
```

Hàm này xử lý khi người dùng click vào một ô trên bàn cờ.

Quy trình chính:

* Nếu chưa chọn quân, kiểm tra ô đó có quân Trắng không.
* Nếu có quân Trắng, lưu ô đó vào `selectedSquare`.
* Nếu đã chọn quân, click lần hai sẽ tạo nước đi.
* Nếu nước đi hợp lệ, gọi `sendMove()`.
* Nếu nước đi không hợp lệ, hiển thị thông báo lỗi.

Vai trò chính:

* Xử lý tương tác chọn quân.
* Xử lý tương tác di chuyển quân.
* Kết nối hành động click của người dùng với backend.

---

## 7. Hàm `isLegalMove(move)`

```javascript
function isLegalMove(move)
```

Hàm `isLegalMove()` kiểm tra nước đi người chơi chọn có nằm trong danh sách nước đi hợp lệ hay không.

Danh sách nước đi hợp lệ được backend gửi về thông qua `legal_moves`.

Vai trò chính:

* Ngăn người chơi đi sai luật.
* Chỉ cho phép gửi nước đi hợp lệ lên server.
* Hỗ trợ xử lý trường hợp phong cấp.

---

## 8. Hàm `getLegalTargetsFromSelected()`

```javascript
function getLegalTargetsFromSelected()
```

Hàm này lấy danh sách các ô mà quân đang chọn có thể đi đến.

Ví dụ nếu chọn quân ở ô `e2`, hàm sẽ tìm các nước bắt đầu bằng `e2`, như:

```text
e2e3
e2e4
```

Sau đó lấy ra ô đích:

```text
e3
e4
```

Vai trò chính:

* Hiển thị gợi ý nước đi hợp lệ.
* Highlight các ô có thể đi.
* Giúp người dùng dễ tương tác với bàn cờ.

---

## 9. Hàm `isWhitePiece(piece)`

```javascript
function isWhitePiece(piece)
```

Hàm này kiểm tra quân cờ có phải quân Trắng hay không.

Trong FEN:

* Quân Trắng được ký hiệu bằng chữ in hoa.
* Quân Đen được ký hiệu bằng chữ thường.

Ví dụ:

```text
P, N, B, R, Q, K  => quân Trắng
p, n, b, r, q, k  => quân Đen
```

Vai trò chính:

* Chỉ cho phép người chơi chọn quân Trắng.
* Ngăn người chơi điều khiển quân Đen của AI.

---

## 10. Hàm `parseFen(fen)`

```javascript
function parseFen(fen)
```

Hàm `parseFen()` chuyển chuỗi FEN thành dữ liệu bàn cờ để frontend có thể render.

FEN là định dạng mô tả trạng thái bàn cờ. Ví dụ:

```text
rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR
```

Trong đó:

* Chữ cái biểu thị quân cờ.
* Số biểu thị số ô trống liên tiếp.
* Dấu `/` phân tách các hàng.

Vai trò chính:

* Đọc trạng thái bàn cờ từ backend.
* Biến FEN thành object JavaScript.
* Giúp `renderBoard()` biết ô nào có quân nào.

---

## 11. Hàm `fileRankToSquare(file, rank)`

```javascript
function fileRankToSquare(file, rank)
```

Hàm này chuyển chỉ số cột và hàng thành tên ô cờ.

Ví dụ:

```text
file = 0, rank = 1  => a1
file = 4, rank = 2  => e2
file = 7, rank = 8  => h8
```

Vai trò chính:

* Hỗ trợ render bàn cờ.
* Tạo tên ô theo chuẩn cờ vua.
* Giúp JavaScript xử lý nước đi dạng UCI.

---

# Hướng Dẫn Cập Nhật Lên GitHub

Sau khi sửa file `README.md`, chạy:

```bash
git add README.md
git commit -m "Update README theory sections"
git push
```

---

# Link Website

Website đã được deploy tại:

```text
https://chess-ai-dashboard.onrender.com
```
