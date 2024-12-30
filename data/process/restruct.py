import os
import shutil
import argparse

# Hàm để di chuyển các tệp cùng cấp với file JSON ra thư mục đích
def move_files_to_version_dir(version_dir):
    for root, dirs, files in os.walk(version_dir, topdown=False):
        for file in files:
            if file.endswith(".json"):
                json_dir = root  # Thư mục chứa file JSON

                # Di chuyển tất cả file và thư mục cùng cấp với file JSON ra thư mục version
                for item in os.listdir(json_dir):
                    item_path = os.path.join(json_dir, item)
                    target_path = os.path.join(version_dir, item)

                    if os.path.exists(target_path):
                        # Nếu file hoặc thư mục đã tồn tại, bỏ qua hoặc hợp nhất (tùy chỉnh nếu cần)
                        print(f"Bỏ qua: {target_path} đã tồn tại.")
                        continue

                    shutil.move(item_path, target_path)

                break  # Không cần tìm thêm file JSON khác trong cùng thư mục

        # Xóa thư mục trống
        if not os.listdir(root):
            os.rmdir(root)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Di chuyển các tệp cùng cấp với file JSON ra thư mục đích.")
    parser.add_argument("base_dir", type=str, help="Đường dẫn thư mục gốc chứa các package/version")

    args = parser.parse_args()
    base_dir = args.base_dir

    # Kiểm tra sự tồn tại của thư mục gốc
    if not os.path.isdir(base_dir):
        print(f"Thư mục '{base_dir}' không tồn tại.")
        exit(1)

    # Lặp qua từng thư mục package/version
    for package in os.listdir(base_dir):
        package_path = os.path.join(base_dir, package)

        if os.path.isdir(package_path):
            for version in os.listdir(package_path):
                version_path = os.path.join(package_path, version)

                if os.path.isdir(version_path):
                    print(f"Xử lý: {version_path}")
                    move_files_to_version_dir(version_path)

    print("Hoàn tất!")