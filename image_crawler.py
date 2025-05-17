#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
图片自动爬取脚本
定期从网络上爬取图片并更新到图床中
'''

import os
import json
import random
import requests
import argparse
from datetime import datetime
from urllib.parse import urlparse

# 配置信息
CONFIG = {
    'unsplash_api_url': 'https://api.unsplash.com/photos/random',
    'pexels_api_url': 'https://api.pexels.com/v1/curated',
    'image_dir': 'images',
    'json_file': 'images.json',
    'categories': ['风景', '城市', '动物', '建筑', '自然', '科技', '艺术', '美食'],
    'max_images': 20,  # 最大图片数量
    'image_format': 'jpg'  # 图片格式
}

# 确保脚本目录存在
def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# 从Unsplash获取随机图片
def get_unsplash_image(api_key, category=None):
    headers = {
        'Authorization': f'Client-ID {api_key}'
    }
    
    params = {}
    if category:
        params['query'] = category
    
    try:
        response = requests.get(CONFIG['unsplash_api_url'], headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            return {
                'url': data['urls']['regular'],
                'title': data.get('description', 'Unsplash图片') or f"Unsplash图片_{random.randint(1000, 9999)}",
                'category': category or random.choice(CONFIG['categories'])
            }
    except Exception as e:
        print(f"从Unsplash获取图片失败: {e}")
    
    return None

# 从Pexels获取图片
def get_pexels_image(api_key, category=None):
    headers = {
        'Authorization': api_key
    }
    
    params = {
        'per_page': 1,
        'page': random.randint(1, 20)
    }
    
    try:
        response = requests.get(CONFIG['pexels_api_url'], headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            if data['photos']:
                photo = data['photos'][0]
                return {
                    'url': photo['src']['large'],
                    'title': photo.get('alt', 'Pexels图片') or f"Pexels图片_{random.randint(1000, 9999)}",
                    'category': category or random.choice(CONFIG['categories'])
                }
    except Exception as e:
        print(f"从Pexels获取图片失败: {e}")
    
    return None

# 下载图片
def download_image(image_info, image_dir, image_id):
    try:
        response = requests.get(image_info['url'], stream=True)
        if response.status_code == 200:
            # 从URL中获取文件扩展名
            parsed_url = urlparse(image_info['url'])
            path = parsed_url.path
            ext = os.path.splitext(path)[1]
            if not ext:
                ext = f".{CONFIG['image_format']}"
            
            # 构建文件名
            filename = f"image_{image_id}{ext}"
            filepath = os.path.join(image_dir, filename)
            
            # 保存图片
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            return filename
    except Exception as e:
        print(f"下载图片失败: {e}")
    
    return None

# 更新图片JSON数据
def update_image_json(json_file, new_image):
    try:
        # 读取现有JSON数据
        if os.path.exists(json_file):
            with open(json_file, 'r', encoding='utf-8') as f:
                images = json.load(f)
        else:
            images = []
        
        # 添加新图片
        images.append(new_image)
        
        # 如果超过最大数量，删除最早的图片
        if len(images) > CONFIG['max_images']:
            # 按ID排序
            images = sorted(images, key=lambda x: x['id'])
            # 删除文件
            old_image = images[0]
            old_image_path = os.path.join(os.path.dirname(json_file), old_image['path'])
            if os.path.exists(old_image_path):
                os.remove(old_image_path)
            # 从列表中移除
            images.pop(0)
        
        # 保存更新后的JSON
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(images, f, ensure_ascii=False, indent=4)
        
        return True
    except Exception as e:
        print(f"更新JSON数据失败: {e}")
        return False

# 获取下一个可用的图片ID
def get_next_image_id(json_file):
    try:
        if os.path.exists(json_file):
            with open(json_file, 'r', encoding='utf-8') as f:
                images = json.load(f)
            if images:
                return max(image['id'] for image in images) + 1
        return 1
    except Exception as e:
        print(f"获取下一个ID失败: {e}")
        return 1

# 主函数
def main():
    parser = argparse.ArgumentParser(description='自动爬取图片并更新到图床')
    parser.add_argument('--unsplash-key', help='Unsplash API密钥')
    parser.add_argument('--pexels-key', help='Pexels API密钥')
    parser.add_argument('--category', help='指定图片分类')
    parser.add_argument('--count', type=int, default=1, help='爬取图片数量')
    args = parser.parse_args()
    
    # 确保目录存在
    script_dir = os.path.dirname(os.path.abspath(__file__))
    image_dir = os.path.join(script_dir, CONFIG['image_dir'])
    json_file = os.path.join(script_dir, CONFIG['json_file'])
    
    ensure_dir(image_dir)
    
    # 爬取指定数量的图片
    for _ in range(args.count):
        image_info = None
        
        # 尝试从Unsplash获取图片
        if args.unsplash_key:
            image_info = get_unsplash_image(args.unsplash_key, args.category)
        
        # 如果Unsplash失败，尝试从Pexels获取
        if not image_info and args.pexels_key:
            image_info = get_pexels_image(args.pexels_key, args.category)
        
        # 如果没有API密钥或获取失败，使用占位图片
        if not image_info:
            placeholder_url = f"https://picsum.photos/800/600?random={random.randint(1, 1000)}"
            image_info = {
                'url': placeholder_url,
                'title': f"随机图片_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                'category': args.category or random.choice(CONFIG['categories'])
            }
        
        # 获取下一个可用ID
        next_id = get_next_image_id(json_file)
        
        # 下载图片
        filename = download_image(image_info, image_dir, next_id)
        if filename:
            # 更新JSON
            new_image = {
                'id': next_id,
                'title': image_info['title'],
                'category': image_info['category'],
                'path': f"images/{filename}"
            }
            
            if update_image_json(json_file, new_image):
                print(f"成功添加图片: {new_image['title']} (ID: {next_id})")
            else:
                print("添加图片失败")
        else:
            print("下载图片失败")

# 无需API密钥的简化版爬虫函数
def crawl_images_simple(count=1, category=None):
    """无需API密钥的简化版爬虫函数，可以直接在其他脚本中调用"""
    # 确保目录存在
    script_dir = os.path.dirname(os.path.abspath(__file__))
    image_dir = os.path.join(script_dir, CONFIG['image_dir'])
    json_file = os.path.join(script_dir, CONFIG['json_file'])
    
    ensure_dir(image_dir)
    
    results = []
    # 爬取指定数量的图片
    for _ in range(count):
        # 使用占位图片服务
        category_text = category or random.choice(CONFIG['categories'])
        placeholder_url = f"https://picsum.photos/800/600?random={random.randint(1, 1000)}"
        image_info = {
            'url': placeholder_url,
            'title': f"{category_text}_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            'category': category_text
        }
        
        # 获取下一个可用ID
        next_id = get_next_image_id(json_file)
        
        # 下载图片
        filename = download_image(image_info, image_dir, next_id)
        if filename:
            # 更新JSON
            new_image = {
                'id': next_id,
                'title': image_info['title'],
                'category': image_info['category'],
                'path': f"images/{filename}"
            }
            
            if update_image_json(json_file, new_image):
                print(f"成功添加图片: {new_image['title']} (ID: {next_id})")
                results.append(new_image)
            else:
                print("添加图片失败")
        else:
            print("下载图片失败")
    
    return results

if __name__ == '__main__':
    main()