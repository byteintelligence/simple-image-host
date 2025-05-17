#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
删除示例图片脚本
'''

import os
import json

# 配置信息
JSON_FILE = 'images.json'

# 要删除的文件前缀
SAMPLE_PREFIX = 'sample'

# 更新图片JSON数据
def update_image_json(json_file):
    try:
        # 读取现有JSON数据
        if os.path.exists(json_file):
            with open(json_file, 'r', encoding='utf-8') as f:
                images = json.load(f)
        else:
            print(f"文件 {json_file} 不存在")
            return False
        
        # 过滤掉sample开头的图片
        filtered_images = [img for img in images if SAMPLE_PREFIX not in img['path']]
        
        # 如果有图片被过滤掉
        if len(filtered_images) < len(images):
            print(f"从JSON中移除了 {len(images) - len(filtered_images)} 个示例图片")
            
            # 保存更新后的JSON
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(filtered_images, f, ensure_ascii=False, indent=4)
            
            return True
        else:
            print("没有找到示例图片")
            return False
    except Exception as e:
        print(f"更新JSON数据失败: {e}")
        return False

# 主函数
def main():
    # 更新JSON文件
    if update_image_json(JSON_FILE):
        print(f"成功更新 {JSON_FILE} 文件，移除了示例图片的引用")
    else:
        print(f"更新 {JSON_FILE} 文件失败或没有需要移除的图片")

if __name__ == '__main__':
    main()