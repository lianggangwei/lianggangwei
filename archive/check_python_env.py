import sys
import os

print("=== Python环境信息 ===")
print(f"Python版本: {sys.version}")
print(f"Python路径: {sys.executable}")
print(f"Python版本信息: {sys.version_info}")
print(f"系统路径: {sys.path}")

print("\n=== 环境变量 ===")
print(f"PATH: {os.environ.get('PATH', '未设置')}")

print("\n=== 已安装的包 ===")
try:
    import pkg_resources
    for dist in pkg_resources.working_set:
        print(f"{dist.key}=={dist.version}")
except ImportError:
    print("无法获取已安装包信息")
