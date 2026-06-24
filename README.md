# Chess AI Dashboard

## Link Trải Nghiệm Game

Trải nghiệm trực tiếp tại:

[Chess AI Dashboard Web App](https://chess-ai-dashboard.onrender.com)

---

## Giới Thiệu Đồ Án

Chess AI Dashboard là một website mô phỏng trò chơi cờ vua, trong đó người chơi thi đấu với trí tuệ nhân tạo. Người chơi điều khiển quân Trắng, còn hệ thống AI điều khiển quân Đen.

AI trong đồ án được xây dựng dựa trên thuật toán Minimax kết hợp Alpha-Beta Pruning để tính toán và lựa chọn nước đi phù hợp trong quá trình chơi.

---

## Thông Tin Sinh Viên

- Họ và tên: Nguyễn Tâm Đoan
- Mã số sinh viên: 247060005
- Trường: TDU
- Lớp: CNTT19A
- Giảng viên hướng dẫn: Bùi Xuân Tùng

---

## Tên Đề Tài

Xây dựng website game cờ vua tích hợp trí tuệ nhân tạo sử dụng thuật toán Minimax và Alpha-Beta Pruning.

---

## Công Nghệ Sử Dụng

- Python
- Flask
- python-chess
- HTML
- CSS
- JavaScript
- Gunicorn
- Render

---

## Chức Năng Chính

- Hiển thị bàn cờ vua 8x8.
- Người chơi điều khiển quân Trắng.
- AI điều khiển quân Đen.
- Kiểm tra nước đi hợp lệ theo luật cờ vua.
- AI tự tính toán nước đi bằng thuật toán Minimax.
- Tối ưu tìm kiếm bằng Alpha-Beta Pruning.
- Hiển thị trạng thái ván đấu.
- Hiển thị lịch sử nước đi.
- Cho phép chọn độ khó thông qua độ sâu tìm kiếm của AI.

---

## Mô Tả Thuật Toán

### 1. Minimax

Minimax là thuật toán tìm kiếm được sử dụng trong các trò chơi đối kháng hai người. Thuật toán giả định rằng cả hai bên đều chơi tối ưu.

Trong đồ án này:

- Người chơi cầm quân Trắng.
- AI cầm quân Đen.
- Quân Trắng cố gắng tối đa hóa điểm đánh giá bàn cờ.
- Quân Đen cố gắng tối thiểu hóa điểm đánh giá bàn cờ.

### 2. Alpha-Beta Pruning

Alpha-Beta Pruning là kỹ thuật tối ưu cho Minimax. Kỹ thuật này giúp loại bỏ những nhánh tìm kiếm không cần thiết, từ đó giảm số lượng trạng thái bàn cờ cần duyệt.

### 3. Hàm Đánh Giá

Hàm đánh giá bàn cờ dựa trên:

- Giá trị vật chất của quân cờ.
- Khả năng kiểm soát trung tâm.
- Trạng thái chiếu vua.
- Trạng thái chiếu hết hoặc hòa.

---

## Cài Đặt Project

Cài đặt thư viện:

```bash
pip install -r requirements.txt
