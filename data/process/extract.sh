#!/bin/bash

if [ $# -ne 2 ]; then
    echo "Usage: $0 source-directory destination-directory"
    exit 1
fi

source_dir=$1
destination_dir=$2

# Tạo thư mục đích nếu chưa tồn tại
mkdir -p "$destination_dir"

# Tìm tất cả các file .zip trong thư mục nguồn
find "$source_dir" -type f -name '*.zip' | while read sample; do
    # Tạo đường dẫn đích tương ứng trong cùng thư mục
    relative_path=$(realpath --relative-to="$source_dir" "$(dirname "$sample")")
    target_dir="$destination_dir/$relative_path"

    # Tạo thư mục đích tương ứng
    mkdir -p "$target_dir"

    # Giải nén file ZIP vào thư mục đích
    unzip -o -P infected "$sample" -d "$target_dir" >/dev/null 2>&1
    if [ $? -eq 0 ]; then
        echo "Đã giải nén: $sample vào $target_dir"
    else
        echo "Không thể giải nén: $sample"
    fi
done

echo "Hoàn tất giải nén tất cả các file ZIP vào $destination_dir."
