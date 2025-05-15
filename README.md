# 简易图片图床

一个简单的图片存放图床，支持通过参数随机访问图片。

## 功能特点

- 支持按分类查看图片
- 支持指定ID查看特定图片
- 支持随机显示图片
- 简洁的界面设计

## 使用方法

访问格式: `https://coder-rangu.github.io/simple-image-host/?category=风景&id=1`

参数说明:
- `category`: 图片分类 (可选)
- `id`: 指定图片ID (可选，如不指定则随机显示)

## 添加新图片

1. 将图片文件放入 `images` 文件夹
2. 在 `images.json` 文件中添加图片信息

```json
{
    "id": 6,
    "title": "新图片标题",
    "category": "分类名称",
    "path": "images/your-image-filename.jpg"
}
```

## 部署说明

本项目可以直接部署在GitHub Pages上，无需额外的服务器支持。

## 许可证

MIT