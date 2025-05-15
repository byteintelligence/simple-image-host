document.addEventListener('DOMContentLoaded', function() {
    // 获取URL参数
    const urlParams = new URLSearchParams(window.location.search);
    const category = urlParams.get('category');
    const id = urlParams.get('id');
    
    // 加载图片数据
    fetch('images.json')
        .then(response => response.json())
        .then(data => {
            let filteredImages = data;
            
            // 按分类筛选
            if (category) {
                filteredImages = data.filter(img => img.category === category);
            }
            
            if (filteredImages.length === 0) {
                displayError('没有找到符合条件的图片');
                return;
            }
            
            let selectedImage;
            
            // 按ID查找
            if (id) {
                selectedImage = filteredImages.find(img => img.id.toString() === id);
                if (!selectedImage) {
                    displayError(`没有找到ID为 ${id} 的图片`);
                    return;
                }
            } else {
                // 随机选择一张图片
                const randomIndex = Math.floor(Math.random() * filteredImages.length);
                selectedImage = filteredImages[randomIndex];
            }
            
            displayImage(selectedImage);
        })
        .catch(error => {
            console.error('加载图片数据失败:', error);
            displayError('加载图片数据失败');
        });
});

function displayImage(image) {
    const container = document.getElementById('image-container');
    container.innerHTML = `
        <img src="${image.path}" alt="${image.title || '图片'}">
        <h3>${image.title || '未命名图片'}</h3>
        <p>分类: ${image.category || '未分类'}</p>
        <p>ID: ${image.id}</p>
    `;
}

function displayError(message) {
    const container = document.getElementById('image-container');
    container.innerHTML = `<p style="color: red;">${message}</p>`;
}