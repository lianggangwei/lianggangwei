
import subprocess
import sys

print("=" * 60)
print("安装 ModelScope（阿里云模型库）")
print("=" * 60)

def install_package(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package, "-i", "https://pypi.tuna.tsinghua.edu.cn/simple"])

print("\n正在安装 ModelScope...")
try:
    install_package("modelscope")
    print("✅ ModelScope 安装成功！")
except Exception as e:
    print(f"❌ 安装失败: {e}")

