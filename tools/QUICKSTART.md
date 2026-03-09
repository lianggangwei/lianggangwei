# 自动化工具包 - 快速入门

## 第一步：安装依赖

```bash
cd tools
pip install -r requirements.txt
```

## 第二步：运行示例

### 1. 网页自动化示例
```bash
cd examples
python web_scraper_example.py
```

### 2. 数据处理示例
```bash
python data_example.py
```

### 3. AI工具示例
```bash
python ai_example.py
```

### 4. 系统工具示例
```bash
python system_example.py
```

## 功能模块详解

### 🕸️ 网页自动化 (web/)
- **scraper.py** - 网络爬虫、数据抓取
- **browser.py** - Playwright浏览器自动化

### 📊 数据处理 (data/)
- **excel.py** - Excel文件读写、格式化
- **csv_tool.py** - CSV文件处理、转换
- **database.py** - SQLite/SQLAlchemy数据库操作

### 🤖 AI工具 (ai/)
- **api_client.py** - OpenAI API客户端封装
- **local_llm.py** - Ollama本地模型支持

### 🔧 系统工具 (system/)
- **file_ops.py** - 文件管理、查找、去重
- **backup.py** - 数据备份、恢复

## 常用代码片段

### 网页抓取
```python
from web.scraper import WebScraper
scraper = WebScraper("https://example.com")
data = scraper.scrape_single_page("https://example.com")
print(data['title'])
```

### Excel处理
```python
from data.excel import ExcelTool
import pandas as pd
excel = ExcelTool('data.xlsx')
df = pd.DataFrame({'name': ['张三', '李四'], 'age': [25, 30]})
excel.write_excel(df, '人员信息')
```

### 数据库操作
```python
from data.database import SQLiteTool
with SQLiteTool('mydb.db') as db:
    db.create_table('users', {'id': 'INTEGER PRIMARY KEY', 'name': 'TEXT'})
    db.insert('users', {'name': '张三'})
    users = db.query('SELECT * FROM users')
```

### 文件管理
```python
from system.file_ops import FileManager
fm = FileManager('.')
py_files = fm.list_files('*.py', recursive=True)
print(f"找到 {len(py_files)} 个Python文件")
```

### 数据备份
```python
from system.backup import BackupTool
backup = BackupTool('.', 'backups')
zip_path = backup.backup_to_zip(exclude_patterns=['venv'])
print(f"备份已创建: {zip_path}")
```
