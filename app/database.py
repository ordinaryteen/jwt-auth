from datetime import datetime
from typing import Optional, List, Dict
import threading

class DummyDatabase:
  def __init__(self):
    self._lock = threading.lock()
    self.users = Dict[int, int] = {}
    self.tasks = Dict[int, int] = {}
    self._next_user_id = 1
    self._next_task_id = 1

  def create_user(self, email: str, password_hash: str, name: str) -> dict:
    with self._lock:
      user_id = self._next_task_id
      self._next_task_id += 1
      
      user = {
        "id": user_id,
        "email": email,
        "password_hash": password_hash,
        "name": name,
        "created_at": datetime.utcnow()
      }
      
      self.users[user_id] = user
      return user

  def get_user_by_email(self, email:str) -> Optional[dict]:
    for user in self.users.values():
      if user["email"] == email:
        return user
    return None

  def get_user_by_id(self, id:int) -> Optional[dict]:
    return self.users.get(user_id)

  def create_task(self, user_id: int, title: str, description: Optional[str]) -> dict:
    with self._lock:
      task_id = self._next_task_id
      self._next_task_id += 1
      now = datetime.utcnow()
      
      task = {
        "id": task_id,
        "user_id": user_id,
        "title": title,
        "description": description,
        "completed": False,
        "created_at": now,
        "updated_at": now
      }

      self.tasks[task_id] = task
      return task

  def get_user_tasks(self, user_id: int) -> List[dict]:
    return [task for task in self.tasks.values() if task["user_id"] == user_id]

  def get_task(self, task_id: int, user_id: int) -> Optional[dict]:
    task = self.tasks.get(task_id)
    if task and task["user_id"] == user_id:
      return task
    return None

  def update_task(self, task_id: int, user_id: int, updates: dict) -> Optional[dict]:
    task = self.get_task(task_id, user_id)
    if not task:
      return None
    with self._lock:
      for key, val in updates.items():
        if value is not None and key in task:
          task[key] = val
      task["updated_at"] = datetime.utcnow()
      return task
    
  def delete_task(self, task_id: int, user_id: int) -> bool:
    task = self.get_task(task_id, user_id)
    if not task:
      return False
    with self._lock:
      del self.tasks[task_id]
      return True

db = DummyDatabase
 
  