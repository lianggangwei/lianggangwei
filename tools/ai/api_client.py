import os
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

load_dotenv()


class OpenAIClient:
    def __init__(self, api_key: str = None, base_url: str = None):
        try:
            from openai import OpenAI
            self.api_key = api_key or os.getenv('OPENAI_API_KEY')
            self.base_url = base_url or os.getenv('OPENAI_BASE_URL')
            self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)
        except ImportError:
            print("请先安装: pip install openai")
            raise

    def chat(self, messages: List[Dict[str, str]], model: str = 'gpt-3.5-turbo',
             temperature: float = 0.7, max_tokens: int = 1000, stream: bool = False):
        response = self.client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=stream
        )
        if stream:
            return response
        return response.choices[0].message.content

    def simple_chat(self, prompt: str, system_prompt: str = '你是一个有用的助手', **kwargs):
        messages = [
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': prompt}
        ]
        return self.chat(messages, **kwargs)

    def generate_embedding(self, text: str, model: str = 'text-embedding-ada-002'):
        response = self.client.embeddings.create(input=text, model=model)
        return response.data[0].embedding


class MultiAIClient:
    def __init__(self):
        self.clients = {}
        self.load_clients()

    def load_clients(self):
        if os.getenv('OPENAI_API_KEY'):
            self.clients['openai'] = OpenAIClient()

    def add_client(self, name: str, client):
        self.clients[name] = client

    def chat(self, prompt: str, provider: str = 'openai', **kwargs):
        if provider not in self.clients:
            raise ValueError(f"Provider {provider} not available. Available: {list(self.clients.keys())}")
        return self.clients[provider].simple_chat(prompt, **kwargs)


def chat_with_ai(prompt: str, api_key: str = None, base_url: str = None, **kwargs):
    client = OpenAIClient(api_key=api_key, base_url=base_url)
    return client.simple_chat(prompt, **kwargs)


def create_chat_template(system_prompt: str, examples: List[Dict[str, str]] = None):
    messages = [{'role': 'system', 'content': system_prompt}]
    if examples:
        for ex in examples:
            messages.append({'role': 'user', 'content': ex['user']})
            messages.append({'role': 'assistant', 'content': ex['assistant']})
    return messages
