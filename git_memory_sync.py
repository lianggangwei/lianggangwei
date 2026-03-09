
import os
import subprocess
import json
from datetime import datetime

class GitMemorySync:
    def __init__(self, repo_path: str = "."):
        self.repo_path = repo_path
        self.memory_db_path = os.path.join(repo_path, "memory_db")
        
    def is_git_repo(self) -> bool:
        git_dir = os.path.join(self.repo_path, ".git")
        return os.path.exists(git_dir)
    
    def run_git_command(self, *args):
        try:
            result = subprocess.run(
                ["git"] + list(args),
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                encoding='utf-8'
            )
            return result.returncode == 0, result.stdout, result.stderr
        except Exception as e:
            return False, "", str(e)
    
    def sync_to_git(self, commit_message: str = None):
        if not self.is_git_repo():
            print("❌ 当前目录不是 Git 仓库")
            return False
        
        if commit_message is None:
            commit_message = f"自动同步记忆数据 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        success, _, _ = self.run_git_command("add", "memory_db/")
        if not success:
            print("⚠️ 添加 memory_db 到暂存区失败")
        
        success, _, _ = self.run_git_command("add", ".")
        if not success:
            print("⚠️ 添加文件到暂存区失败")
        
        success, stdout, stderr = self.run_git_command("commit", "-m", commit_message)
        if success:
            print(f"✅ 提交成功: {commit_message}")
        else:
            if "nothing to commit" in stderr or "nothing to commit" in stdout:
                print("ℹ️ 没有需要提交的更改")
            else:
                print(f"⚠️ 提交失败: {stderr}")
        
        success, stdout, stderr = self.run_git_command("push")
        if success:
            print("✅ 推送到远程仓库成功")
        else:
            print(f"⚠️ 推送失败: {stderr}")
        
        return True
    
    def pull_from_git(self):
        if not self.is_git_repo():
            print("❌ 当前目录不是 Git 仓库")
            return False
        
        success, stdout, stderr = self.run_git_command("pull")
        if success:
            print("✅ 从远程仓库拉取成功")
        else:
            print(f"⚠️ 拉取失败: {stderr}")
        
        return success
    
    def get_status(self):
        if not self.is_git_repo():
            return {"is_repo": False}
        
        success, stdout, _ = self.run_git_command("status", "--short")
        changes = stdout.strip().split('\n') if stdout.strip() else []
        
        success, stdout, _ = self.run_git_command("branch", "--show-current")
        branch = stdout.strip() if success else "unknown"
        
        return {
            "is_repo": True,
            "branch": branch,
            "changes": changes,
            "has_memory_db": os.path.exists(self.memory_db_path)
        }
    
    def auto_sync(self):
        print("=" * 60)
        print("自动同步记忆数据到 Git")
        print("=" * 60)
        
        status = self.get_status()
        
        if not status["is_repo"]:
            print("❌ 当前目录不是 Git 仓库")
            print("   请先初始化 Git 仓库: git init")
            return False
        
        print(f"\n当前分支: {status['branch']}")
        print(f"记忆数据库: {'存在' if status['has_memory_db'] else '不存在'}")
        
        if status['changes']:
            print(f"\n待提交的更改: {len(status['changes'])} 个文件")
        
        print("\n正在同步...")
        
        self.pull_from_git()
        self.sync_to_git()
        
        return True


if __name__ == "__main__":
    sync = GitMemorySync()
    sync.auto_sync()
