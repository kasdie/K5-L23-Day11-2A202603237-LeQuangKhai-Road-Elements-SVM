# Phiếu QC 1 — Road v1.0

**Trạng thái:** Lê Quang Khải xác nhận đã kiểm qua nội dung phiếu trong trao đổi. Bản này chép lại từ ảnh phiếu do học viên cung cấp, thay cho bản dự thảo; không bổ sung chữ ký hoặc kết quả kiểm độc lập của công cụ.

Lô được kiểm (học viên): **Hoàng Kim Chi — 2A202603172**.  
Người kiểm (học viên): **Lê Quang Khải — 2A202603237**.  
Ngày đối chiếu bản file ghi trên phiếu: **21/11/2026**. Phiên bản guideline: **Road v1.0**.  
File được kiểm: **hoangkimchi-front.zip, hoangkimchi-fisheye.zip; manifest revision 2**.  
Số ảnh kiểm trực quan: **6**, không kiểm ảnh thêm. Số nhãn trong mẫu: **47 shape + 24 tag = 71 nhãn**.

Tôi kiểm **A01, A08, A10, B01, B03, B06** trên cùng bộ ảnh gốc. Tôi kiểm định dạng hai ZIP trên toàn bộ ảnh chứa trong file; phần nhận xét trực quan và mẫu số tỷ lệ lỗi chỉ dùng sáu ảnh trên. Tôi không dùng bài của người khác làm GT.

## Tổng hợp theo mã

| Mã | Loại lỗi | Số mục kiểm | Số lỗi xác định | Mức |
| --- | --- | ---: | ---: | --- |
| QC1-01 tag camera | sai thuộc tính / bỏ sót | 6 | 0 | nặng |
| QC1-02 đủ L1/R1 | bỏ sót | 6 | 0 | nặng |
| QC1-03 position | sai thuộc tính / thừa | 11 | 0 | nặng |
| QC1-04 tâm vạch, chiều, điểm dừng | sai phạm vi / bỏ sót | 11 | 0 | chính |
| QC1-05 vạch đứt, che | sai phạm vi / sai thuộc tính | 3 | 0 | chính |
| QC1-06 style, color, kind | sai thuộc tính | 11 | 0 | chính |
| QC1-07 vùng lái | sai phạm vi / bỏ sót / thừa | 11 | 2 | chính |
| QC1-08 đèn, màu | bỏ sót / sai phạm vi / sai thuộc tính | 13 | 0 | nặng / chính |
| QC1-09 facing, type, group, biển phụ | sai thuộc tính | 22 | 0 | chính |
| QC1-10 hình in, đủ biển | bỏ sót / sai phạm vi | 9 | 0 | chính |
| QC1-11 fisheye | sai phạm vi / sai thuộc tính | 7 | 2 | chính |
| QC1-12 file | lỗi file | 71 | 0 | nhẹ / nặng |

Số mục kiểm là đơn vị theo từng tiêu chí: camera tính theo ảnh; L1/R1 tính theo vị trí; các mục hình học/thuộc tính tính theo đối tượng. Một nhãn có thể được kiểm ở nhiều mã nhưng chỉ được tính một lần trong mẫu số 71 nhãn. Mã QC1-12 gồm kiểm mở file, schema và nhãn trong mẫu; ngoài ra hai ZIP được kiểm không kèm ảnh. Số 0 chỉ có nghĩa chưa phát hiện lỗi xác định trong phạm vi kiểm, không chứng nhận toàn lô hoàn hảo hoặc sai số ≤5 px.

## Danh sách lỗi

