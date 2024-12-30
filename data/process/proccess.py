#!/bin/bash

# Tạo thư mục output nếu chưa có
output_dir="output"
mkdir -p "$output_dir"

# Duyệt qua tất cả các thư mục cha trong thư mục hiện tại
for parent_dir in */; do
    # Kiểm tra nếu thư mục cha là thư mục và có tên bắt đầu với "@"
    if [[ -d "$parent_dir" ]]; then
        # Lấy tên thư mục cha
        parent_name=$(basename "$parent_dir")
        
        # Nếu tên thư mục cha bắt đầu bằng "@" thì đổi tên thư mục con
        if [[ "$parent_name" == @* ]]; then
            # Duyệt qua các thư mục con trong thư mục cha
            for dir in "$parent_dir"*/; do
                # Kiểm tra nếu là thư mục (không phải file)
                if [ -d "$dir" ]; then
                    # Tạo tên thư mục mới bằng cách kết hợp tên thư mục cha và thư mục con
                    new_name="${parent_name}@$(basename "$dir")"
                    
                    # Tạo thư mục con trong thư mục output
                    mkdir -p "$output_dir/$new_name"
                    
                    # Di chuyển nội dung từ thư mục con cũ sang thư mục mới trong output
                    mv "$dir"/* "$output_dir/$new_name/"
                    
                    # Xóa thư mục con cũ sau khi đã di chuyển
                    rmdir "$dir"
                    
                    echo "Đã tạo thư mục mới và di chuyển nội dung: $dir -> $output_dir/$new_name"
                fi
            done
        else
            # Nếu thư mục cha không bắt đầu bằng "@", di chuyển nguyên thư mục con vào thư mục output
            mkdir -p "$output_dir/$parent_name"
            mv "$parent_dir"/* "$output_dir/$parent_name/"
            echo "Giữ nguyên thư mục con trong thư mục cha: $parent_dir -> $output_dir/$parent_name"
        fi
    fi
done
