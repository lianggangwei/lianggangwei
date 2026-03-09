
import os
import json
from datetime import datetime
from typing import List, Dict, Any, Optional

HAS_CHROMADB = False
try:
    import sys
    import warnings
    warnings.filterwarnings('ignore', category=UserWarning)
    import chromadb
    from chromadb.config import Settings
    HAS_CHROMADB = True
except Exception as e:
    HAS_CHROMADB = False
    print(f"⚠️ ChromaDB 不可用: {e}")
    print("   使用 JSON 存储模式")

class LongTermMemory:
    def __init__(self, persist_directory: str = "./memory_db"):
        self.persist_directory = persist_directory
        os.makedirs(persist_directory, exist_ok=True)
        
        self.use_chromadb = HAS_CHROMADB
        
        if self.use_chromadb:
            try:
                self.client = chromadb.PersistentClient(path=persist_directory)
                
                self.conversations = self.client.get_or_create_collection(
                    name="conversations",
                    metadata={"description": "Complete conversation history"}
                )
                
                self.preferences = self.client.get_or_create_collection(
                    name="preferences",
                    metadata={"description": "User preferences and settings"}
                )
                
                self.habits = self.client.get_or_create_collection(
                    name="habits",
                    metadata={"description": "User habits and patterns"}
                )
                
                self.needs = self.client.get_or_create_collection(
                    name="needs",
                    metadata={"description": "User needs and requirements"}
                )
                
                self.personality = self.client.get_or_create_collection(
                    name="personality",
                    metadata={"description": "User personality and communication style"}
                )
                
                self.commands = self.client.get_or_create_collection(
                    name="commands",
                    metadata={"description": "Frequently used commands"}
                )
            except Exception as e:
                print(f"⚠️ ChromaDB 初始化失败: {e}")
                print("   切换到 JSON 存储模式")
                self.use_chromadb = False
        
        if not self.use_chromadb:
            self.json_files = {
                "conversations": os.path.join(persist_directory, "conversations.json"),
                "preferences": os.path.join(persist_directory, "preferences.json"),
                "habits": os.path.join(persist_directory, "habits.json"),
                "needs": os.path.join(persist_directory, "needs.json"),
                "personality": os.path.join(persist_directory, "personality.json"),
                "commands": os.path.join(persist_directory, "commands.json")
            }
            for filepath in self.json_files.values():
                if not os.path.exists(filepath):
                    with open(filepath, 'w', encoding='utf-8') as f:
                        json.dump([], f)
        
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    def _load_json(self, category: str) -> List[Dict]:
        if self.use_chromadb:
            return []
        try:
            with open(self.json_files[category], 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    
    def _save_json(self, category: str, data: List[Dict]):
        if self.use_chromadb:
            return
        with open(self.json_files[category], 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def save_conversation(self, user_input: str, assistant_response: str, 
                          metadata: Optional[Dict] = None):
        timestamp = datetime.now().isoformat()
        doc_id = f"conv_{timestamp.replace(':', '-').replace('.', '-')}"
        
        content = f"User: {user_input}\nAssistant: {assistant_response}"
        
        meta = {
            "timestamp": timestamp,
            "session_id": self.session_id,
            "user_input": user_input,
            "assistant_response": assistant_response
        }
        if metadata:
            meta.update(metadata)
        
        if self.use_chromadb:
            try:
                self.conversations.add(
                    documents=[content],
                    metadatas=[meta],
                    ids=[doc_id]
                )
            except:
                pass
        else:
            data = self._load_json("conversations")
            data.append({
                "id": doc_id,
                "document": content,
                "metadata": meta
            })
            self._save_json("conversations", data)
        
        return doc_id
    
    def save_preference(self, key: str, value: str, category: str = "general"):
        doc_id = f"pref_{category}_{key}"
        
        if self.use_chromadb:
            try:
                self.preferences.add(
                    documents=[f"{key}: {value}"],
                    metadatas=[{
                        "key": key,
                        "value": value,
                        "category": category,
                        "updated_at": datetime.now().isoformat()
                    }],
                    ids=[doc_id]
                )
            except:
                pass
        else:
            data = self._load_json("preferences")
            existing = [d for d in data if d.get('id') == doc_id]
            if existing:
                existing[0]['document'] = f"{key}: {value}"
                existing[0]['metadata'] = {
                    "key": key,
                    "value": value,
                    "category": category,
                    "updated_at": datetime.now().isoformat()
                }
            else:
                data.append({
                    "id": doc_id,
                    "document": f"{key}: {value}",
                    "metadata": {
                        "key": key,
                        "value": value,
                        "category": category,
                        "updated_at": datetime.now().isoformat()
                    }
                })
            self._save_json("preferences", data)
    
    def save_habit(self, habit_name: str, description: str, frequency: int = 1):
        doc_id = f"habit_{habit_name.replace(' ', '_')}"
        
        if self.use_chromadb:
            try:
                self.habits.add(
                    documents=[f"{habit_name}: {description}"],
                    metadatas=[{
                        "name": habit_name,
                        "description": description,
                        "frequency": frequency,
                        "last_updated": datetime.now().isoformat()
                    }],
                    ids=[doc_id]
                )
            except:
                pass
        else:
            data = self._load_json("habits")
            data.append({
                "id": doc_id,
                "document": f"{habit_name}: {description}",
                "metadata": {
                    "name": habit_name,
                    "description": description,
                    "frequency": frequency,
                    "last_updated": datetime.now().isoformat()
                }
            })
            self._save_json("habits", data)
    
    def save_need(self, need: str, priority: str = "medium", context: str = ""):
        doc_id = f"need_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        if self.use_chromadb:
            try:
                self.needs.add(
                    documents=[need],
                    metadatas=[{
                        "need": need,
                        "priority": priority,
                        "context": context,
                        "created_at": datetime.now().isoformat()
                    }],
                    ids=[doc_id]
                )
            except:
                pass
        else:
            data = self._load_json("needs")
            data.append({
                "id": doc_id,
                "document": need,
                "metadata": {
                    "need": need,
                    "priority": priority,
                    "context": context,
                    "created_at": datetime.now().isoformat()
                }
            })
            self._save_json("needs", data)
    
    def save_personality_trait(self, trait: str, description: str):
        doc_id = f"personality_{trait.replace(' ', '_')}"
        
        if self.use_chromadb:
            try:
                self.personality.add(
                    documents=[f"{trait}: {description}"],
                    metadatas=[{
                        "trait": trait,
                        "description": description,
                        "updated_at": datetime.now().isoformat()
                    }],
                    ids=[doc_id]
                )
            except:
                pass
        else:
            data = self._load_json("personality")
            data.append({
                "id": doc_id,
                "document": f"{trait}: {description}",
                "metadata": {
                    "trait": trait,
                    "description": description,
                    "updated_at": datetime.now().isoformat()
                }
            })
            self._save_json("personality", data)
    
    def save_command(self, command: str, description: str, usage_count: int = 1):
        doc_id = f"cmd_{command.replace(' ', '_')}"
        
        if self.use_chromadb:
            try:
                existing = self.commands.get(ids=[doc_id])
                if existing and existing['documents']:
                    usage_count = existing['metadatas'][0].get('usage_count', 0) + 1
                
                self.commands.upsert(
                    documents=[f"{command}: {description}"],
                    metadatas=[{
                        "command": command,
                        "description": description,
                        "usage_count": usage_count,
                        "last_used": datetime.now().isoformat()
                    }],
                    ids=[doc_id]
                )
            except:
                pass
        else:
            data = self._load_json("commands")
            existing = [d for d in data if d.get('id') == doc_id]
            if existing:
                existing[0]['metadata']['usage_count'] = existing[0]['metadata'].get('usage_count', 0) + 1
                existing[0]['metadata']['last_used'] = datetime.now().isoformat()
            else:
                data.append({
                    "id": doc_id,
                    "document": f"{command}: {description}",
                    "metadata": {
                        "command": command,
                        "description": description,
                        "usage_count": usage_count,
                        "last_used": datetime.now().isoformat()
                    }
                })
            self._save_json("commands", data)
    
    def get_all_preferences(self) -> Dict:
        if self.use_chromadb:
            try:
                result = self.preferences.get()
                prefs = {}
                for i, doc in enumerate(result['documents']):
                    meta = result['metadatas'][i]
                    category = meta.get('category', 'general')
                    if category not in prefs:
                        prefs[category] = {}
                    prefs[category][meta['key']] = meta['value']
                return prefs
            except:
                return {}
        else:
            data = self._load_json("preferences")
            prefs = {}
            for item in data:
                meta = item.get('metadata', {})
                category = meta.get('category', 'general')
                if category not in prefs:
                    prefs[category] = {}
                prefs[category][meta.get('key', '')] = meta.get('value', '')
            return prefs
    
    def get_stats(self) -> Dict:
        stats = {}
        if self.use_chromadb:
            for name, coll in [
                ("conversations", self.conversations),
                ("preferences", self.preferences),
                ("habits", self.habits),
                ("needs", self.needs),
                ("personality", self.personality),
                ("commands", self.commands)
            ]:
                try:
                    stats[name] = coll.count()
                except:
                    stats[name] = 0
        else:
            for name in ["conversations", "preferences", "habits", "needs", "personality", "commands"]:
                data = self._load_json(name)
                stats[name] = len(data)
        return stats
    
    def export_to_json(self, filepath: str):
        data = {
            "exported_at": datetime.now().isoformat(),
            "conversations": [],
            "preferences": [],
            "habits": [],
            "needs": [],
            "personality": [],
            "commands": []
        }
        
        if self.use_chromadb:
            for coll_name, coll in [
                ("conversations", self.conversations),
                ("preferences", self.preferences),
                ("habits", self.habits),
                ("needs", self.needs),
                ("personality", self.personality),
                ("commands", self.commands)
            ]:
                try:
                    result = coll.get()
                    for i, doc in enumerate(result['documents']):
                        data[coll_name].append({
                            "document": doc,
                            "metadata": result['metadatas'][i] if result['metadatas'] else {}
                        })
                except:
                    pass
        else:
            for name in ["conversations", "preferences", "habits", "needs", "personality", "commands"]:
                data[name] = self._load_json(name)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        return filepath


if __name__ == "__main__":
    memory = LongTermMemory()
    
    print("=" * 60)
    print("长期记忆系统初始化完成")
    print(f"存储模式: {'ChromaDB' if memory.use_chromadb else 'JSON'}")
    print("=" * 60)
    
    memory.save_conversation(
        "测试对话",
        "这是测试响应",
        metadata={"test": True}
    )
    
    memory.save_preference("language", "中文", "communication")
    memory.save_habit("每天检查项目", "定期检查项目状态", 1)
    memory.save_need("需要部署Qwen模型", "high", "AI项目")
    memory.save_personality_trait("友好", "喜欢友好交流")
    memory.save_command("python qwen_demo.py", "启动Qwen对话")
    
    print("\n记忆统计:")
    stats = memory.get_stats()
    for key, value in stats.items():
        print(f"  {key}: {value} 条记录")
    
    print("\n✅ 长期记忆系统已就绪！")
