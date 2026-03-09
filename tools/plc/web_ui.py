from flask import Flask, render_template_string, request, jsonify
import sys
import os

project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from tools.plc.elements import LadderProgram, Rung, Contact, Coil, Timer, Counter, Position
from tools.plc.ladder import LadderParser, LadderGenerator, LadderSerializer
from tools.plc.validator import LadderValidator, QuickValidator

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>三菱梯形图编辑器</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }
        .header {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            color: white;
            padding: 25px 30px;
        }
        .header h1 {
            font-size: 28px;
            margin-bottom: 5px;
        }
        .header p {
            opacity: 0.8;
            font-size: 14px;
        }
        .main-content {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            padding: 30px;
        }
        .section {
            background: #f8f9fa;
            border-radius: 8px;
            padding: 20px;
        }
        .section h2 {
            color: #1a1a2e;
            margin-bottom: 15px;
            font-size: 18px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .editor-container {
            display: flex;
            flex-direction: column;
            height: 400px;
        }
        textarea {
            flex: 1;
            width: 100%;
            padding: 15px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-family: 'Consolas', 'Monaco', monospace;
            font-size: 14px;
            resize: none;
            background: #1e1e1e;
            color: #d4d4d4;
        }
        textarea:focus {
            outline: none;
            border-color: #667eea;
        }
        .buttons {
            display: flex;
            gap: 10px;
            margin-top: 15px;
            flex-wrap: wrap;
        }
        button {
            padding: 12px 24px;
            border: none;
            border-radius: 6px;
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        .btn-primary {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }
        .btn-success {
            background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
            color: white;
        }
        .btn-success:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(17, 153, 142, 0.4);
        }
        .btn-info {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
        }
        .btn-info:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(245, 87, 108, 0.4);
        }
        .output {
            background: white;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            padding: 15px;
            min-height: 200px;
            max-height: 400px;
            overflow-y: auto;
            font-family: 'Consolas', 'Monaco', monospace;
            font-size: 13px;
            white-space: pre-wrap;
        }
        .error {
            color: #e74c3c;
            background: #fee;
            padding: 8px 12px;
            border-radius: 4px;
            margin: 5px 0;
            border-left: 4px solid #e74c3c;
        }
        .warning {
            color: #f39c12;
            background: #fff3cd;
            padding: 8px 12px;
            border-radius: 4px;
            margin: 5px 0;
            border-left: 4px solid #f39c12;
        }
        .success {
            color: #27ae60;
            background: #d4edda;
            padding: 8px 12px;
            border-radius: 4px;
            margin: 5px 0;
            border-left: 4px solid #27ae60;
        }
        .info {
            color: #3498db;
            background: #d1ecf1;
            padding: 8px 12px;
            border-radius: 4px;
            margin: 5px 0;
            border-left: 4px solid #3498db;
        }
        @media (max-width: 900px) {
            .main-content {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>⚡ 三菱梯形图在线编辑器</h1>
            <p>支持梯形图解析、生成和在线校验</p>
        </div>
        <div class="main-content">
            <div class="section">
                <h2>📝 梯形图代码编辑器</h2>
                <div class="editor-container">
                    <textarea id="editor" placeholder="// 在这里输入三菱梯形图代码...
// 示例:
// RUNG 1 启动逻辑
// LD X0
// OUT Y0

RUNG 1 启动电路
LD X0
OUT Y0

RUNG 2 自锁电路
LD X0
OR Y0
ANI X1
OUT Y0

RUNG 3 定时器示例
LD X2
TON T0 100"></textarea>
                </div>
                <div class="buttons">
                    <button class="btn-primary" onclick="quickValidate()">⚡ 快速校验</button>
                    <button class="btn-success" onclick="fullValidate()">✅ 完整校验</button>
                    <button class="btn-info" onclick="generateSVG()">🖼️ 生成SVG</button>
                    <button class="btn-info" onclick="loadExample1()">📋 示例1</button>
                    <button class="btn-info" onclick="loadExample2()">📋 示例2</button>
                </div>
            </div>
            <div class="section">
                <h2>📊 输出结果</h2>
                <div id="output" class="output">欢迎使用三菱梯形图编辑器！
请在左侧输入代码，然后点击相应按钮进行操作。</div>
            </div>
        </div>
    </div>

    <script>
        function quickValidate() {
            const code = document.getElementById('editor').value;
            fetch('/quick_validate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ code: code })
            })
            .then(response => response.json())
            .then(data => {
                let output = '';
                if (data.valid) {
                    output += '<div class="success">✅ 语法检查通过！</div>';
                } else {
                    output += '<div class="error">❌ 发现错误：</div>';
                    data.errors.forEach(err => {
                        output += '<div class="error">' + err + '</div>';
                    });
                }
                document.getElementById('output').innerHTML = output;
            });
        }

        function fullValidate() {
            const code = document.getElementById('editor').value;
            fetch('/full_validate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ code: code })
            })
            .then(response => response.json())
            .then(data => {
                let output = '';
                if (data.valid) {
                    output += '<div class="success">✅ 完整校验通过！</div>';
                } else {
                    output += '<div class="error">❌ 发现错误：</div>';
                }
                
                if (data.errors && data.errors.length > 0) {
                    output += '<div style="margin-top:10px;"><strong>错误：</strong></div>';
                    data.errors.forEach(err => {
                        output += '<div class="error">' + err + '</div>';
                    });
                }
                
                if (data.warnings && data.warnings.length > 0) {
                    output += '<div style="margin-top:10px;"><strong>警告：</strong></div>';
                    data.warnings.forEach(warn => {
                        output += '<div class="warning">' + warn + '</div>';
                    });
                }
                
                if (data.generated_code) {
                    output += '<div style="margin-top:15px;"><strong>生成的代码：</strong></div>';
                    output += '<div class="info">' + escapeHtml(data.generated_code) + '</div>';
                }
                
                document.getElementById('output').innerHTML = output;
            });
        }

        function generateSVG() {
            const code = document.getElementById('editor').value;
            fetch('/generate_svg', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ code: code })
            })
            .then(response => response.json())
            .then(data => {
                let output = '';
                if (data.svg) {
                    output += '<div class="success">✅ SVG生成成功！</div>';
                    output += '<div style="margin-top:10px; overflow:auto;">' + data.svg + '</div>';
                } else if (data.error) {
                    output += '<div class="error">❌ ' + data.error + '</div>';
                }
                document.getElementById('output').innerHTML = output;
            });
        }

        function loadExample1() {
            document.getElementById('editor').value = '// 示例1：简单的启动停止电路\nRUNG 1 启动停止\nLD X0\nOR Y0\nANI X1\nOUT Y0\n\nRUNG 2 运行指示\nLD Y0\nOUT Y1';
        }

        function loadExample2() {
            document.getElementById('editor').value = '// 示例2：定时器和计数器\nRUNG 1 定时器启动\nLD X0\nTON T0 50\n\nRUNG 2 定时器输出\nLD T0\nOUT Y0\n\nRUNG 3 计数器\nLD X1\nCTU C0 10\n\nRUNG 4 计数器输出\nLD C0\nOUT Y1';
        }

        function escapeHtml(text) {
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }
    </script>
