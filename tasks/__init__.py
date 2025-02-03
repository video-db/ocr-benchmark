from .base_task import BaseTask
from .ocr import OCR
import configs.ocr_config as ocr_config

from typing import Any


def get_task(task_name: str) -> tuple[BaseTask, Any]:
    
    tasks = {
        "ocr": OCR
    }
    config = {
        "ocr": ocr_config
    }
    if task_name not in tasks:
        raise ValueError(f"Unknown task: {task_name}. Available tasks: {list(tasks.keys())}")
    
    if task_name not in config:
        raise ValueError(f"Unknown config for task: {task_name}. Available configs: {list(config.keys())}")
    return tasks[task_name], config[task_name]