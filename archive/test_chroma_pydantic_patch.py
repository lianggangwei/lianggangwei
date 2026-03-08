import os
import sys

# 猴子补丁：替换pydantic.v1的导入
class MockPydanticV1:
    class BaseSettings:
        pass
    
    @staticmethod
    def validator(*args, **kwargs):
        def decorator(func):
            return func
        return decorator

# 在导入chromadb之前替换pydantic.v1
sys.modules['pydantic.v1'] = MockPydanticV1()

print("=== 测试ChromaDB基本功能（Pydantic补丁）===")
try:
    # 尝试导入chromadb
    import chromadb
    print("1. 测试导入:")
    print(f"ChromaDB版本: {chromadb.__version__}")
    
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
    
    print("\n=== 测试完成 ===")
except Exception as e:
    print(f"❌ 测试失败: {e}")
    import traceback
    traceback.print_exc()
