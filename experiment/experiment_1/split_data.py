import os
import shutil

# Đường dẫn đến thư mục chứa 912 gói npm
source_dir = "malicious/npm_pack"  # Thay đổi thành đường dẫn thực tế

# Các thư mục đích
dest_dirs = [
    "data_npm/basic_corpus",  # 150 gói
    "data_npm/day_1",  # 270 gói
    "data_npm/day_2",  # 270 gói
    "data_npm/day_3"   # 65 gói
]

# Số lượng gói cho mỗi thư mục đích
counts = [502, 150, 200, 60]

# Tạo các thư mục đích nếu chưa tồn tại
for folder in dest_dirs:
    os.makedirs(folder, exist_ok=True)

# Lấy danh sách tất cả các thư mục con trong thư mục gốc
all_packages = [pkg for pkg in os.listdir(source_dir) if os.path.isdir(os.path.join(source_dir, pkg))]

# Kiểm tra tổng số thư mục
if sum(counts) > len(all_packages):
    raise ValueError("Tổng số lượng thư mục cần sao chép vượt quá số thư mục hiện có!")

# Chia và sao chép các thư mục
current_index = 0
for i, count in enumerate(counts):
    dest_dir = dest_dirs[i]
    for j in range(count):
        package = all_packages[current_index]
        src_path = os.path.join(source_dir, package)
        dest_path = os.path.join(dest_dir, package)
        shutil.copytree(src_path, dest_path)
        current_index += 1

print("Đã chia và sao chép các gói npm vào 4 thư mục thành công!")
