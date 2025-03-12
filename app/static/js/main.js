// 全局JavaScript功能

// 激活Bootstrap工具提示和弹出框
document.addEventListener('DOMContentLoaded', function() {
    // 激活所有工具提示
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // 激活所有弹出框
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function(popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
    
    // 给卡片添加点击事件（在首页）
    const functionCards = document.querySelectorAll('.card');
    functionCards.forEach(card => {
        // 查找卡片内的链接按钮
        const linkBtn = card.querySelector('.btn-primary');
        if (linkBtn) {
            // 点击卡片时触发链接按钮的点击事件
            card.addEventListener('click', function(event) {
                // 如果点击的不是按钮本身，则模拟点击按钮
                if (event.target !== linkBtn && !linkBtn.contains(event.target)) {
                    linkBtn.click();
                }
            });
        }
    });
}); 