# 三菱梯形图工具

一个用于生成、解析和校验三菱梯形图的Python工具包，支持Web在线编辑和校验。

## 功能特性

- 📝 **梯形图生成**：支持通过代码或文本格式生成梯形图
- 🔍 **梯形图解析**：解析文本格式的梯形图代码
- ✅ **语法校验**：快速语法检查和完整程序校验
- 🖼️ **SVG可视化**：生成SVG格式的梯形图图形
- 💾 **JSON序列化**：支持程序的保存和加载
- 🌐 **Web界面**：美观的在线编辑器

## 安装

```bash
pip install -r requirements.txt
```

## 主要依赖：
- Flask (用于Web界面)

## 使用方法

### 1. 作为Python API使用

```python
from tools.plc import (
    LadderProgram, Rung, Contact, Coil, Position,
    LadderParser, LadderGenerator, LadderValidator
)

# 创建程序
program = LadderProgram(name="我的程序")

# 添加梯级
rung = Rung(number=1, comment="启动电路")
rung.add_element(Contact(address="X0", position=Position(row=1, column=0)))
rung.add_element(Coil(address="Y0", position=Position(row=1, column=1)))
program.add_rung(rung)

# 生成文本
text = LadderGenerator.generate_text(program)
print(text)

# 校验程序
validator = LadderValidator()
valid, errors, warnings = validator.validate(program)
```

### 2. 运行示例程序

```bash
python tools/plc/examples.py
```

### 3. 启动Web服务器

```bash
python tools/plc/web_ui.py
```

然后在浏览器访问 http://localhost:5000

## 支持的指令

### 基础指令：
- `LD X0` - 加载常开触点
- `LDI X1` - 加载常闭触点
- `OUT Y0` - 输出线圈
- `SET Y0` - 置位线圈
- `RST Y0` - 复位线圈

### 定时器：
- `TON T0 100` - 通电延时定时器
- `TOF T1 50` - 断电延时定时器

### 计数器：
- `CTU C0 10` - 加计数器
- `CTD C1 5` - 减计数器

## 项目结构

```
tools/plc/
├── __init__.py          # 模块导出
├── elements.py           # 梯形图元素类
├── ladder.py            # 解析、生成和序列化
├── validator.py         # 校验器
├── web_ui.py          # Web界面
├── examples.py        # 示例程序
├── requirements.txt   # 依赖
└── README.md        # 本文档
```

## 许可证

MIT
