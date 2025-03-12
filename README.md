# 函数演示平台

这是一个用于数学教学的函数演示平台，使用Python Flask框架开发。该平台可以直观地展示各种数学函数的图像，并允许用户通过调整参数实时观察函数图像的变化。

## 功能特点

- 展示多种常见数学函数（线性函数、二次函数、指数函数、对数函数、三角函数等）
- 交互式参数调整，实时更新函数图像
- 包含函数说明和公式展示
- 直观的用户界面，适合教学使用
- **函数对比功能**：可以在同一张图上比较多个函数
- **导出图像功能**：可以将生成的函数图像保存为图片文件
- **函数分类展示**：按照函数类别组织，便于查找
- **中文字体支持**：完整支持中文显示

## 安装步骤

1. 克隆或下载本项目代码
2. 安装所需依赖：
   ```
   pip install -r requirements.txt
   ```
3. 运行应用：
   ```
   python run.py
   ```
4. 在浏览器中访问：`http://127.0.0.1:5000/`

## 函数类型

### 基础函数
- 线性函数
- 二次函数
- 指数函数
- 对数函数
- 三角函数

### 三角函数
- 正弦函数（基础三角函数）
- 余弦函数
- 正切函数

### 特殊函数
- 绝对值函数
- 幂函数
- 平方根函数
- 倒数函数

### 高等函数
- 双曲函数
- 高斯函数
- 多项式函数

## 技术栈

- 后端：Python Flask
- 函数计算：NumPy, SciPy
- 图形绘制：Matplotlib
- 前端：HTML, CSS, JavaScript, Bootstrap 5
- 交互：AJAX, Fetch API

## 适用对象

- 数学教师：作为教学辅助工具
- 学生：用于自主学习和探索函数特性
- 任何对数学函数感兴趣的人

## 项目结构

```
/app
  /static
    /css
      style.css     # 自定义样式
    /js
      main.js       # 全局JS功能
    /images         # 静态图片
    /temp           # 导出图像临时存储
  /templates
    base.html       # 基础模板
    index.html      # 首页
    function.html   # 函数详情页
    compare.html    # 函数对比页
  __init__.py       # 应用初始化
  routes.py         # 路由定义
requirements.txt    # 依赖列表
run.py              # 应用入口
README.md           # 项目说明
```

## 更新记录

### 最新更新
- 添加支持中文的字体配置
- 添加更多类型的函数（总计14种函数）
- 实现函数对比功能
- 添加导出图像功能
- 按类别组织函数，优化导航

## 拓展方向

- 支持自定义函数表达式
- 添加函数求导和积分功能
- 支持3D函数图像
- 添加用户账户系统，保存自定义函数
- 添加函数特征点分析（如极值点、拐点等）
