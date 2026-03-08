import sys
print("Python sys.path:")
for path in sys.path:
    print(f"- {path}")

# 检查用户站点目录是否在sys.path中
user_site = r"C:\Users\Administrator\AppData\Roaming\Python\Python314\site-packages"
if user_site in sys.path:
    print("\nUser site directory is in sys.path")
else:
    print("\nUser site directory is NOT in sys.path")
    print("Adding user site directory to sys.path...")
    sys.path.append(user_site)
    print("User site directory added to sys.path")

# 尝试导入chromadb
try:
    import chromadb
    print("\nChromaDB is installed!")
    print(f"ChromaDB version: {chromadb.__version__}")
except ImportError:
    print("\nChromaDB is not installed.")
except Exception as e:
    print(f"\nError: {e}")