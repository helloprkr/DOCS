from typing import Dict, Any, List
import logging
from datetime import datetime
import json
import os
from pathlib import Path

class VariableProcessor:
    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self.storage_dir = Path("data")
        self.storage_dir.mkdir(exist_ok=True)
        self.context_file = self.storage_dir / "context.json"
        self.tasks_file = self.storage_dir / "tasks.json"
        
        # Load or initialize context
        self.context: Dict[str, Any] = self._load_context()
        self.tasks: List[Dict[str, Any]] = self._load_tasks()
        
    def _load_context(self) -> Dict[str, Any]:
        """Load context from file or initialize if not exists."""
        try:
            if self.context_file.exists():
                with open(self.context_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            self.logger.error(f"Error loading context: {str(e)}")
            
        return {
            "date": datetime.now().isoformat(),
            "variables": {},
            "metadata": {}
        }
        
    def _load_tasks(self) -> List[Dict[str, Any]]:
        """Load tasks from file or initialize if not exists."""
        try:
            if self.tasks_file.exists():
                with open(self.tasks_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            self.logger.error(f"Error loading tasks: {str(e)}")
            
        return []
        
    def _save_context(self) -> None:
        """Save context to file."""
        try:
            with open(self.context_file, 'w') as f:
                json.dump(self.context, f, indent=2)
        except Exception as e:
            self.logger.error(f"Error saving context: {str(e)}")
            
    def _save_tasks(self) -> None:
        """Save tasks to file."""
        try:
            with open(self.tasks_file, 'w') as f:
                json.dump(self.tasks, f, indent=2)
        except Exception as e:
            self.logger.error(f"Error saving tasks: {str(e)}")
            
    def _normalize_key(self, key: str) -> str:
        """Normalize variable key to consistent format."""
        return key.lower().replace("-", "_").strip()
        
    def add_variable(self, name: str, value: Any) -> None:
        """Add a variable to the context."""
        try:
            if value:  # Only add non-empty values
                # Normalize the key
                key = self._normalize_key(name)
                self.context["variables"][key] = value
                self.logger.debug(f"Added variable {key}")
                self._save_context()
        except Exception as e:
            self.logger.error(f"Error adding variable {name}: {str(e)}")
            raise
            
    def add_metadata(self, key: str, value: Any) -> None:
        """Add metadata to the context."""
        try:
            if value:  # Only add non-empty values
                key = self._normalize_key(key)
                self.context["metadata"][key] = value
                self.logger.debug(f"Added metadata {key}")
                self._save_context()
        except Exception as e:
            self.logger.error(f"Error adding metadata {key}: {str(e)}")
            raise
            
    def add_task(self, description: str, status: Dict[str, bool] = None) -> None:
        """Add a task with optional status flags."""
        try:
            if not description:
                return
                
            if status is None:
                status = {
                    "completed_today": False,
                    "completed_later": False,
                    "decided_against": False
                }
                
            task = {
                "description": description,
                **status
            }
            
            self.tasks.append(task)
            self.logger.debug(f"Added task: {description}")
            self._save_tasks()
        except Exception as e:
            self.logger.error(f"Error adding task: {str(e)}")
            raise
            
    def update_task_status(self, task_index: int, status_update: Dict[str, bool]) -> None:
        """Update the status of a task by index."""
        try:
            if 0 <= task_index < len(self.tasks):
                task = self.tasks[task_index]
                for key, value in status_update.items():
                    if key in task:
                        task[key] = value
                self.logger.debug(f"Updated task {task_index} status")
                self._save_tasks()
            else:
                raise ValueError(f"Invalid task index: {task_index}")
        except Exception as e:
            self.logger.error(f"Error updating task status: {str(e)}")
            raise
            
    def get_context(self) -> Dict[str, Any]:
        """Get the current context."""
        return self.context
        
    def get_tasks(self) -> List[Dict[str, Any]]:
        """Get the current tasks."""
        return self.tasks
        
    def clear(self) -> None:
        """Clear all variables and tasks."""
        try:
            self.context["variables"].clear()
            self.context["metadata"].clear()
            self.tasks.clear()
            self._save_context()
            self._save_tasks()
            self.logger.info("Cleared all variables and tasks")
        except Exception as e:
            self.logger.error(f"Error clearing variables and tasks: {str(e)}")
            raise
