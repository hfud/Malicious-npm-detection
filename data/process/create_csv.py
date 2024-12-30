import os
import hashlib
import json
import csv

def hash_package(root):
    """
    Tính hash giống với logic trong đoạn code clone-detect.
    `package.json` sẽ bị loại bỏ trường `name` và `version`.
    """
    m = hashlib.md5()
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames.sort()
        for filename in sorted(filenames):
            path = os.path.join(dirpath, filename)
            m.update(f"{os.path.relpath(path, root)}\n".encode("utf-8"))  # Đường dẫn tương đối với xuống dòng
            if filename == "package.json":
                with open(path, "r", encoding="utf-8") as f:
                    pkg = json.load(f)
                    pkg["name"] = ""
                    pkg["version"] = ""
                    m.update(json.dumps(pkg, sort_keys=True).encode("utf-8"))
            else:
                with open(path, "rb") as f:
                    m.update(f.read())  # Hash nội dung file
    return m.hexdigest()

def process_packages(base_dir, analysis_label):
    """
    Duyệt qua các gói và tính hash cho từng version.
    """
    data = []
    for package in os.listdir(base_dir):
        package_path = os.path.join(base_dir, package)
        if os.path.isdir(package_path):  # Kiểm tra package là thư mục
            for version in os.listdir(package_path):
                version_path = os.path.join(package_path, version)
                if os.path.isdir(version_path):  # Kiểm tra version là thư mục
                    package_hash = hash_package(version_path)
                    data.append([package, version, package_hash, analysis_label])
    return data

def main():
    # Đường dẫn đến thư mục malicious và benign
    malicious_dir = "Malicious"
    benign_dir = "Benign"
    output_file = "basic_corpus.csv"

    # Xử lý từng thư mục và tính hash
    malicious_data = process_packages(malicious_dir, "malicious")
    benign_data = process_packages(benign_dir, "benign")

    # Ghi dữ liệu vào file CSV
    with open(output_file, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["package", "version", "hash", "analysis"])  # Ghi header
        writer.writerows(malicious_data + benign_data)  # Ghi dữ liệu

    print(f"File CSV đã được tạo: '{output_file}'")

if __name__ == "__main__":
    main()
