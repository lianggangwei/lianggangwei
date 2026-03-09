import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ai.local_llm import OllamaClient, check_ollama_installed, install_ollama_guide


def example_ollama_check():
    print("=== Ollama检查示例 ===")
    if check_ollama_installed():
        print("Ollama已安装！")
        client = OllamaClient()
        if client.available:
            print("Ollama服务正在运行")
            models = client.list_models()
            print(f"可用模型: {models}")
        else:
            print("Ollama服务未运行，请运行: ollama serve")
    else:
        print("Ollama未安装")
        install_ollama_guide()
    print()


def example_simple_chat():
    print("=== AI聊天示例 ===")
    print("注意: 此示例需要Ollama或OpenAI API密钥")
    print("提示: 如果没有API，可以安装Ollama使用本地模型")
    print()


if __name__ == "__main__":
    try:
        example_ollama_check()
        example_simple_chat()
        print("AI示例运行完成！")
    except Exception as e:
        print(f"示例运行出错: {e}")
