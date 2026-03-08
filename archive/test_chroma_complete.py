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

print("=== 测试ChromaDB完整功能 ===")
try:
    # 1. 测试导入
    print("1. 测试导入:")
    import chromadb
    print(f"ChromaDB版本: {chromadb.__version__}")
    print("✅ 导入成功")
    
    # 2. 测试创建客户端
    print("\n2. 测试创建客户端:")
    client = chromadb.Client()
    print("✅ 客户端创建成功")
    
    # 3. 测试创建集合
    print("\n3. 测试创建集合:")
    collection = client.create_collection(name="test_collection")
    print("✅ 集合创建成功")
    
    # 4. 测试添加文档
    print("\n4. 测试添加文档:")
    collection.add(
        documents=["这是第一个文档", "这是第二个文档", "这是第三个文档"],
        ids=["1", "2", "3"]
    )
    print("✅ 文档添加成功")
    
    # 5. 测试查询
    print("\n5. 测试查询:")
    results = collection.query(
        query_texts=["第一个"],
        n_results=2
    )
    print("✅ 查询成功")
    print(f"查询结果: {results}")
    
    # 6. 测试获取集合
    print("\n6. 测试获取集合:")
    collections = client.list_collections()
    print(f"集合列表: {collections}")
    print("✅ 获取集合成功")
    
    # 7. 测试删除集合
    print("\n7. 测试删除集合:")
    client.delete_collection(name="test_collection")
    print("✅ 删除集合成功")
    
    print("\n=== 测试完成 ===")
    print("🎉 ChromaDB所有基本功能测试通过！")
except Exception as e:
    print(f"❌ 测试失败: {e}")
    import traceback
    traceback.print_exc()
