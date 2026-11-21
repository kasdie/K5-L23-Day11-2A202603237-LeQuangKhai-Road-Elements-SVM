# Bộ bàn giao Day11 — Lê Quang Khải

Học viên: **Lê Quang Khải — 2A202603237**. Bạn QC: Hoàng Kim Chi.

Repo nộp link LMS: [kasdie/K5-L23-Day11-2A202603237-LeQuangKhai-Road-Elements-SVM](https://github.com/kasdie/K5-L23-Day11-2A202603237-LeQuangKhai-Road-Elements-SVM).

**Trạng thái: đã hoàn thiện năm file bàn giao cá nhân; sẵn sàng nộp link LMS.** Chi đã đồng ý Release cho lô Khải sau sửa theo xác nhận của học viên; ảnh minh chứng đã được học viên gửi riêng. Rework trong phiếu Khải kiểm Chi chỉ dành cho lô Chi revision 2. Điểm do coach chấm; trợ lý chưa thực hiện nộp LMS.

## Các file bàn giao

| File | Nội dung / trạng thái |
| --- | --- |
| [lequangkhai-front.zip](lms_submission/lequangkhai-front.zip) | Nhãn 12 ảnh core front, sau sửa; không kèm ảnh |
| [lequangkhai-fisheye.zip](lms_submission/lequangkhai-fisheye.zip) | Nhãn 8 ảnh core fisheye, sau sửa; không kèm ảnh |
| [lequangkhai-manifest.json](lms_submission/lequangkhai-manifest.json) | Revision 1, checksum và lint của hai ZIP hiện tại |
| [lequangkhai-qc1-for-hoangkimchi.md](lms_submission/lequangkhai-qc1-for-hoangkimchi.md) | Đã bổ sung từ ảnh phiếu học viên cung cấp: 6 ảnh, 71 nhãn, 4 lỗi chính (5,63%), Rework cho lô Chi revision 2 |
| [lequangkhai-report.md](lms_submission/lequangkhai-report.md) | Báo cáo đã cập nhật số lượng, bốn chỉnh sửa, xác nhận Chi đồng ý Release và tự đánh giá; ảnh minh chứng đã gửi riêng |

## Phần đã hoàn thiện

- Hai job core front/fisheye đã completed; 20 ảnh, 129 hình và 80 tag trong bộ export. Tám ảnh thêm chưa làm hình, không tính điểm thưởng.
- Đã sửa lane L2 ở A01/A10, lane L1 và biên drivable liên quan ở B03, polygon crosswalk ở B06.
- Kiểm cục bộ sau sửa: điểm sơn đối chiếu A01/A10 cách đường 0 px, B03 khoảng 3 px; điểm trên dải phân cách B06 không còn nằm trong crosswalk. Đây không phải phép chấm sai số toàn ảnh so với GT.
- Source của nhãn là manual; báo cáo vẫn ghi AI hỗ trợ tạo nhãn ban đầu.
- Hai ZIP chỉ chứa annotations.xml. Manifest giữ tám cảnh báo QC1-02 và phần giải trình coach; không sửa số cảnh báo để làm kết quả đẹp hơn.

Chi tiết trạng thái và giới hạn kiểm tra: [LAB_STATUS.json](LAB_STATUS.json). Nội dung coach đã thông qua theo xác nhận của học viên: [COACH_RESOLUTIONS.md](COACH_RESOLUTIONS.md).

## Xác nhận hoàn tất và theo dõi riêng

1. Phiếu Khải kiểm Chi đã có đủ 12 mã và kết luận Rework cho revision 2. Chi sửa và gửi bản mới để Khải kiểm lại là theo dõi lô Chi; không phải phần còn thiếu trong năm file của Khải. Giới hạn đối chiếu bảng phân công và hash file Chi vẫn ghi rõ trong phiếu.
2. Mục 4 báo cáo đã có bảng tổng hợp bốn góp ý và phần đã sửa. Theo xác nhận của học viên, Chi đã kiểm toàn bộ 20 ảnh core; số nhãn đếm từ hai ZIP là 209. Chi đã xác nhận đồng ý Release sau sửa theo lời học viên cung cấp; row-anchor là tùy chọn.
3. Ảnh minh chứng: **đã được học viên tự gửi riêng**, theo xác nhận trong trao đổi; bản đầy đủ tiếp tục lưu tại máy, GitHub không nhúng ảnh dataset. Đây không còn là phần chờ gửi.

## Phạm vi dữ liệu trên GitHub

Theo [ATTRIBUTION.md](ATTRIBUTION.md), gói ảnh lớp không được phân phối lại và không đưa ảnh WoodScape vào repo. Báo cáo GitHub chỉ giữ mô tả ảnh; không nhúng pixel dataset. Ảnh gốc, GT, phiên đăng nhập, file môi trường và lịch sử làm việc local không thuộc bộ bàn giao.

## Kiểm tra và cập nhật

- Kiểm công cụ: `PYTHONPATH=src python -m road_lab.road_check selftest`; chạy test bằng `python -m pytest -q` trong môi trường có pytest.
- Kiểm bộ nộp: `.venv/bin/python scripts/check_delivery.py --directory lms_submission --name lequangkhai --peer hoangkimchi`. Phiếu đã điền và qua kiểm cấu trúc; công cụ vẫn giữ tám cảnh báo QC1-02 của lô Khải có giải trình coach. Công cụ không xác minh lại chất lượng lô Chi từ ảnh phiếu.
- Khi Chi gửi bản đã sửa hoặc bổ sung phiếu Chi kiểm lô Khải, cập nhật file tương ứng và báo cáo. Khi tạo lại bản GitHub từ bộ đầy đủ local, dùng `scripts/prepare_lms_repo.py --out <thư-mục-mới>` để loại ảnh nhúng, rồi lưu bản cũ trước khi thay bộ hiện tại.

Bước tiếp theo của học viên: nộp link repo ở trên vào LMS và giữ bản đầy đủ có ảnh để coach đối chiếu khi cần.
