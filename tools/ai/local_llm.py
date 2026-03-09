import subprocess
import json
from typing import List, Dict, Any, Optional, Generator
import os


class OllamaClient:
    def __init__(self, base_url: str = 'http://localhost:11434'):
        self.base_url = base_url.rstrip('/')
        self.available = self._check_available()

    def _check_available(self) -> bool:
        try:
            import requests
            response = requests.get(f"{self.base_url}/api/tags", timeout=2)
            return response.status_code == 200
        except:
            return False

    def list_models(self) -> List[str]:
        if not self.available:
            return []
        try:
            import requests
            response = requests.get(f"{self.base_url}/api/tags")
            data = response.json()
            return [model['name'] for model in data.get('models', [])]
        except:
            return []

    def pull_model(self, model_name: str) -> bool:
        try:
            import requests
            response = requests.post(
                f"{self.base_url}/api/pull",
                json={'name': model_name},
                stream=True
            )
            for line in response.iter_lines():
                if line:
                    print(json.loads(line.decode()).get('status', ''))
            return True
        except Exception as e:
            print(f"拉取模型失败: {e}")
            return False

    def chat(self, model: str, prompt: str, system_prompt: str = None,
             temperature: float = 0.7, stream: bool = False):
        if not self.available:
            raise RuntimeError("Ollama服务不可用，请确保已启动Ollama")
        try:
            import requests
            messages = []
            if system_prompt:
                messages.append({'role': 'system', 'content': system_prompt})
            messages.append({'role': 'user', 'content': prompt})
            data = {
                'model': model,
                'messages': messages,
                'stream': stream,
                'options': {'temperature': temperature}
            }
            if stream:
                return self._chat_stream(model, prompt, system_prompt, temperature)
            response = requests.post(f"{self.base_url}/api/chat", json=data)
            result = response.json()
            return result['message']['content']
        except Exception as e:
            raise RuntimeError(f"聊天失败: {e}")

    def _chat_stream(self, model: str, prompt: str, system_prompt: str = None,
                     temperature: float = 0.7) -> Generator[str, None, None]:
        import requests
        messages = []
        if system_prompt:
            messages.append({'role': 'system', 'content': system_prompt})
        messages.append({'role': 'user', 'content': prompt})
        data = {
            'model': model,
            'messages': messages,
            'stream': True,
            'options': {'temperature': temperature}
        }
        response = requests.post(f"{self.base_url}/api/chat", json=data, stream=True)
        for line in response.iter_lines():
            if line:
                chunk = json.loads(line.decode())
                if 'message' in chunk and 'content' in chunk['message']:
                    yield chunk['message']['content']

    def generate_embedding(self, model: str, text: str) -> List[float]:
        if not self.available:
            raise RuntimeError("Ollama服务不可用")
        try:
            import requests
            response = requests.post(
                f"{self.base_url}/api/embeddings",
                json={'model': model, 'prompt': text}
            )
            result = response.json()
            return result['embedding']
        except Exception as e:
            raise RuntimeError(f"生成嵌入失败: {e}")


def check_ollama_installed() -> bool:
    try:
        result = subprocess.run(['ollama', '--version'], capture_output=True, text=True)
        return result.returncode == 0
    except:
        return False


def install_ollama_guide():
    print("Ollama 安装指南:")
    print("1. Windows: 下载 https://ollama.com/download/windows")
    print("2. macOS: brew install ollama 或下载 https://ollama.com/download/macos")
    print("3. Linux: curl -fsSL https://ollama.com/install.sh | sh")
    print("\n安装后运行: ollama serve")


class SimpleLocalLLM:
    def __init__(self, use_ollama: bool = True):
        self.use_ollama = use_ollama
        if use_ollama:
            self.client = OllamaClient()

    def chat(self, prompt: str, model: str = 'llama2', **kwargs):
        if self.use_ollama and self.client.available:
            return self.client.chat(model, prompt, **kwargs)
        else:
            return f"本地模型不可用。这是对 '{prompt}' 的模拟响应。"
