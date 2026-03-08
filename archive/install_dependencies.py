import subprocess
import sys

# 依赖包列表
dependencies = [
    "numpy",
    "pydantic",
    "uvicorn",
    "build",
    "pybase64",
    "posthog",
    "typing-extensions",
    "onnxruntime",
    "opentelemetry-api",
    "opentelemetry-exporter-otlp-proto-grpc",
    "opentelemetry-sdk",
    "tokenizers",
    "pypika",
    "tqdm",
    "overrides",
    "importlib-resources"
]

def install_package(package):
    """安装单个包"""
    try:
        print(f"正在安装 {package}...")
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "-q", "--no-input", package],
            capture_output=True,
            text=True,
            timeout=60
        )
        if result.returncode == 0:
            print(f"✓ {package} 安装成功")
            return True
        else:
            print(f"✗ {package} 安装失败: {result.stderr}")
            return False
    except Exception as e:
        print(f"✗ {package} 安装异常: {e}")
        return False

def main():
    print("开始安装依赖包...")
    print("=" * 60)
    
    success_count = 0
    failure_count = 0
    
    for package in dependencies:
        if install_package(package):
            success_count += 1
        else:
            failure_count += 1
        print()
    
    print("=" * 60)
    print(f"依赖安装完成: 成功 {success_count}, 失败 {failure_count}")
    
    # 尝试安装chromadb
    print("\n尝试安装 ChromaDB...")
    if install_package("chromadb==1.0.0"):
        print("✓ ChromaDB 安装成功")
    else:
        print("✗ ChromaDB 安装失败")
        print("尝试安装较老版本的 ChromaDB...")
        if install_package("chromadb==0.4.0"):
            print("✓ ChromaDB 0.4.0 安装成功")
        else:
            print("✗ ChromaDB 0.4.0 安装失败")

if __name__ == "__main__":
    main()