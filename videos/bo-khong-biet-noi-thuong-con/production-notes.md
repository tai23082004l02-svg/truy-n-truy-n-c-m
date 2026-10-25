# Ghi chú sản xuất

## Audio và phụ đề

Audio do người dùng cung cấp: `Audio Bố không biết nói thương con - giọng Aria.mp3`, MP3 mono 24 kHz, thời lượng container 524,376 giây. Không tạo lại giọng hoặc đổi tempo. Bản xuất AAC mono 48 kHz, cân âm lượng từ số đo riêng của tệp này.

Faster Whisper 1.2.1, mô hình Systran/faster-whisper-small, CPU int8, tiếng Việt, word timestamps và VAD dùng để lấy mốc lời đọc. AV 16.1.0 được dùng vì AV 19 không tương thích với lời gọi giải mã của bản Faster Whisper này. Mốc từ được đối chiếu bằng SequenceMatcher với lời thoại để sửa lỗi chính tả ASR. Các vùng thay thế ngắn dùng khoảng thời gian nhận dạng tại đúng vùng đó, không chia đều toàn bộ bài theo số chữ. Dữ liệu thô và danh sách hiệu chỉnh được giữ để rà soát.

Audio có đọc cả tiêu đề đầu bài. Cuối audio có thêm lượt “Bố ra đón”; giữ audio nguyên vẹn và phản ánh lượt này trong phụ đề. Văn bản lời thoại gốc không bị ghi đè. Có 192 cue sau khi gộp một mẩu chữ quá ngắn. Mốc phụ đề do nhận dạng tự động hỗ trợ, không tuyên bố đã được người nghe kiểm tra từng âm tiết.

## Ảnh và nhịp dựng

11 tấm nguồn 4 × 4, tổng 176 ô trước tuyển chọn, 126 ô thực sự dùng. Không coi mọi ô nguồn là hình được dùng. Một số ô được bỏ để tránh đổi cảnh quá nhanh, trùng nội dung hoặc diễn tả chưa khớp. Ví dụ ô 12 (đánh số từ 0) của sheet-07 được bỏ: hình đưa thức ăn tới miệng dễ khiến người con trông nhỏ tuổi; thay bằng cận bát cơm/miếng cá và vẻ mặt người con.

Các đường chia hàng thực tế không cách đều nhau. Script dò dải trắng trên từng tấm, bỏ viền, cắt 16:9 ở giữa ô và scale giữ tỷ lệ; lưu tọa độ thật trong grid-crops.json. Không đưa contact sheet nguyên tấm vào phim.

Các điểm đổi hình được chọn theo nội dung lời đọc rồi làm tròn ra frame ở 24 fps, tránh lệch tích lũy. Loại các điểm cắt cách nhau dưới 2,5 giây. Không thêm đoạn im lặng để kéo dài video. Không zoom/pan/rung hay hiệu ứng chuyển cảnh.

Người con được thể hiện là nữ để phù hợp giọng kể Aria; áo vàng và tóc buộc thấp nhận diện xuyên suốt. Bố có tóc bạc và nếp nhăn rõ hơn ở phần sau. Đây là minh họa cách điệu; không khẳng định từng nét mặt giống hệt giữa mọi ảnh AI.

## Phạm vi và quyền sử dụng

Kịch bản là chuyện hư cấu được viết cho dự án, không được trình bày như lời chứng của một gia đình thật. Hình minh họa tạo mới bằng công cụ tạo ảnh, dùng ảnh trước làm tham chiếu phong cách và nhân vật. Không lấy hình từ video có sẵn để ghép vào bản mới. Audio do người dùng cung cấp. Không sử dụng nhạc bên thứ ba.

## Kiểm tra bản xuất

MP4 giải mã toàn bộ không có lỗi. 12.585 frame ở 24 fps, thời lượng 524,375 giây; 126 cảnh liền mạch, 192 cue không chồng nhau. Audio sau AAC đo -16,03 LUFS, true peak -1,64 dBTP. Đối chiếu tương quan audio gốc/bản xuất tại giây 20, 250 và 500 cho độ trễ 0 giây ở độ phân giải đo 1/8000 giây. Kiểm tra vùng hình không có phụ đề ở 3 cảnh cho thấy hình tĩnh trong sai số nén. Đã xem 12 khung đại diện dọc timeline, mẫu phụ đề đầy khung và thumbnail. Các kiểm tra này không thay cho việc nghe thủ công từng âm tiết.