</body>
</html>
"""


@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)


@app.route('/quick_validate', methods=['POST'])
def quick_validate():
    data = request.json
    code = data.get('code', '')
    
    try:
        valid, errors = QuickValidator.quick_validate_text(code)
        return jsonify({
            'valid': valid,
            'errors': errors
        })
    except Exception as e:
        return jsonify({
            'valid': False,
            'errors': [str(e)]
        })


@app.route('/full_validate', methods=['POST'])
def full_validate():
    data = request.json
    code = data.get('code', '')
    
    try:
        program, parse_errors = LadderParser.parse_text(code)
        
        if parse_errors:
            return jsonify({
                'valid': False,
                'errors': parse_errors,
                'warnings': []
            })
        
        validator = LadderValidator()
        valid, errors, warnings = validator.validate(program)
        
        generated_code = LadderGenerator.generate_text(program)
        
        return jsonify({
            'valid': valid,
            'errors': [str(e) for e in errors],
            'warnings': [str(w) for w in warnings],
            'generated_code': generated_code
        })
    except Exception as e:
        return jsonify({
            'valid': False,
            'errors': [str(e)],
            'warnings': []
        })


@app.route('/generate_svg', methods=['POST'])
def generate_svg():
    data = request.json
    code = data.get('code', '')
    
    try:
        program, parse_errors = LadderParser.parse_text(code)
        
        if parse_errors:
            return jsonify({
                'error': '解析错误: ' + ', '.join(parse_errors)
            })
        
        svg = LadderGenerator.generate_svg(program)
        
        return jsonify({
            'svg': svg
        })
    except Exception as e:
        return jsonify({
            'error': str(e)
        })


def start_server():
    print("🚀 启动三菱梯形图编辑器服务器...")
    print("📖 访问地址: http://localhost:5000")
    print("⚡ 按 Ctrl+C 停止服务器")
    print("=" * 50)
    app.run(host='0.0.0.0', port=5000, debug=False)


if __name__ == '__main__':
    start_server()
