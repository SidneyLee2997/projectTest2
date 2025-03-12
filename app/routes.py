from flask import render_template, request, jsonify, send_file
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import io
import base64
import os
import uuid
from datetime import datetime
from app import app
import matplotlib

# 配置matplotlib支持中文
matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS', 'sans-serif']
matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# 创建临时图像存储目录
if not os.path.exists('app/static/temp'):
    os.makedirs('app/static/temp')

# 函数定义
functions = {
    '线性函数': {
        'formula': 'f(x) = ax + b',
        'description': '线性函数是最基本的函数类型，图像是一条直线。a决定斜率，b决定y轴截距。',
        'params': {'a': 1, 'b': 0},
        'eval': lambda x, a, b: a * x + b,
        'category': '基础函数'
    },
    '二次函数': {
        'formula': 'f(x) = ax² + bx + c',
        'description': '二次函数的图像是抛物线。a决定开口方向和宽窄，b影响轴的位置，c决定y轴截距。',
        'params': {'a': 1, 'b': 0, 'c': 0},
        'eval': lambda x, a, b, c: a * x**2 + b * x + c,
        'category': '基础函数'
    },
    '指数函数': {
        'formula': 'f(x) = a × b^x',
        'description': '指数函数表示以b为底的指数增长，a是比例系数。',
        'params': {'a': 1, 'b': 2},
        'eval': lambda x, a, b: a * b**x,
        'category': '基础函数'
    },
    '对数函数': {
        'formula': 'f(x) = log_b(x)',
        'description': '对数函数是指数函数的反函数，表示以b为底的对数。',
        'params': {'b': 10},
        'eval': lambda x, b: np.log(x) / np.log(b) if np.all(x > 0) else np.nan,
        'category': '基础函数'
    },
    '三角函数': {
        'formula': 'f(x) = a × sin(bx + c)',
        'description': '正弦函数是最基本的三角函数之一，a决定振幅，b决定频率，c决定相位。',
        'params': {'a': 1, 'b': 1, 'c': 0},
        'eval': lambda x, a, b, c: a * np.sin(b * x + c),
        'category': '基础函数'
    },
    '余弦函数': {
        'formula': 'f(x) = a × cos(bx + c)',
        'description': '余弦函数是基本的三角函数之一，a决定振幅，b决定频率，c决定相位。',
        'params': {'a': 1, 'b': 1, 'c': 0},
        'eval': lambda x, a, b, c: a * np.cos(b * x + c),
        'category': '三角函数'
    },
    '正切函数': {
        'formula': 'f(x) = tan(x)',
        'description': '正切函数tan(x)=sin(x)/cos(x)，在cos(x)=0的点处有间断点。',
        'params': {'a': 1},
        'eval': lambda x, a: a * np.tan(x),
        'category': '三角函数'
    },
    '绝对值函数': {
        'formula': 'f(x) = |x|',
        'description': '绝对值函数返回x的绝对值，图像在原点处有一个尖角。',
        'params': {'a': 1},
        'eval': lambda x, a: a * np.abs(x),
        'category': '特殊函数'
    },
    '幂函数': {
        'formula': 'f(x) = x^n',
        'description': '幂函数是指数为常数的函数，n决定了曲线的形状。',
        'params': {'n': 2},
        'eval': lambda x, n: np.power(x, n),
        'category': '特殊函数'
    },
    '双曲函数': {
        'formula': 'f(x) = sinh(x)',
        'description': '双曲正弦函数，类似于正弦函数但增长更快。',
        'params': {'a': 1},
        'eval': lambda x, a: a * np.sinh(x),
        'category': '高等函数'
    },
    '平方根函数': {
        'formula': 'f(x) = √x',
        'description': '平方根函数返回x的正平方根，定义域为非负实数。',
        'params': {'a': 1},
        'eval': lambda x, a: a * np.sqrt(np.maximum(x, 0)),
        'category': '特殊函数'
    },
    '倒数函数': {
        'formula': 'f(x) = 1/x',
        'description': '倒数函数返回x的倒数，在x=0处有间断点。',
        'params': {'a': 1},
        'eval': lambda x, a: a / x,
        'category': '特殊函数'
    },
    '高斯函数': {
        'formula': 'f(x) = a × e^(-(x-b)²/(2c²))',
        'description': '高斯函数（正态分布）是统计学中重要的函数，a控制高度，b控制中心，c控制宽度。',
        'params': {'a': 1, 'b': 0, 'c': 1},
        'eval': lambda x, a, b, c: a * np.exp(-((x-b)**2)/(2*c**2)),
        'category': '高等函数'
    },
    '多项式函数': {
        'formula': 'f(x) = ax³ + bx² + cx + d',
        'description': '三次多项式函数，可以用来拟合曲线。',
        'params': {'a': 1, 'b': 0, 'c': 0, 'd': 0},
        'eval': lambda x, a, b, c, d: a * x**3 + b * x**2 + c * x + d,
        'category': '高等函数'
    }
}

