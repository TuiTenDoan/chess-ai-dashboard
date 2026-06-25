# Chess AI Dashboard

## Tên Đề Tài

**Xây dựng website game cờ vua tích hợp trí tuệ nhân tạo sử dụng thuật toán Minimax và Alpha-Beta Pruning**

---

## Giới Thiệu Đề Tài

Cờ vua là một trò chơi trí tuệ có tính chiến thuật cao, trong đó người chơi cần tính toán nhiều nước đi tiếp theo để đưa ra lựa chọn tối ưu. Với sự phát triển của trí tuệ nhân tạo, việc xây dựng một hệ thống AI có khả năng chơi cờ là một bài toán phù hợp để tìm hiểu các thuật toán tìm kiếm, đánh giá trạng thái và ra quyết định.

Đề tài **Chess AI Dashboard** được xây dựng nhằm tạo ra một website chơi cờ vua đơn giản, trong đó người chơi điều khiển quân Trắng và AI điều khiển quân Đen. Hệ thống cho phép người dùng thực hiện nước đi trực tiếp trên bàn cờ, sau đó AI sẽ tính toán và phản hồi bằng một nước đi phù hợp.

Trong đề tài này, AI được xây dựng dựa trên thuật toán **Minimax**, kết hợp với kỹ thuật tối ưu **Alpha-Beta Pruning** và **Heuristic**. Đây là ba thành phần chính giúp hệ thống có thể phân tích trạng thái ván cờ và lựa chọn nước đi hợp lý.

---

## Mục Tiêu Đề Tài

Mục tiêu của đề tài là xây dựng một website game cờ vua có tích hợp trí tuệ nhân tạo, cho phép người dùng trải nghiệm chơi cờ với máy tính.

Các mục tiêu cụ thể gồm:

* Xây dựng giao diện bàn cờ vua trên nền tảng web.
* Cho phép người chơi thực hiện nước đi hợp lệ theo luật cờ vua.
* Xây dựng AI có khả năng tự động chọn nước đi.
* Áp dụng thuật toán Minimax để mô phỏng quá trình ra quyết định.
* Tối ưu tốc độ tìm kiếm bằng Alpha-Beta Pruning.
* Xây dựng Heuristic để AI xác định bên nào đang có lợi thế.
* Triển khai website để người dùng có thể truy cập và trải nghiệm trực tuyến.

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

Website có các chức năng chính sau:

* Hiển thị bàn cờ vua 8x8.
* Người chơi điều khiển quân Trắng.
* AI điều khiển quân Đen.
* Kiểm tra nước đi hợp lệ theo luật cờ vua.
* AI tự động tính toán và đưa ra nước đi phản hồi.
* Cho phép người dùng chọn độ sâu tìm kiếm của AI.
* Hiển thị trạng thái hiện tại của ván đấu.
* Hiển thị lịch sử các nước đi.
* Cho phép bắt đầu ván cờ mới.
* Có thể triển khai và sử dụng trực tiếp trên nền tảng web.

---

## Hướng Dẫn Chạy Dự Án Trên Máy Cá Nhân

### Bước 1: Clone source code

```bash
git clone LINK_REPOSITORY_GITHUB
cd chess-ai-dashboard
```

Nếu đã có sẵn source code trên máy, có thể mở terminal trực tiếp trong thư mục project.

### Bước 2: Tạo môi trường ảo

