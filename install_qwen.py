
import subprocess
import sys
import os

def install_package(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

print("=" * 60)
print("Qwen 千问模型本地部署")
print("=" * 60)

print("\n1. 安装必要的依赖包...")
dependencies = [
    "transformers",
    "torch",
    "accelerate",
    "sentencepiece",
    "bitsandbytes"
]

for dep in dependencies:
    try:
        print(f"   安装 {dep}...")
        install_package(dep)
    except Exception as e:
        print(f"   ⚠️  {dep} 安装可能已存在或出错: {e}")

print("\n✅ 依赖安装完成！")
print("\n现在运行 'python qwen_demo.py' 来测试模型！")

