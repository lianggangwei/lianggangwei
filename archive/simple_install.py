import subprocess
import sys

# 安装单个包的函数
def install_package(package):
    try:
        # 使用--no-cache-dir避免缓存问题，添加静默安装参数
        cmd = [sys.executable, "-m", "pip", "install", "-q", "--no-input", package, "--no-cache-dir"]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if result.returncode == 0:
            print(f"✓ {package} 安装成功")
            return True
        else:
            print(f"✗ {package} 安装失败: {result.stderr}")
            return False
    except Exception as e:
        print(f"✗ {package} 安装异常: {e}")
        return False

# 安装依赖
def main():
    print("开始安装基础依赖...")
    
    # 安装基础依赖
    base_deps = ["numpy", "pydantic"]
    for dep in base_deps:
        install_package(dep)
    
    print("\n尝试安装 ChromaDB...")
    # 尝试安装不同版本的ChromaDB
    chroma_versions = ["chromadb==1.0.0", "chromadb==0.4.0"]
    
    installed = False
    for version in chroma_versions:
        if install_package(version):
            installed = True
            break
    
    if installed:
        print("\nChromaDB 安装成功！")
    else:
        print("\nChromaDB 安装失败，可能是因为Python 3.14.3版本太新，不兼容。")

if __name__ == "__main__":
    main()