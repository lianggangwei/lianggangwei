
import sys
import numpy as np

def init_chromadb():
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

def get_chroma_client(persist_directory=None):
    init_chromadb()
    import chromadb
    
    if persist_directory:
        return chromadb.PersistentClient(path=persist_directory)
    else:
        return chromadb.Client()

class SimpleEmbeddingGenerator:
    def __init__(self, dimension=128):
        self.dimension = dimension
    
    def _text_to_hash(self, text):
        hash_val = 0
        for char in text:
            hash_val = (hash_val * 31 + ord(char)) % (2**32)
        return hash_val
    
    def generate_embedding(self, text):
        embedding = np.zeros(self.dimension, dtype=np.float32)
        
        words = text.lower().split()
        for i, word in enumerate(words):
            word_hash = self._text_to_hash(word)
            pos = i % self.dimension
            embedding[pos] = embedding[pos] + (word_hash % 1000) / 1000.0
        
        norm = np.linalg.norm(embedding)
        if norm > 0:
            embedding = embedding / norm
        
        return embedding.tolist()
    
    def generate_embeddings(self, texts):
        return [self.generate_embedding(text) for text in texts]

class KnowledgeBase:
    def __init__(self, name, persist_directory=None, embedding_dim=128):
        self.name = name
        self.client = get_chroma_client(persist_directory)
        self.embedding_generator = SimpleEmbeddingGenerator(embedding_dim)
        
        try:
            self.collection = self.client.get_collection(name=name)
        except:
            self.collection = self.client.create_collection(name=name)
    
    def add_documents(self, documents, ids=None, metadatas=None):
        if ids is None:
            import uuid
            ids = [str(uuid.uuid4()) for _ in documents]
        
        embeddings = self.embedding_generator.generate_embeddings(documents)
        
        self.collection.add(
            documents=documents,
            embeddings=embeddings,
            ids=ids,
            metadatas=metadatas
        )
    
    def add_document(self, document, id=None, metadata=None):
        if id is None:
            import uuid
            id = str(uuid.uuid4())
        
        embedding = self.embedding_generator.generate_embedding(document)
        
        self.collection.add(
            documents=[document],
            embeddings=[embedding],
            ids=[id],
            metadatas=[metadata] if metadata else None
        )
        
        return id
    
    def query(self, query_text, n_results=5, where=None):
        query_embedding = self.embedding_generator.generate_embedding(query_text)
        
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            where=where
        )
        
        return results
    
    def get_all_documents(self):
        return self.collection.get()
    
    def update_document(self, id, document=None, metadata=None):
        update_kwargs = {"ids": [id]}
        
        if document is not None:
            embedding = self.embedding_generator.generate_embedding(document)
            update_kwargs["documents"] = [document]
            update_kwargs["embeddings"] = [embedding]
        
        if metadata is not None:
            update_kwargs["metadatas"] = [metadata]
        
        self.collection.update(**update_kwargs)
    
    def delete_document(self, id):
        self.collection.delete(ids=[id])
    
    def delete_documents(self, ids):
        self.collection.delete(ids=ids)
    
    def count(self):
        return self.collection.count()
    
    def delete(self):
        self.client.delete_collection(name=self.name)

def batch_add_documents(kb, documents, batch_size=100):
    for i in range(0, len(documents), batch_size):
        batch = documents[i:i + batch_size]
        
        contents = [doc['content'] for doc in batch]
        ids = [doc.get('id') for doc in batch]
        metadatas = [doc.get('metadata') for doc in batch]
        
        kb.add_documents(contents, ids=ids, metadatas=metadatas)

