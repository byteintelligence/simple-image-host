# 图片爬虫使用说明

本项目包含一个自动爬取图片的Python脚本，可以用来定期更新图床中的图片。

## 使用方法

### 前提条件

- 安装Python 3.6+
- 安装必要的依赖：`pip install requests`

### 基本用法

```bash
# 爬取1张随机图片（默认）
python image_crawler.py

# 爬取指定数量的图片
python image_crawler.py --count 5

# 爬取指定分类的图片
python image_crawler.py --category 风景
```

### 高级用法

如果你有Unsplash或Pexels的API密钥，可以获取更高质量的图片：

```bash
# 使用Unsplash API
python image_crawler.py --unsplash-key YOUR_API_KEY

# 使用Pexels API
python image_crawler.py --pexels-key YOUR_API_KEY
```

## 自动化运行

你可以设置定时任务来自动运行爬虫脚本，定期更新图床中的图片。

### 在Linux/Mac上设置cron任务

```bash
# 编辑crontab
crontab -e

# 添加以下行（每天凌晨3点运行）
0 3 * * * cd /path/to/simple-image-host && python image_crawler.py --count 3
```

### 在Windows上使用任务计划程序

1. 打开任务计划程序
2. 创建基本任务
3. 设置触发器为每天凌晨3点
4. 操作选择"启动程序"
5. 程序/脚本选择`python.exe`
6. 添加参数：`image_crawler.py --count 3`
7. 起始位置：你的仓库路径

## 脚本工作原理

1. 从网络上获取随机图片（使用Unsplash API、Pexels API或picsum.photos）
2. 下载图片并保存到`images`目录
3. 更新`images.json`文件，添加新图片的信息
4. 如果图片数量超过设定的最大值，会删除最早的图片

## 在代码中调用

你也可以在其他Python脚本中直接调用爬虫函数：

```python
from image_crawler import crawl_images_simple

# 爬取3张风景分类的图片
new_images = crawl_images_simple(count=3, category="风景")
print(f"成功爬取了{len(new_images)}张图片")
```

## 注意事项

- 请遵守图片源网站的使用条款和API限制
- 不要过于频繁地爬取图片，以免被封IP
- 建议使用自己的API密钥，以获取更高质量的图片和更稳定的服务
