// 图片API接口

// 获取URL参数
function getQueryParams() {
    const params = {};
    const queryString = window.location.search.substring(1);
    const pairs = queryString.split('&');
    
    for (let i = 0; i < pairs.length; i++) {
        if (!pairs[i]) continue;
        const pair = pairs[i].split('=');
        params[decodeURIComponent(pair[0])] = decodeURIComponent(pair[1] || '');
    }
    
    return params;
}

// 加载图片数据
async function loadImageData() {
    try {
        const response = await fetch('images.json');
        if (!response.ok) {
            throw new Error('无法加载图片数据');
        }
        return await response.json();
    } catch (error) {
        console.error('加载图片数据失败:', error);
        return [];
    }
}

// 获取图片URL
async function getImageUrl() {
    const params = getQueryParams();
    const category = params.category;
    const id = params.id;
    
    const images = await loadImageData();
    if (images.length === 0) {
        return { error: '没有可用的图片' };
    }
    
    let filteredImages = images;
    
    // 按分类筛选
    if (category) {
        filteredImages = images.filter(img => img.category === category);
        if (filteredImages.length === 0) {
            return { error: `没有找到分类为 ${category} 的图片` };
        }
    }
    
    // 按ID查找
    if (id) {
        const selectedImage = filteredImages.find(img => img.id.toString() === id);
        if (!selectedImage) {
            return { error: `没有找到ID为 ${id} 的图片` };
        }
        return { image: selectedImage };
    }
    
    // 随机选择一张图片
    const randomIndex = Math.floor(Math.random() * filteredImages.length);
    return { image: filteredImages[randomIndex] };
}

// 如果是直接访问API页面，返回JSON数据
if (window.location.pathname.endsWith('/api.js') || window.location.pathname.endsWith('/api')) {
    document.addEventListener('DOMContentLoaded', async () => {
        const result = await getImageUrl();
        document.body.innerHTML = `<pre>${JSON.stringify(result, null, 2)}</pre>`;
    });
}

// 导出函数供其他脚本使用
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { getImageUrl, loadImageData };
}