# 简单图片图床

一个简单的图片存放图床，支持通过参数随机访问图片，也支持类似 picsum.photos 的 URL 格式。

## 功能特点

- 支持按分类查看图片
- 支持指定ID查看特定图片
- 支持随机显示图片
- 支持指定图片尺寸
- 支持类似 picsum.photos 的 URL 格式
- 简洁的界面设计

## 使用方法

### 1. 参数查询方式

访问格式: `https://devpulseGu.github.io/pixrand/?category=风景&id=1`

参数说明:
- `category`: 图片分类 (可选)
- `id`: 指定图片ID (可选，如不指定则随机显示)

### 2. 路径方式 (类似 picsum.photos)

访问格式: `https://devpulseGu.github.io/pixrand/id/1/200/300`

路径说明:
- `/id/数字`: 指定图片ID
- `/宽度/高度`: 指定图片尺寸
- `/尺寸`: 指定正方形图片尺寸

示例:
- `https://devpulseGu.github.io/pixrand/id/1/200/300` - 显示ID为1的图片，尺寸为200×300
- `https://devpulseGu.github.io/pixrand/200/300` - 随机显示一张图片，尺寸为200×300
- `https://devpulseGu.github.io/pixrand/400` - 随机显示一张正方形图片，尺寸为400×400

### 3. 简洁图片页面

如果只想显示图片，没有其他元素，可以使用 image.html:

`https://devpulseGu.github.io/pixrand/image.html?id=3`

## 添加新图片

1. 将图片文件放入 `images` 文件夹
2. 在 `images.json` 文件中添加图片信息

```json
{
    "id": 6,
    "title": "新图片标题",
    "category": "分类名称",
    "path": "images/your-image-filename.svg"
}
```

## 部署说明

本项目可以直接部署在GitHub Pages上，无需独立的服务器支持。

## 许可协议

MIT