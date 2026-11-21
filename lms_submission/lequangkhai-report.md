> BẢN GITHUB: ảnh minh chứng được lưu riêng; trạng thái QC và giới hạn kiểm tra được ghi trong báo cáo và phiếu QC đi kèm.

# Báo cáo cá nhân — Ngày 11: Road Elements & SVM

**Họ tên:** Lê Quang Khải  
**Mã học viên:** 2A202603237  
**Bạn được ghép QC:** Hoàng Kim Chi  
**Project:** [d11-road-lequangkhai](http://localhost:8080/projects/5)  
**CVAT:** 2.83.0 · **Guideline:** Road v1.0 · **Revision trong manifest:** 1  
**Thời điểm tạo bộ export hiện tại:** 21/11/2026 11:02:54 +0700 (giờ Việt Nam).  
**Số lần nộp lại sau Rework:** 0 đối với lô của tôi; đã sửa bốn vị trí hình học. Phiếu tôi kiểm lô Chi revision 2 đã bổ sung, kết luận Rework cho lô Chi.

Tôi thực hiện 20 ảnh bắt buộc A01–A12 và B01–B08 trên CVAT local. Tôi có sử dụng AI hỗ trợ tạo nhãn ban đầu và công cụ kiểm file, sau đó tự xem lại ảnh, trao đổi các ca khó với coach và rà nhãn trên CVAT. Sau phản hồi ban đầu, tôi ghi nhận bốn góp ý hình học từ lần rà có AI hỗ trợ; tôi đã xác nhận Hoàng Kim Chi cũng đồng ý với các góp ý này. Mục 4 ghi các góp ý cụ thể và kết quả sửa. Tôi đã bổ sung phiếu kiểm lô Chi revision 2 theo nội dung đã kiểm qua và cung cấp trong trao đổi; phần so sánh row-anchor ở mục 8 vẫn chờ dữ liệu.

Trường nguồn `source` của các hình và tag trong CVAT hiện là `manual`, được chuyển theo yêu cầu sau khi rà nhãn. Lần chuyển này chỉ đổi metadata nguồn; tọa độ, thuộc tính và số lượng hình/tag được đối chiếu và giữ nguyên. Phần mô tả AI hỗ trợ tạo nhãn ban đầu vẫn được giữ trong báo cáo.

## 1. Kiểm project

| Mục | Kết quả | Ghi chú |
| --- | --- | --- |
| 6 label, đúng kiểu | Cấu hình khớp Road v1.0 | lane/road_curb: polyline; crosswalk/drivable: polygon; traffic_light/traffic_sign: rectangle |
| Thuộc tính và giá trị | Đối chiếu cấu hình API với taxonomy của repo: khớp | Thuộc tính hiện có được giữ trong bản export và kiểm đọc lại |
| 4 tag ảnh | 20/20 ảnh core có camera, timeofday, weather, source | Camera lấy theo tên ảnh; source=real cho ảnh dataset |
| Task và phạm vi làm | front 12 ảnh; fisheye 8 ảnh | Hai task extra mới có tag, chưa tính là ảnh đã gán và không xin điểm thưởng |
| Tình trạng job tại lúc export | Hai job core đều completed | Đã hoàn tất phần annotation của tôi; phiếu tôi kiểm lô Chi revision 2 đã được bổ sung |

Tôi phân biệt tag với nhãn hình học: tag là thông tin cho toàn ảnh, không tạo đường hay vùng trên ảnh. Trong Objects, lane/curb hiện là Polyline Shape, vùng hiện là Polygon Shape, còn đèn/biển là Rectangle Shape. Để sửa thuộc tính, tôi chọn đối tượng, mở Details và kiểm lại giá trị; không coi giá trị mặc định là đã đúng.

Cách kết thúc polyline theo hướng dẫn CVAT của lab là phím **N** sau khi đặt điểm cuối; vạch được đi từ gần xe ra xa. Cách đặt tag là chọn công cụ Tag, chọn label rồi sửa thuộc tính `value` trong Details. Bộ nhãn ban đầu của bài được đưa vào qua API; việc kiểm thuộc tính và hình ảnh được thực hiện trên giao diện CVAT.

## 2. Số lượng đã gán

Số lượng dưới đây được đếm từ hai ZIP export hiện tại, không lấy từ dự đoán hay điểm tự chấm.

| Task | Ảnh có hình | lane | road_curb | crosswalk | drivable | traffic_light | traffic_sign |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| front | 12 | 21 | 9 | 4 | 14 | 23 | 26 |
| front-extra | 0/4 | 0 | 0 | 0 | 0 | 0 | 0 |
| fisheye | 8 | 2 | 10 | 7 | 5 | 5 | 3 |
| fisheye-extra | 0/4 | 0 | 0 | 0 | 0 | 0 | 0 |

Tổng cộng: **129 hình và 80 tag trên 20 ảnh bắt buộc**. Cả 20 ảnh có đủ bốn tag; không có ảnh core chỉ có tag mà không có hình. Tám ảnh thêm có 32 tag nhưng chưa có hình, được loại khỏi hai ZIP core hiện tại.

## 3. Bảng ca khó và cách xử lý

Tôi đã rà các ca trong HOI_COACH.md và xác nhận với coach cách xử lý. Việc thông qua coach được tôi xác nhận trong trao đổi ngày 21/11/2026; tôi không tự ghi thêm tên coach hay thời điểm buổi xác nhận khi chưa có thông tin đó.

| Ảnh | Nhãn | Phân vân giữa | Đã chọn / cách xử lý | Lý do |
| --- | --- | --- | --- | --- |
| A01 | lane R1, drivable | Kéo vạch xuống đáy ảnh / dừng tại vệt cuối còn thấy | R1 bắt đầu ở (650,665), đi ra xa; chỉnh hai vùng drivable liên quan | Không kéo dài polyline qua phần không còn dấu vết sơn; tránh tạo đích huấn luyện ngoài đoạn nhìn thấy |
| A03 | lane, occluded | Dừng trước vật che / nối qua đoạn che ngắn | Dùng một polyline và bật occluded cho R1 được nối qua đoạn che | Duy trì tính liên tục khi có dấu vết để xác định cùng một vạch |
| A04 | lane, drivable | Vạch vàng đơn / đôi; làn đang đi / làn bên cạnh | Vạch vàng đôi dùng kind=double; phân biệt direct và alternative | Thuộc tính mô tả vạch và chức năng vùng lái, không dựa riêng vào màu hiển thị của label |
| A05 | lane L1/R1 | Thêm làn theo mép đường / giữ phần thực sự thấy | Giữ cách xử lý đã rà và được coach thông qua; export không có L1/R1 | Không biến mép lề thành vạch sơn để xóa cảnh báo lint |
| A06 | lane, crosswalk | Vạch ngang qua đường / vạch phân làn | Gán crosswalk; giữ cách xử lý L1/R1 đã thông qua coach | Crosswalk không phải lane; không tự thêm vạch dọc không có bằng chứng |
| A07 | lane L1 | Vạch bị che / mép dải bê tông | Rà vùng xe trước và giữ cách xử lý đã trao đổi coach | Dải bê tông không tự động được coi là lane; cảnh báo L1 được giải trình |
| A08 | lane L1, traffic_light | Vạch phân làn / vạch tại giao lộ | Rà hình tại giao lộ và màu từng cụm đèn; giữ xử lý L1 đã thông qua | Không dùng vạch ngang thay L1; màu đèn là màu đang sáng |
| A09–A10 | traffic_sign | Nhóm chức năng, mặt biển và biển phụ | Phân nhóm theo chức năng; tách hộp cho tấm biển phụ riêng; dùng other khi chưa phân loại chắc và ghi lý do | Không phân nhóm chỉ từ hình dạng/màu; ảnh nhỏ, mờ có giới hạn nhận biết |
| A10 | lane R1 | Vạch phải bị bỏ sót / không thấy đủ dấu vết | Đã xem và trao đổi coach; giữ cách xử lý hiện tại, export còn cảnh báo R1 | Không suy ra có vạch chỉ vì checker đang yêu cầu R1 |
| A12 | lane R1 | Biên làn / phần đỗ xe sát lề | Đã rà và thông qua coach cách xử lý R1 | Phân biệt làn đang đi với dải đỗ xe, không gán theo giả định |
| B03 | lane position, camera rear | Trái/phải của ảnh / trái/phải theo xe | Quy chiếu L1/R1 theo hướng xe đang chạy, không theo góc nhìn camera | Giữ ý nghĩa vị trí làn khi đổi hướng camera |
| B05–B08 | crosswalk, curb, drivable | Cung cong / đoạn thẳng; mặt đường / thân xe | Dùng nhiều điểm theo hình cong; camera hai bên chỉ dùng position=other nếu có lane thật | Ảnh fisheye không được nắn thẳng để gán; thân xe không thuộc vùng lái |
| B06 | drivable | Mặt đường cùng vùng xe đi / phần sau dải phân cách, cọc | Đã xem lại ranh giới và xử lý theo trao đổi coach | Không mặc định toàn bộ mặt đường nhìn thấy đều thuộc vùng lái của xe |

**Giải trình cảnh báo L1/R1:** bản lint hiện tại còn tám dòng QC1-02: A05 L1/R1, A06 L1/R1, A07 L1, A08 L1, A10 R1, A12 R1. Đây là các ca tôi đã đưa coach và xác nhận cách xử lý, không phải tám lỗi mới do peer-QC tìm ra. Tôi giữ nguyên tám dòng trong manifest, không sửa số đếm để làm đẹp kết quả. Phần xác nhận coach không được dùng thay cho phiếu QC của Chi.

## 4. Phiếu QC 1 nhận được — Hoàng Kim Chi

**Bạn kiểm lô của tôi:** Hoàng Kim Chi.  
**Phạm vi kiểm:** theo xác nhận của tôi, Chi đã kiểm toàn bộ 20 ảnh core trong hai ZIP nộp bài. Số nhãn đếm lại từ XML là 97 + 32 = 129 shape và 48 + 32 = 80 tag, tổng **209 nhãn**; không tính tám ảnh extra ngoài bộ nộp.
**Phản hồi đã ghi nhận:** tôi xác nhận Chi đồng ý với bốn góp ý hình học dưới đây; nhận xét chung trước đó là ổn.  
**Hướng xử lý:** sửa bốn vị trí và kiểm lại trước khi chốt; cả bốn đã sửa trong bộ export hiện tại. **Quyết định nhận được sau sửa: Release.** Tôi xác nhận trong trao đổi ngày 21/11/2026 rằng Hoàng Kim Chi đã đồng ý với kết luận Release cho lô của tôi. Bốn góp ý đã được sửa; các ngoại lệ L1/R1 được giải trình theo xác nhận coach. Việc đồng ý của Chi được ghi theo xác nhận của tôi, không bổ sung chữ ký hay số liệu kiểm khác chưa được cung cấp.

### 4.1. Tổng hợp phản hồi và việc sửa

| Mã lỗi | Số lỗi/góp ý đã ghi nhận | Đồng ý? | Đã sửa? |
| --- | ---: | --- | --- |
| QC1-04 — tâm vạch | 2: A01 L2, A10 L2 | Có | Đã đưa đường về tâm sơn, export lại và kiểm cục bộ |
| QC1-07 — polygon tràn vùng | 1: crosswalk B06 | Có | Đã loại điểm dải phân cách vàng khỏi polygon |
| QC1-11 — cung fisheye | 1: lane L1 B03 | Có | Đã chỉnh cung và đồng bộ biên drivable liên quan |
| Tổng góp ý hình học | 4 | Đồng ý cả bốn | Đã sửa cả bốn |

Bảng trên chỉ tổng hợp các góp ý đã được xác nhận, không ghi 0 cho các mã chưa có kết quả kiểm của Chi. Chi kiểm toàn bộ bộ nộp theo xác nhận của tôi nên mẫu số là 209 nhãn, được tính từ XML thay vì chọn số ước lượng. Bốn góp ý chính ban đầu tương ứng **4/209 = 1,91%**; cả bốn đã được sửa. Đây là tỷ lệ của các góp ý đã ghi nhận, không phải chứng nhận mọi nhãn còn lại đều chính xác. Không dùng 71 nhãn của phiếu tôi kiểm Chi làm mẫu số cho bài của tôi.

### 4.2. Chi tiết góp ý và kết quả đối chiếu

Tôi đã gửi ảnh cho **Hoàng Kim Chi** QC chéo. Theo xác nhận của tôi trong trao đổi, Chi đồng ý với bốn góp ý dưới đây, nên tôi dùng chúng thay cho nhận xét chung trước đó. Phần quan sát chi tiết và phép đo cục bộ do AI thực hiện trên mẫu A01, A04, A10, B01, B03, B06; không ghi chúng thành số đo hay chữ ký của Chi. Tôi xác nhận Chi đã kiểm toàn bộ bộ nộp; số lượng 209 nhãn được đếm từ hai ZIP hiện tại. Theo xác nhận mới của tôi, Chi đã đồng ý Release sau sửa. Số mục kiểm chi tiết theo đủ 12 mã chưa được cung cấp nên tôi chỉ tổng hợp các góp ý đã ghi nhận, không tự điền thêm số liệu.

| Mã đề xuất | Ảnh, nhãn | Nhận xét nhận được | Tôi đồng ý? | Đã sửa trong bản export hiện tại? |
| --- | --- | --- | --- | --- |
| QC1-04, chính | A01, lane L2 | Đường vẽ lệch tâm vệt sơn; tại cột x=100, khoảng cách kiểm cục bộ khoảng 10,5 px | Đồng ý đưa đường về tâm sơn và rà lại cả polyline | Đã sửa và đối chiếu lại trong bản export mới |
| QC1-04, chính | A10, lane L2 | Polyline bám gần mép thay vì tâm sơn; khoảng cách tại điểm kiểm khoảng 9,5 px | Đồng ý chỉnh lại đoạn gần xe | Đã sửa và đối chiếu lại trong bản export mới |
| QC1-11, chính | B03, lane L1 | Đường chưa bám cung qua tâm các vệt đứt; điểm sơn chọn (770,345) cách đường khoảng 18,6 px | Đồng ý dời/thêm điểm theo cung, vẫn giữ một polyline | Đã sửa và đối chiếu lại trong bản export mới |
| QC1-07, chính | B06, crosswalk | Polygon bao một phần dải phân cách vàng; điểm (1000,470) trên dải phân cách nằm trong polygon | Đồng ý loại phần dải phân cách khỏi crosswalk, thống nhất cách thể hiện nếu bị chia cắt | Đã sửa và đối chiếu lại trong bản export mới |

Kết quả kiểm cục bộ sau sửa: A01 tại (100,571) và A10 tại (260,522) cách đường 0 px; B03 tại (770,345) còn cách khoảng 3,0 px; điểm dải phân cách (1000,470) không còn nằm trong crosswalk B06. Các số đo là phép kiểm cục bộ trên ảnh gốc, không phải sai số tối đa so với GT. Tôi ghi nhận bốn vị trí đã sửa, không dùng mẫu AI 42 shape + 24 tag làm mẫu số vì tôi đã xác nhận Chi kiểm toàn bộ bộ nộp 209 nhãn. Những lỗi này có trong bản khởi tạo có hỗ trợ AI. Cách xử lý L1/R1 được coach thông qua ở mục 3 là nội dung khác, không tự miễn các lỗi hình học vừa phát hiện.

| Nội dung | Trạng thái | Việc sẽ cập nhật khi nhận dữ liệu |
| --- | --- | --- |
| Phiếu tôi kiểm lô của Chi | Đã bổ sung đủ 12 mã cho A01, A08, A10, B01, B03, B06; 47 shape + 24 tag = 71 nhãn; revision 2 | 0 lỗi nặng, 4 lỗi chính, 0 lỗi nhẹ; 4/71 = 5,63%; Rework cho lô Chi, chờ sửa và kiểm lại |
| Phản hồi về lô của tôi | Chi kiểm toàn bộ 20 ảnh core theo xác nhận của tôi; XML có 209 nhãn; bốn góp ý đã sửa | Đã nhận xác nhận Chi đồng ý Release sau sửa, theo trao đổi của tôi ngày 21/11/2026 |
| Sửa theo góp ý đã thống nhất | Đã sửa A01 L2, A10 L2, B03 L1 và crosswalk B06; đồng bộ thêm biên drivable B03 | Đã export lại, cập nhật ảnh chụp và manifest; giữ bản trước/sau ở máy |

Lỗi chính được chia cho số nhãn thực sự đã kiểm (shape + tag), không chia cho số ảnh và không cộng lặp số mục của 12 mã làm mẫu số. Có lỗi nặng hoặc lỗi chính trên 5% thì Rework; còn ca mơ hồ ảnh hưởng kết luận thì Hold; các trường hợp còn lại mới Release theo luật lớp.

## 5. Kiểm file export

Hai file được lấy từ CVAT bằng **CVAT for images 1.1**, tắt Save images. Tôi đã đọc lại XML trong ZIP và so với nhãn đang lưu, gồm số hình, loại hình, thuộc tính, tag và tọa độ ở độ chính xác hai chữ số thập phân của export. Tất cả 20 ảnh khớp khi đối chiếu ở độ chính xác đó; đây không phải phép so với GT và không chứng minh sai số gán nhãn ≤5 px.

| File | Mở lại được? | Số shape ảnh 1 (job/file) | Số shape ảnh 2 (job/file) | Tag camera trong XML? |
| --- | --- | --- | --- | --- |
| lequangkhai-front.zip | Có, 12 ảnh | A01: 7/7 | A02: 4/4 | Có, 12/12 |
| lequangkhai-fisheye.zip | Có, 8 ảnh | B01: 3/3 | B02: 6/6 | Có, 8/8 |

Manifest `lequangkhai-manifest.json` ghi contains_images=false cho cả hai ZIP, checksum SHA-256, revision 1 và số nhãn thực tế. Lint có **8 cảnh báo nặng QC1-02, 0 chính, 0 nhẹ**; giải trình coach nằm ở mục 3. Kết luận QC sau sửa là Release theo xác nhận Chi đồng ý do tôi cung cấp; đây không phải điểm chấm GT của coach.

Bộ export này lấy sau khi hai job core đã completed và bốn vị trí đã sửa. Phiếu tôi kiểm lô Chi đã được bổ sung từ ảnh phiếu tôi cung cấp và xác nhận đã kiểm qua: hai lỗi QC1-07 ở A10/B03, hai lỗi QC1-11 ở B01/B06; không đếm trùng đối tượng. Số liệu và dấu vân tay file của Chi được chép từ phiếu, chưa đối chiếu độc lập lại hai ZIP trong phiên cập nhật. Bộ hồ sơ cá nhân đã đủ năm file bàn giao; Chi đã đồng ý Release cho lô của tôi theo xác nhận trong trao đổi, và tôi đã tự gửi ảnh minh chứng riêng. Việc Chi sửa lô của Chi để tôi kiểm lại là theo dõi riêng; phần so sánh row-anchor là tùy chọn. Điểm và kết luận chấm rubric do coach quyết định.

## 6. Ảnh chụp màn hình — minh chứng lưu riêng

Các ảnh minh chứng được chụp từ CVAT local và lưu trong bản báo cáo đầy đủ trên máy. Bản GitHub này chỉ giữ mô tả; không nhúng pixel dataset. Tôi xác nhận đã tự gửi riêng ảnh minh chứng qua kênh của lớp trong trao đổi; bản GitHub không nhúng các ảnh này.

### 6.1. Labels của project

**Bằng chứng labels:** ảnh minh chứng lưu riêng; đã được tôi gửi riêng theo xác nhận trong trao đổi.

### 6.2. A01 — lane, vùng lái và biển báo

**Bằng chứng front:** ảnh minh chứng lưu riêng; đã được tôi gửi riêng theo xác nhận trong trao đổi.

### 6.3. B03 — nhãn trên ảnh fisheye

**Bằng chứng fisheye:** ảnh minh chứng lưu riêng; đã được tôi gửi riêng theo xác nhận trong trao đổi.

### 6.4. Phóng to polyline cong ở B03

**Bằng chứng fisheye-zoom:** ảnh minh chứng lưu riêng; đã được tôi gửi riêng theo xác nhận trong trao đổi.

### 6.5. Đoạn XML thực tế từ ZIP front, có polyline lane

**Bằng chứng xml:** ảnh minh chứng lưu riêng; đã được tôi gửi riêng theo xác nhận trong trao đổi.

## 7. Tự đánh giá

Sau bài này, tôi thấy cần phân biệt rõ “đã có nhãn” và “nhãn đã đúng”. Ban đầu khi mở B10, tôi thấy các giá trị ở Objects nhưng không thấy hình vẽ; sau đó tôi hiểu đây mới là bốn tag cho toàn ảnh, còn B10 là ảnh thêm chưa có nhãn hình học. Khi rà bài core, tôi cần xem cả đường/vùng trên ảnh và thuộc tính trong Details, thay vì chỉ nhìn danh sách đối tượng.

Nhóm lỗi tôi chú ý nhất khi tự rà là **QC1-04: tâm vạch, chiều và điểm dừng**. Ở A01, đoạn R1 ban đầu kéo về phía đáy vượt phần sơn còn quan sát được. Trong quá trình làm bài có hỗ trợ AI, R1 và hai vùng drivable liên quan đã được chỉnh lại; R1 hiện bắt đầu tại (650,665) rồi đi ra xa. Tôi cũng học cách phân biệt vạch sơn lane, mép đường road_curb và vạch qua đường crosswalk; không vẽ thêm lane chỉ để làm checker hết cảnh báo. Việc giữ đúng ý nghĩa cảnh quan trọng hơn làm đủ hình theo suy đoán.

Để tránh lặp lại ở Ngày 20, tôi sẽ kiểm ảnh đầu tiên kỹ trước khi làm cả lô; mỗi ảnh đi theo thứ tự tag → lane/curb → vùng → đèn/biển → lưu. Với vạch đứt tôi giữ một polyline; đoạn che ngắn chỉ nối khi có dấu vết và bật occluded. Với fisheye tôi thêm điểm ở chỗ cong, kiểm ranh giới thân xe và quy chiếu position theo xe.

Nhãn của tôi tạo mục tiêu học cho model: polyline lane có thể nội suy thành tọa độ x tại các hàng neo; polygon drivable/crosswalk tạo vùng/mặt nạ; rectangle và thuộc tính đèn/biển tạo hộp mục tiêu và nhãn phân loại. Nếu kéo R1 qua nơi không còn thấy sơn, model sẽ được dạy rằng vẫn có vạch tại những hàng đó; sai vị trí hoặc sai trạng thái có/không có làn làm đích học sai. Việc chỉnh điểm dừng A01 giúp tránh tạo các mục tiêu không có bằng chứng từ ảnh. Màu đèn, camera và group của biển cũng phải đúng vì đó là ý nghĩa nhãn mà model học, không chỉ là phần trang trí trên CVAT.

## 8. Tùy chọn — từ polyline đến đích row-anchor

Tôi dùng R1 của A01 từ ZIP hiện tại. Hàng nằm ngoài đoạn y của polyline được ghi “không có làn”, không ngoại suy kéo dài vạch.

| y | 720 | 680 | 640 | 600 | 560 |
| --- | ---: | ---: | ---: | ---: | ---: |
| x của tôi | không có làn | không có làn | 611.7 | 550.5 | 490.7 |
| x của Chi | Chờ dữ liệu Chi | Chờ dữ liệu Chi | Chờ dữ liệu Chi | Chờ dữ liệu Chi | Chờ dữ liệu Chi |

**1. Nếu dừng sớm 40 px:** công thức nội suy là x = x1 + (y−y1)/(y2−y1) × (x2−x1), khi y nằm trên đoạn. R1 hiện trải từ y=506 đến y=665. Nếu cắt đầu xa từ 506 lên 546, các hàng được hỏi không mất thêm hàng hợp lệ vì 560/600/640 vẫn nằm trong đoạn; 680/720 vốn đã ngoài đoạn. Nếu cắt đầu gần từ 665 xuống 625 thì hàng 640 trở thành “không có làn”. Vì vậy phải nói rõ cắt ở đầu nào và xét khoảng y, không kết luận máy móc rằng mọi hàng đều đổi.

**2. So sánh với Chi:** chờ polyline cùng ảnh của Chi để tính độ lệch tại 720 và 560; không thay bằng số giả định. Hàng 720 của bản hiện tại không có làn nên cần so cả trạng thái có/không có trước khi tính chênh lệch x. Về hình học điều khiển, sai vị trí làn gần xe có thể làm sai ước lượng độ lệch ngang hiện tại; đây là giải thích của tôi, chưa phải kết quả so sánh với Chi.

**3. Đảo chiều polyline:** với một đường đơn trị theo y, đảo thứ tự điểm không đổi vị trí giao điểm nội suy, nhưng vi phạm quy tắc gần → xa. road_check lint phát hiện trường hợp front có y điểm đầu nhỏ hơn y điểm cuối; rowanchor cũng in cảnh báo về chiều. Vì thế giữ chiều đúng giúp thống nhất dữ liệu và giảm lỗi trong bước xử lý dựa vào thứ tự điểm.

Nguồn yêu cầu và cách xử lý: guideline Road v1.0, mẫu báo cáo và quy tắc bàn giao trong repo của lớp. Mục 4 đã ghi nhận Chi đồng ý Release theo xác nhận của tôi. Câu 2 mục 8 là phần so sánh tùy chọn, cập nhật nếu có polyline của Chi.