Trên Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\activate
```

### Bước 3: Cài đặt thư viện

```bash
pip install -r requirements.txt
```

### Bước 4: Chạy chương trình

```bash
python app.py
```

Sau đó mở trình duyệt và truy cập:

```text
http://127.0.0.1:5000
```

---

## Các File Cấu Hình Quan Trọng

### File `requirements.txt`

File này khai báo các thư viện cần thiết để chạy dự án.

```txt
flask
python-chess
gunicorn
```

Trong đó:

* `flask`: dùng để xây dựng web server.
* `python-chess`: dùng để xử lý luật cờ vua, trạng thái bàn cờ và nước đi hợp lệ.
* `gunicorn`: dùng để chạy ứng dụng khi deploy lên Render.

### File `render.yaml`

File này dùng để cấu hình triển khai ứng dụng lên nền tảng Render.

```yaml
services:
  - type: web
    name: chess-ai-dashboard
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn app:app
```

---

# Cơ Sở Lý Thuyết Của Hệ Thống AI

Trong dự án này, AI chơi cờ được xây dựng dựa trên ba thành phần chính:

* Thuật toán Minimax.
* Thuật toán Alpha-Beta Pruning.
* Heuristic.

Ba thành phần này kết hợp với nhau để giúp AI phân tích các nước đi có thể xảy ra, đánh giá lợi thế của từng trạng thái bàn cờ và chọn ra nước đi phù hợp nhất.

---

## Thuật Toán Minimax

Minimax là thuật toán thường được sử dụng trong các trò chơi đối kháng hai người như cờ vua, cờ caro hoặc cờ tướng. Trong các trò chơi này, mỗi người chơi đều cố gắng chọn nước đi có lợi nhất cho mình, đồng thời làm giảm lợi thế của đối thủ.

Trong đề tài này:

* Người chơi điều khiển quân Trắng.
* AI điều khiển quân Đen.
* Hai bên thay phiên nhau thực hiện nước đi.
* AI giả định rằng người chơi cũng sẽ chọn nước đi tốt nhất.

Thuật toán Minimax hoạt động bằng cách mô phỏng các nước đi có thể xảy ra trong tương lai. Ở mỗi lượt, thuật toán sẽ đánh giá xem trạng thái bàn cờ sau nước đi đó có lợi cho bên nào.

Quy ước điểm trong chương trình:

```text
Điểm dương  => Trắng đang có lợi.
Điểm âm    => Đen đang có lợi.
Điểm 0     => Hai bên cân bằng.
```

Vì AI điều khiển quân Đen, nên AI sẽ chọn nước đi làm cho điểm số nhỏ nhất. Điều này có nghĩa là AI luôn cố gắng đưa bàn cờ về trạng thái có lợi cho quân Đen.

Ví dụ:

```text
+500  => Trắng đang có lợi thế.
-500  => Đen đang có lợi thế.
0     => Hai bên cân bằng.
```

Nếu một nước đi làm điểm số giảm xuống thấp hơn, AI sẽ đánh giá đó là nước đi tốt hơn cho quân Đen.

Có thể hiểu đơn giản rằng Minimax giúp AI trả lời câu hỏi:

```text
Nếu mình đi nước này, đối thủ sẽ phản ứng thế nào?
Sau vài lượt tiếp theo, trạng thái đó có lợi cho mình hay không?
```

Nhờ vậy, AI không chỉ chọn nước đi theo hiện tại mà còn có khả năng tính toán một số bước tiếp theo.

---

## Thuật Toán Alpha-Beta Pruning

Minimax có nhược điểm là phải duyệt qua rất nhiều trạng thái bàn cờ. Trong cờ vua, số lượng nước đi hợp lệ ở mỗi lượt có thể rất lớn. Nếu AI duyệt toàn bộ các khả năng, chương trình sẽ chạy chậm, đặc biệt khi tăng độ sâu tìm kiếm.

Để khắc phục vấn đề này, đề tài sử dụng kỹ thuật **Alpha-Beta Pruning**.

Alpha-Beta Pruning là phương pháp tối ưu cho Minimax. Mục đích của kỹ thuật này là loại bỏ những nhánh không cần thiết trong quá trình tìm kiếm.

Hai giá trị chính trong Alpha-Beta Pruning là:

* `alpha`: giá trị tốt nhất hiện tại của bên tối đa hóa.
* `beta`: giá trị tốt nhất hiện tại của bên tối thiểu hóa.

Trong quá trình duyệt các nước đi, nếu thuật toán phát hiện một nhánh chắc chắn không thể tạo ra kết quả tốt hơn kết quả đã có, nhánh đó sẽ bị bỏ qua.

Điều kiện cắt tỉa là:

```text
Nếu beta <= alpha thì dừng duyệt nhánh hiện tại.
```

Việc cắt tỉa này không làm thay đổi kết quả cuối cùng của thuật toán Minimax. Nó chỉ giúp giảm số lượng trạng thái cần kiểm tra, từ đó làm cho AI tính toán nhanh hơn.

Trong dự án, Alpha-Beta Pruning giúp AI:

* Giảm số lượng nước đi cần duyệt.
* Tăng tốc độ phản hồi của AI.
* Cho phép tìm kiếm sâu hơn trong cùng một khoảng thời gian.
* Giúp trải nghiệm chơi game mượt mà hơn.

Có thể hiểu đơn giản:

```text
Minimax giúp AI chọn nước đi tốt.
Alpha-Beta Pruning giúp AI chọn nước đi tốt nhanh hơn.
```

---

## Heuristic

Trong thực tế, AI không thể tính toán toàn bộ ván cờ từ đầu đến cuối vì số lượng khả năng là rất lớn. Do đó, tại một độ sâu nhất định, AI cần một phương pháp để đánh giá trạng thái bàn cờ hiện tại.

Phương pháp đó được gọi là **Heuristic**.

Heuristic có nhiệm vụ chấm điểm một thế cờ để xác định bên nào đang có lợi.

Trong đề tài này, Heuristic dựa trên các yếu tố chính sau:

* Trạng thái chiếu hết.
* Trạng thái hòa.
* Giá trị quân cờ trên bàn.
* Vị trí quân cờ so với trung tâm.
* Trạng thái chiếu vua.

### Giá trị quân cờ

Mỗi loại quân cờ được gán một giá trị tương ứng với sức mạnh của nó:

```text
Tốt    = 100 điểm
Mã     = 320 điểm
Tượng  = 330 điểm
Xe     = 500 điểm
Hậu    = 900 điểm
Vua    = 20000 điểm
```

Khi đánh giá bàn cờ:

* Quân Trắng được cộng điểm.
* Quân Đen bị trừ điểm.

Ví dụ:

```text
Trắng hơn một Hậu  => điểm tăng khoảng +900.
Đen hơn một Hậu    => điểm giảm khoảng -900.
```

Vì AI điều khiển quân Đen, nên AI sẽ ưu tiên những trạng thái có điểm số thấp.

### Kiểm soát trung tâm

Trong cờ vua, các ô trung tâm có vai trò rất quan trọng. Quân cờ đứng ở trung tâm thường kiểm soát được nhiều ô hơn và có khả năng di chuyển linh hoạt hơn.

Vì vậy, Heuristic cộng thêm điểm cho các quân đứng gần trung tâm bàn cờ.

Điều này giúp AI không chỉ quan tâm đến việc ăn quân, mà còn biết phát triển quân đến những vị trí tốt hơn.

### Trạng thái chiếu và chiếu hết

Nếu một bên bị chiếu, trạng thái đó sẽ được đánh giá là bất lợi cho bên bị chiếu.

Nếu một bên bị chiếu hết, Heuristic sẽ trả về điểm rất lớn hoặc rất nhỏ để AI ưu tiên trạng thái thắng và tránh trạng thái thua.

Cụ thể:

* Nếu Trắng bị chiếu hết, Đen thắng, đây là trạng thái rất tốt cho AI.
* Nếu Đen bị chiếu hết, AI thua, đây là trạng thái rất xấu cần tránh.

### Tổng kết Heuristic

Có thể hiểu công thức tổng quát như sau:

```text
Điểm bàn cờ =
Giá trị quân Trắng
- Giá trị quân Đen
+ Điểm vị trí
+ Điểm trạng thái chiếu
```

Heuristic là thành phần rất quan trọng vì nó quyết định cách AI nhìn nhận một thế cờ. Nếu Heuristic tốt, AI sẽ có xu hướng chọn những nước đi hợp lý hơn.

---

# Nguyên Lý Hoạt Động Của Hệ Thống

Quy trình hoạt động của hệ thống có thể mô tả như sau:

* Người dùng truy cập website.
* Website hiển thị bàn cờ vua ban đầu.
* Người chơi chọn quân Trắng và thực hiện nước đi.
* Frontend gửi nước đi của người chơi lên backend.
* Backend kiểm tra nước đi có hợp lệ hay không.
* Nếu hợp lệ, backend cập nhật trạng thái bàn cờ.
* AI sử dụng Minimax kết hợp Alpha-Beta Pruning để tìm nước đi tốt nhất.
* Heuristic được dùng để chấm điểm các trạng thái có thể xảy ra.
* AI chọn nước đi phù hợp và cập nhật bàn cờ.
* Backend gửi trạng thái mới về frontend.
* Frontend cập nhật lại giao diện và lịch sử nước đi.

Quy trình trên được lặp lại cho đến khi ván cờ kết thúc.

---

# Vai Trò Của Backend Và Frontend

## Backend

Backend được xây dựng bằng Flask và Python. Nhiệm vụ chính của backend là xử lý logic của ván cờ và thuật toán AI.

Backend đảm nhiệm các công việc:

* Khởi tạo ván cờ mới.
* Nhận nước đi từ người chơi.
* Kiểm tra nước đi hợp lệ.
* Cập nhật trạng thái bàn cờ.
* Gọi thuật toán AI để tìm nước đi.
* Trả dữ liệu bàn cờ về frontend.

Có thể hiểu backend là phần xử lý “bộ não” của hệ thống.

## Frontend

Frontend được xây dựng bằng HTML, CSS và JavaScript. Nhiệm vụ chính của frontend là hiển thị giao diện và xử lý thao tác của người dùng.

Frontend đảm nhiệm các công việc:

* Hiển thị bàn cờ.
* Cho phép người dùng chọn quân và di chuyển quân.
* Gửi nước đi của người chơi lên backend.
* Nhận kết quả từ backend.
* Cập nhật trạng thái ván đấu.
* Hiển thị lịch sử nước đi.

Có thể hiểu frontend là phần giao diện giúp người dùng tương tác với hệ thống.

---

# Link Trải Nghiệm Game

Website đã được deploy tại:

```text
https://chess-ai-dashboard.onrender.com
```

Hoặc truy cập:

[Chess AI Dashboard Web App](https://chess-ai-dashboard.onrender.com)

---

# Thông Tin Sinh Viên

* Họ và tên: Nguyễn Tâm Đoan
* Mã số sinh viên: 247060005
* Trường: TDU
* Lớp: CNTT19A
* Giảng viên hướng dẫn: Bùi Xuân Tùng
