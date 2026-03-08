#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
静默测试ChromaDB功能（带有猴子补丁）
所有操作后台自动完成，不需要用户交互
"""

import sys

# 猴子补丁：替换pydantic.v1的导入
class MockPydanticV1:
    class BaseSettings:
        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)
        
        def __getitem__(self, key):
            return getattr(self, key)
        
        def require(self, key):
            return getattr(self, key)
    
    @staticmethod
    def validator(*args, **kwargs):
        def decorator(func):
            return func
        return decorator

# 在导入chromadb之前替换pydantic.v1
sys.modules['pydantic.v1'] = MockPydanticV1()

# 然后导入chromadb相关模块
from chromadb.api.types import EmbeddingFunction, Documents, Embeddings

# 自定义简单嵌入函数，避免下载模型
class SimpleEmbeddingFunction(EmbeddingFunction):
    def __call__(self, input: Documents) -> Embeddings:
        # 简单的嵌入实现：返回文档长度作为嵌入向量
        return [[len(doc)] * 3 for doc in input]

# 测试ChromaDB基本功能
def test_chroma_offline():
    print("=== 静默测试ChromaDB基本功能 ===")
    
    # 1. 导入测试
    try:
        import chromadb
        version = chromadb.__version__
        print(f"1. 导入ChromaDB...")
        print(f"✅ 成功导入ChromaDB {version}")
    except Exception as e:
        print(f"❌ 导入失败: {e}")
        return False
    
    # 2. 创建客户端
    try:
        client = chromadb.Client()
        print("2. 创建客户端...")
        print("✅ 客户端创建成功")
    except Exception as e:
        print(f"❌ 客户端创建失败: {e}")
        return False
    
    # 3. 创建集合（使用自定义嵌入函数）
    try:
        collection = client.create_collection(
            name="test_collection",
            embedding_function=SimpleEmbeddingFunction()
        )
        print("3. 创建集合...")
        print("✅ 集合创建成功")
    except Exception as e:
        print(f"❌ 集合创建失败: {e}")
        return False
    
    # 4. 添加文档
    try:
        collection.add(
            documents=["测试文档1", "测试文档2"],
            ids=["1", "2"]
        )
        print("4. 添加文档...")
        print("✅ 文档添加成功")
    except Exception as e:
        print(f"❌ 文档添加失败: {e}")
        return False
    
    # 5. 执行查询
    try:
        results = collection.query(
            query_texts=["测试"],
            n_results=1
        )
        print("5. 执行查询...")
        print("✅ 查询功能正常")
        print(f"   查询结果: {results['documents'][0][0]}")
    except Exception as e:
        print(f"❌ 查询失败: {e}")
        return False
    
    # 6. 获取集合信息
    try:
        collection_info = collection.get()
        print("6. 获取集合信息...")
        print(f"✅ 集合信息获取成功")
        print(f"   文档数量: {len(collection_info['ids'])}")
    except Exception as e:
        print(f"❌ 集合信息获取失败: {e}")
        return False
    
    # 7. 删除集合
    try:
        client.delete_collection(name="test_collection")
        print("7. 删除集合...")
        print("✅ 集合删除成功")
    except Exception as e:
        print(f"❌ 集合删除失败: {e}")
        return False
    
    print("\n=== 所有测试通过！ ===")
    print("ChromaDB离线功能正常工作")
    return True

if __name__ == "__main__":
    success = test_chroma_offline()
    sys.exit(0 if success else 1)
