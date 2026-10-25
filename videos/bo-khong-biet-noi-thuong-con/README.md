# Bố không biết nói thương con

Câu chuyện hư cấu bằng tiếng Việt về tình thương ít lời của bố, qua lời kể của người con đi làm xa. Bố còn sống ở đoạn kết.

## Xem hoặc tải

- **[Tải video MP4](Bo-khong-biet-noi-thuong-con.mp4)** — H.264/AAC, 1280 × 720, 24 fps, khoảng 8 phút 44 giây.
- [Phụ đề tiếng Việt SRT](subtitles.srt), đồng thời được gắn vào hình trong MP4.
- [Lời thoại](loi-thoai.txt).
- [Audio gốc giọng Aria do người dùng cung cấp](audio-goc.mp3).
- [Tiêu đề và mô tả gợi ý](youtube-description.txt).
- [Ghi chú sản xuất](production-notes.md) và [kết quả kiểm tra](validation-summary.json).

![Hình đại diện](thumbnail.jpg)

## Hình ảnh và dựng

126 hình được tuyển từ 11 tấm 4 × 4, trung bình khoảng 4,2 giây/cảnh. Cảnh toàn, cảnh gia đình và cận đồ vật được phối hợp theo lời kể. Phong cách minh họa 2D, màu dịu, nhân vật và bối cảnh gia đình Việt Nam nhất quán theo hướng dẫn tham khảo ở kho `tai23082004l02-svg/YTB-ng-i-que`.

Hình đứng yên, chuyển thẳng; không zoom, pan, rung, header hoặc bộ đếm. Đây là video minh họa tĩnh có đổi cảnh, không có chuyển động tay chân riêng. Phụ đề chữ sáng viền tối ở dưới, không dải nền đen cố định.

Giữ giọng Aria và tốc độ audio đã gửi; chỉ cân âm lượng cho bản xuất. Không dùng nhạc của bên thứ ba. Ảnh nguồn nhiều ô được phóng lên 720p sau khi cắt; không phải từng ảnh nguồn được tạo độc lập ở 720p.

## Dữ liệu để sửa về sau

- `project/assets/`: toàn bộ 11 tấm ảnh nguồn AI.
- `project/story-bible.json`: tạo hình nhân vật và bối cảnh.
- `project/grid-crops.json`: ranh giới lưới thực tế và vùng cắt giữ tỷ lệ.
- `project/shots.json`: nguồn ô ảnh và mốc frame từng cảnh.
- `project/captions.json`, `aligned-words.json`, `transcript-asr.json`, `alignment-review.json`: phụ đề, mốc từ và dữ liệu đối chiếu.
- `project/render.py`: script dựng, cần Python 3.12, FFmpeg có libx264/libass, font Noto Sans và các thư viện trong `project/requirements-render.txt`.

Để dựng lại: cài thư viện vào môi trường Python riêng, chạy `python project/render.py` từ thư mục này. Thư mục tạm mặc định ở `/tmp/bo-khong-biet-noi-thuong-con-build`, có thể đổi bằng biến `VIDEO_BUILD_DIR`. Dùng checkout đang có; không cần tạo Git worktree.

Video và tài liệu được bàn giao qua GitHub. Chưa đăng hoặc lên lịch trên YouTube.
