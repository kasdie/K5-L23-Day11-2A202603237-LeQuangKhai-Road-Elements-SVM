# Bộ bàn giao Day11 — Lê Quang Khải

Học viên: **Lê Quang Khải — 2A202603237**. Bạn QC: Hoàng Kim Chi.

Repo nộp link LMS: [kasdie/K5-L23-Day11-2A202603237-LeQuangKhai-Road-Elements-SVM](https://github.com/kasdie/K5-L23-Day11-2A202603237-LeQuangKhai-Road-Elements-SVM).

**Trạng thái: đã hoàn thiện phần annotation và báo cáo có thể làm độc lập; phiếu Khải kiểm lô Chi sẽ bổ sung khi học viên cung cấp.** Đây là bàn giao từng phần theo yêu cầu, chưa phải kết luận Release hoặc điểm đạt toàn bộ rubric.

## Các file bàn giao

| File | Nội dung / trạng thái |
| --- | --- |
| [lequangkhai-front.zip](lms_submission/lequangkhai-front.zip) | Nhãn 12 ảnh core front, sau sửa; không kèm ảnh |
| [lequangkhai-fisheye.zip](lms_submission/lequangkhai-fisheye.zip) | Nhãn 8 ảnh core fisheye, sau sửa; không kèm ảnh |
| [lequangkhai-manifest.json](lms_submission/lequangkhai-manifest.json) | Revision 1, checksum và lint của hai ZIP hiện tại |
| [lequangkhai-qc1-for-hoangkimchi.md](lms_submission/lequangkhai-qc1-for-hoangkimchi.md) | **Đang chờ** dữ liệu/kết quả Khải kiểm lô Chi; không có số lỗi giả định |
| [lequangkhai-report.md](lms_submission/lequangkhai-report.md) | Báo cáo đã cập nhật số lượng, bốn chỉnh sửa, tự đánh giá và các phần còn chờ; ảnh minh chứng lưu riêng |

## Phần đã hoàn thiện

- Hai job core front/fisheye đã completed; 20 ảnh, 129 hình và 80 tag trong bộ export. Tám ảnh thêm chưa làm hình, không tính điểm thưởng.
- Đã sửa lane L2 ở A01/A10, lane L1 và biên drivable liên quan ở B03, polygon crosswalk ở B06.
- Kiểm cục bộ sau sửa: điểm sơn đối chiếu A01/A10 cách đường 0 px, B03 khoảng 3 px; điểm trên dải phân cách B06 không còn nằm trong crosswalk. Đây không phải phép chấm sai số toàn ảnh so với GT.
- Source của nhãn là manual; báo cáo vẫn ghi AI hỗ trợ tạo nhãn ban đầu.
- Hai ZIP chỉ chứa annotations.xml. Manifest giữ tám cảnh báo QC1-02 và phần giải trình coach; không sửa số cảnh báo để làm kết quả đẹp hơn.

Chi tiết trạng thái và giới hạn kiểm tra: [LAB_STATUS.json](LAB_STATUS.json). Nội dung coach đã thông qua theo xác nhận của học viên: [COACH_RESOLUTIONS.md](COACH_RESOLUTIONS.md).

## Phần còn chờ bổ sung

1. Phiếu Khải kiểm lô Chi theo sáu ảnh được phân công, đủ 12 mã và số nhãn thực sự đã kiểm. Chi đồng ý góp ý về lô Khải không thay cho phiếu này.
2. Số liệu/phạm vi QC của bạn học và so sánh row-anchor với Chi nếu làm hoạt động tùy chọn.
3. Minh chứng ảnh chụp được cung cấp qua kênh riêng được lớp cho phép; bản đầy đủ có ảnh đang lưu tại máy học viên, không tự gửi qua LMS trong phiên này.

## Phạm vi dữ liệu trên GitHub

Theo [ATTRIBUTION.md](ATTRIBUTION.md), gói ảnh lớp không được phân phối lại và không đưa ảnh WoodScape vào repo. Báo cáo GitHub chỉ giữ mô tả ảnh; không nhúng pixel dataset. Ảnh gốc, GT, phiên đăng nhập, file môi trường và lịch sử làm việc local không thuộc bộ bàn giao.

## Kiểm tra và cập nhật

- Kiểm công cụ: `PYTHONPATH=src python -m road_lab.road_check selftest`; chạy test bằng `python -m pytest -q` trong môi trường có pytest.
- Kiểm bộ nộp: `.venv/bin/python scripts/check_delivery.py --directory lms_submission --name lequangkhai --peer hoangkimchi`. Công cụ hiện vẫn báo phiếu Chi còn chờ và các cảnh báo QC1-02; đây là trạng thái thực tế, không phải lỗi được che đi để cho phép bàn giao từng phần.
- Sau khi có dữ liệu QC, cập nhật file tương ứng và báo cáo. Khi tạo lại bản GitHub từ bộ đầy đủ local, dùng `scripts/prepare_lms_repo.py --out <thư-mục-mới>` để loại ảnh nhúng, rồi lưu bản cũ trước khi thay bộ hiện tại.
