#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
静默安装ChromaDB及其依赖
所有操作后台自动完成，不需要用户交互
"""

import subprocess
import sys
import os

# 确保输出编码正确
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

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

def run_command(cmd, timeout=120):
    """运行命令并返回结果"""
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            shell=False
        )
        return result
    except Exception as e:
        return None

def install_package(package):
    """安装单个包（静默模式）"""
    print(f"正在安装 {package}...")
    # 使用静默参数安装包
    cmd = [sys.executable, "-m", "pip", "install", "-q", "--no-input", "--no-cache-dir", package]
    result = run_command(cmd)
    
    if result and result.returncode == 0:
        print(f"✓ {package} 安装成功")
        return True
    else:
        error_msg = result.stderr if result else "未知错误"
        print(f"✗ {package} 安装失败: {error_msg}")
        return False

def install_with_mirror(package):
    """使用国内镜像源安装包"""
    print(f"使用国内镜像源安装 {package}...")
    # 使用清华大学镜像源
    cmd = [sys.executable, "-m", "pip", "install", "-q", "--no-input", "--no-cache-dir", 
           "-i", "https://pypi.tuna.tsinghua.edu.cn/simple", package]
    result = run_command(cmd)
    
    if result and result.returncode == 0:
        print(f"✓ {package} 安装成功")
        return True
    else:
        error_msg = result.stderr if result else "未知错误"
        print(f"✗ {package} 安装失败: {error_msg}")
        return False

def main():
    print("=" * 80)
    print("ChromaDB静默安装脚本")
    print("所有操作将在后台自动完成，不需要用户交互")
    print("=" * 80)
    
    # 1. 升级pip
    print("\n1. 升级pip...")
    pip_upgrade = [sys.executable, "-m", "pip", "install", "-q", "--no-input", "--upgrade", "pip"]
    result = run_command(pip_upgrade)
    if result and result.returncode == 0:
        print("✓ pip 升级成功")
    else:
        print("⚠ pip 升级失败，继续安装依赖")
    
    # 2. 安装基础依赖
    print("\n2. 安装基础依赖...")
    success_count = 0
    failure_count = 0
    
    for package in dependencies:
        if install_package(package):
            success_count += 1
        else:
            # 尝试使用国内镜像源
            if install_with_mirror(package):
                success_count += 1
            else:
                failure_count += 1
    
    print(f"\n依赖安装完成: 成功 {success_count}, 失败 {failure_count}")
    
    # 3. 安装ChromaDB
    print("\n3. 安装ChromaDB...")
    chroma_installed = False
    
    # 尝试不同版本的ChromaDB
    chroma_versions = ["chromadb", "chromadb==1.0.0", "chromadb==0.4.0"]
    
    for version in chroma_versions:
        if install_with_mirror(version):
            chroma_installed = True
            break
    
    if chroma_installed:
        print("\n✓ ChromaDB 安装成功！")
    else:
        print("\n✗ ChromaDB 安装失败")
    
    # 4. 验证安装
    print("\n4. 验证安装...")
    try:
        # 导入测试
        import chromadb
        version = chromadb.__version__
        print(f"✓ 成功导入ChromaDB {version}")
        
        # 测试基本功能
        from chromadb.api.types import EmbeddingFunction, Documents, Embeddings
        
        class SimpleEmbeddingFunction(EmbeddingFunction):
            def __call__(self, input: Documents) -> Embeddings:
                return [[len(doc)] * 3 for doc in input]
        
        # 创建客户端和集合
        client = chromadb.Client()
        collection = client.create_collection(
            name="test_collection",
            embedding_function=SimpleEmbeddingFunction()
        )
        
        # 添加文档
        collection.add(
            documents=["测试文档1", "测试文档2"],
            ids=["1", "2"]
        )
        
        # 执行查询
        results = collection.query(
            query_texts=["测试"],
            n_results=1
        )
        
        # 删除集合
        client.delete_collection(name="test_collection")
        
        print("✓ ChromaDB 功能测试通过")
        
    except Exception as e:
        print(f"✗ 验证失败: {e}")
        print("可能需要使用猴子补丁来解决Pydantic V1兼容性问题")
    
    print("\n" + "=" * 80)
    print("静默安装完成！")
    print("所有操作已在后台自动执行，不需要用户干预")
    print("=" * 80)

if __name__ == "__main__":
    main()
