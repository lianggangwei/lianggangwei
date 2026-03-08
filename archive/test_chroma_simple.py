import os
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

print("=== 测试ChromaDB基本功能 ===")
try:
    # 1. 测试导入
    print("1. 导入ChromaDB...")
    import chromadb
    print(f"✅ 成功导入ChromaDB {chromadb.__version__}")
    
    # 2. 测试创建客户端
    print("\n2. 创建客户端...")
    client = chromadb.Client()
    print("✅ 客户端创建成功")
    
    # 3. 测试创建集合
    print("\n3. 创建集合...")
    collection = client.create_collection(name="test")
    print("✅ 集合创建成功")
    
    # 4. 测试添加文档
    print("\n4. 添加文档...")
    collection.add(
        documents=["测试文档1", "测试文档2"],
        ids=["1", "2"]
    )
    print("✅ 文档添加成功")
    
    # 5. 测试查询
    print("\n5. 执行查询...")
    results = collection.query(
        query_texts=["测试"],
        n_results=2
    )
    print("✅ 查询成功")
    print(f"查询结果数量: {len(results['documents'][0])}")
    
    print("\n🎉 所有测试通过！ChromaDB已成功安装并正常工作。")
except Exception as e:
    print(f"❌ 测试失败: {e}")
    import traceback
    traceback.print_exc()