@app.route('/')
def index():
    # 按类别组织函数
    categorized_functions = {}
    for name, info in functions.items():
        category = info.get('category', '其他')
        if category not in categorized_functions:
            categorized_functions[category] = {}
        categorized_functions[category][name] = info
    
    return render_template('index.html', 
                          functions=functions, 
                          categorized_functions=categorized_functions)

@app.route('/function/<func_name>')
def show_function(func_name):
    if func_name not in functions:
        return "函数不存在", 404
        
    func_info = functions[func_name]
    return render_template('function.html', 
                          name=func_name, 
                          info=func_info)

@app.route('/compare')
def compare_functions():
    return render_template('compare.html', functions=functions)

@app.route('/generate_plot', methods=['POST'])
def generate_plot():
    data = request.json
    func_name = data.get('function')
    params = data.get('params', {})
    
    if func_name not in functions:
        return jsonify({'error': '函数不存在'}), 400
    
    func_info = functions[func_name]
    func = func_info['eval']
    
    # 生成x值
    x = np.linspace(-10, 10, 1000)
    
    # 根据函数和参数计算y值
    try:
        y = func(x, **params)
    except Exception as e:
        return jsonify({'error': f'计算错误: {str(e)}'}), 400
    
    # 创建图形
    fig = Figure(figsize=(10, 6))
    axis = fig.add_subplot(1, 1, 1)
    
    # 绘制函数图像
    axis.plot(x, y)
    axis.grid(True)
    axis.axhline(y=0, color='k', linestyle='-', alpha=0.3)
    axis.axvline(x=0, color='k', linestyle='-', alpha=0.3)
    
    # 设置标题
    param_str = ', '.join([f"{k}={v}" for k, v in params.items()])
    axis.set_title(f"{func_name}: {func_info['formula']} ({param_str})")
    
    # 转换为base64图像
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    img_data = base64.b64encode(buf.getvalue()).decode('utf-8')
    
    return jsonify({'image': img_data})

@app.route('/compare_plot', methods=['POST'])
def compare_plot():
    data = request.json
    functions_to_compare = data.get('functions', [])
    
    if not functions_to_compare:
        return jsonify({'error': '未选择任何函数'}), 400
    
    # 创建图形
    fig = Figure(figsize=(12, 8))
    axis = fig.add_subplot(1, 1, 1)
    
    # 生成x值
    x = np.linspace(-10, 10, 1000)
    
    # 为每个函数绘制图像
    for func_data in functions_to_compare:
        func_name = func_data.get('name')
        params = func_data.get('params', {})
        
        if func_name not in functions:
            continue
        
        func_info = functions[func_name]
        func = func_info['eval']
        
        try:
            y = func(x, **params)
            param_str = ', '.join([f"{k}={v}" for k, v in params.items()])
            label = f"{func_name} ({param_str})"
            axis.plot(x, y, label=label)
        except Exception as e:
            continue
    
    axis.grid(True)
    axis.axhline(y=0, color='k', linestyle='-', alpha=0.3)
    axis.axvline(x=0, color='k', linestyle='-', alpha=0.3)
    axis.legend()
    axis.set_title('函数对比图')
    
    # 转换为base64图像
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    img_data = base64.b64encode(buf.getvalue()).decode('utf-8')
    
    return jsonify({'image': img_data})

@app.route('/export_image', methods=['POST'])
def export_image():
    data = request.json
    image_data = data.get('image_data', '')
    file_format = data.get('format', 'png')
    
    if not image_data:
        return jsonify({'error': '没有图像数据'}), 400
    
    # 移除base64前缀
    if ',' in image_data:
        image_data = image_data.split(',')[1]
    
    # 解码base64数据
    image_bytes = base64.b64decode(image_data)
    
    # 生成唯一文件名
    filename = f"function_plot_{datetime.now().strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex[:8]}.{file_format}"
    filepath = os.path.join('app/static/temp', filename)
    
    # 保存文件
    with open(filepath, 'wb') as f:
        f.write(image_bytes)
    
    # 返回文件URL
    file_url = f"/static/temp/{filename}"
    return jsonify({'file_url': file_url, 'filename': filename}) 