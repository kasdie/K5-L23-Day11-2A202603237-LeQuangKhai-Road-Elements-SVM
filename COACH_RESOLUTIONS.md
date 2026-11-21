# Ghi nhận xử lý với coach — Lê Quang Khải, 2A202603237

**Trạng thái cập nhật:** học viên xác nhận trong trao đổi ngày 21/11/2026 rằng nội dung HOI_COACH.md đã được coach thông qua và đã sửa/rà lại. Ghi nhận này dựa trên xác nhận của học viên; không bổ sung tên coach, chữ ký hay thời điểm buổi xác nhận khi chưa được cung cấp. Lịch sử ghi chú được lưu riêng trên máy học viên.

## 1. Phạm vi

Bài thực hiện trên CVAT local, project d11-road-lequangkhai trên máy học viên, gói day11-data gồm 28 ảnh. Phần làm và export hiện tại gồm 20 ảnh bắt buộc A01–A12, B01–B08; tám ảnh thêm chưa gán hình và không tính điểm thưởng. Không ghi nhận đã chuyển dữ liệu lên CVAT lớp hoặc đã nộp bài.

## 2. Các ca L1/R1 đã trao đổi và rà lại

| Ảnh | Cảnh báo lint hiện tại | Link | Ghi chú tự rà đã có | Trạng thái ghi nhận |
| --- | --- | --- | --- | --- |
| A05 | L1 và R1 | Ảnh thuộc lô core | Đã xem | Đã thông qua coach theo xác nhận của học viên |
| A06 | L1 và R1 | Ảnh thuộc lô core | Đã xem và ổn; phân biệt crosswalk với lane | Đã thông qua coach theo xác nhận của học viên |
| A07 | L1 | Ảnh thuộc lô core | Đã xem và ổn | Đã thông qua coach theo xác nhận của học viên |
| A08 | L1 | Ảnh thuộc lô core | Đã xem và ổn | Đã thông qua coach theo xác nhận của học viên |
| A10 | R1 | Ảnh thuộc lô core | Đã xem, ghi nhận thiếu vạch bên phải R1; giữ cách xử lý đã trao đổi | Đã thông qua coach theo xác nhận của học viên |
| A12 | R1 | Ảnh thuộc lô core | Đã xem và ổn | Đã thông qua coach theo xác nhận của học viên |

Bản export ngày 21/11 vẫn có tám cảnh báo trên. Không thay đổi số lint trong manifest và không tạo vạch tưởng tượng để xóa cảnh báo. Phần giải trình được đưa vào mục 3 của báo cáo. Đây không phải kết quả QC chéo của Chi và không tự tạo quyết định Release.

## 3. Camera rear và vùng lái

- B03: L1/R1 quy chiếu trái/phải theo hướng xe đang chạy, không theo góc nhìn của camera.
- B06: đã xem lại ranh giới drivable ở dải phân cách/cọc; dùng cách xử lý đã trao đổi với coach.
- Ảnh thêm: bản hiện tại không làm phần thưởng; không đánh dấu task extra có nhãn hình học chỉ vì đã có tag.

## 4. Hồ sơ QC và phần theo dõi

Đã ghép QC với Hoàng Kim Chi. Khải đã cung cấp ảnh phiếu và xác nhận đã kiểm qua: sáu ảnh A01, A08, A10, B01, B03, B06; 71 nhãn; bốn lỗi chính; Rework cho lô Chi revision 2. Phiếu đã được chép lại trong bộ nộp; chờ Chi sửa và kiểm lại. Khải đã gửi ảnh; nhận xét chung ban đầu đã được thay bằng bốn góp ý hình học A01 L2, A10 L2, B03 L1 và crosswalk B06 mà Khải xác nhận Chi cũng đồng ý. Các phép đo là từ lần rà của AI, không phải số đo được gán cho Chi. Phạm vi/số liệu chính thức Chi kiểm lô Khải và số liệu so sánh row-anchor vẫn chưa được cung cấp. Không điền số lỗi hoặc quyết định thay người kiểm.
