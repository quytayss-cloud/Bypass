# AI Smart Multi-Platform Downloader (GitHub Ready)

Ứng dụng web tải video 4K/2K và nhạc Hi-Res (FLAC, ALAC) từ YouTube, TikTok, Instagram có tích hợp AI chống chặn.

## Hướng dẫn đưa lên GitHub:
1. Tạo một repository mới trên GitHub (ví dụ: `ai-downloader`).
2. Giải nén toàn bộ tệp này và push lên repository đó.

## Hướng dẫn cài đặt và chạy trên VPS/Server:
1. Cài đặt Python 3.10+ và FFmpeg (`sudo apt install ffmpeg`).
2. Cài đặt thư viện:
   ```bash
   pip install -r requirements.txt
   ```
3. Chạy ứng dụng:
   ```bash
   python main.py
   ```
   *(Hoặc chạy nhanh bằng Docker: `docker-compose up -d`)*
4. Truy cập qua trình duyệt điện thoại/máy tính tại: `http://<IP_VPS_HOẶC_LOCALHOST>:8000`
