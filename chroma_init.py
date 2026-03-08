
import sys

def init_chromadb():
    """
    初始化ChromaDB环境，解决Python 3.14与Pydantic V1的兼容性问题
    
    用法：
        from chroma_init import init_chromadb
        init_chromadb()
        import chromadb
    """
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
    
    sys.modules['pydantic.v1'] = MockPydanticV1()

def get_chroma_client():
    """
    获取ChromaDB客户端的便捷函数
    
    返回：
        chromadb.Client实例
    """
    init_chromadb()
    import chromadb
    return chromadb.Client()

def create_simple_collection(client, name):
    """
    创建一个简单的集合并返回
    
    参数：
        client: ChromaDB客户端实例
        name: 集合名称
    
    返回：
        Collection实例
    """
    return client.create_collection(name=name)

