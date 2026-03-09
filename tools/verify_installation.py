import sys
import os

print("=== 自动化工具包 - 安装验证 ===\n")

modules_to_check = [
    ('requests', '网页请求'),
    ('bs4', 'BeautifulSoup网页解析'),
    ('lxml', 'XML/HTML解析'),
    ('playwright', '浏览器自动化'),
    ('selenium', 'Selenium浏览器'),
    ('pandas', '数据处理'),
    ('openpyxl', 'Excel处理'),
    ('xlrd', 'Excel读取'),
    ('sqlalchemy', '数据库ORM'),
    ('openai', 'OpenAI API'),
    ('ollama', 'Ollama本地模型'),
    ('dotenv', '环境变量管理'),
    ('tqdm', '进度条'),
    ('rich', '终端美化'),
]

all_ok = True
for module, description in modules_to_check:
    try:
        __import__(module)
        print(f"✅ {description}: {module} 已安装")
    except ImportError:
        print(f"❌ {description}: {module} 未安装")
        all_ok = False

print("\n=== 检查Playwright浏览器 ===")
try:
    from playwright.sync_api import sync_playwright
    print("✅ Playwright Python包已安装")
except Exception as e:
    print(f"❌ Playwright检查失败: {e}")

print("\n" + "="*50)
if all_ok:
    print("🎉 所有依赖包安装成功！")
else:
    print("⚠️  部分依赖包未安装")
print("="*50)