| # | Mã | Ảnh | Nhãn (label, tham chiếu) | Mức | Mô tả và hướng sửa |
| --- | --- | --- | --- | --- | --- |
| 1 | QC1-07 | A10 | drivable #3 direct, đầu (449.01,606.51) | chính | Biên polygon lõm theo đuôi SUV phía trước, loại phần đường bị xe che. Sửa theo vùng đi được nếu đường trống; không khoét/dừng theo xe khác. |
| 2 | QC1-07 | B03 | drivable #2 direct, đầu (258.23,647.04) | chính | Vùng direct khoét quanh xe phía trước. Nối vùng qua phần bị che theo ranh làn hợp lý, giữ loại thân xe mình ở đáy ảnh. |
| 3 | QC1-11 | B01 | crosswalk #1, đầu (755.58,379.47) | chính | Biên bên trái tràn sang phần hè/đảo gạch ngoài vùng các dải sơn trắng. Thu polygon về vùng crosswalk, theo cung trên ảnh fisheye. |
| 4 | QC1-11 | B06 | crosswalk #0, đầu (229.29,308.7) | chính | Polygon hiện chỉ bao phần gần/bên trái của cụm vạch; còn các dải trắng ở phía xa và phía phải ngoài biên. Rà bao đầy đủ vùng vạch cần gán, loại dải phân cách vàng và thân xe; thống nhất với coach nếu cần tách cụm. |

Tham chiếu `#n` là thứ tự shape trong annotations.xml do trình đọc repo đánh từ 0; không phải ID server CVAT. Tôi kèm tọa độ đầu/hộp để người sửa tìm đúng đối tượng. Các lỗi ở các hàng là những đối tượng khác nhau, không đếm lặp một lỗi dưới hai mã.

## Ca mơ hồ

| Ảnh | Câu hỏi cho lead | Lời đáp hiện có |
| --- | --- | --- |
| Các ảnh được giao | Đủ nhóm nhãn theo bảng phân công từng ảnh chưa? | Chưa có bảng phân công coach để đối chiếu phạm vi đầy đủ. |
| Hình học | Sai số tối đa so GT và trạng thái che khuất có đúng hoàn toàn không? | Chưa có GT; kiểm trực quan không thay phép chấm GT. |

## Quyết định

Lỗi nặng xác định trong mẫu: **0**. Lỗi chính xác định: **4 / 71 nhãn = 5,63%**. Lỗi nhẹ xác định: **0**. Ca chưa chốt phạm vi/ngoại lệ: **1**.

**Quyết định: Rework.**

Lý do: tỷ lệ lỗi chính xác định trong mẫu lớn hơn 5%, đã đủ điều kiện trả sửa theo luật lớp. Các ca chờ lead ghi riêng; không dùng Hold thay cho Rework khi đã vượt ngưỡng. Tôi chưa cho điểm số vì không có GT/rubric chấm đầy đủ.

## File và dấu vân tay

Thông tin dưới đây chép từ phiếu học viên cung cấp; chưa đối chiếu độc lập lại bằng hai ZIP của Chi trong phiên cập nhật này.

- `hoangkimchi-front.zip` — 9641 byte; SHA-256 `d061141e51243d46253a62d395cde62b52557c7cc8dabdc434fd042289129a53`.
- `hoangkimchi-fisheye.zip` — 4066 byte; chuỗi dấu vân tay đọc từ ảnh: `dd0a3d1f02e768cd9e6c4f7aad7ff27afb353f79d6aeb0ef2d1e018d4b4782a`. Chuỗi này có 63 ký tự, chưa đủ độ dài SHA-256 (64 ký tự); cần lấy lại từ file gốc trước khi dùng để đối chiếu checksum. Không tự điền ký tự còn thiếu.

Tôi đề nghị sửa các lỗi đã ghi rồi gửi lại đúng bản export mới để kiểm lại. Tôi giữ bản file này và phiếu này để phân biệt trước/sau sửa.

Tham khảo: [thang mức lỗi](../docs/qc_severity_road_v1.0.md). Kết luận Rework trên đây dành cho **lô của Hoàng Kim Chi revision 2**, không phải kết luận QC cho lô của Lê Quang Khải.
