import os

import models
import videodb

from abc import ABC, abstractmethod
from typing import List, Dict, Any

from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
MOONDREAM_API_KEY = os.getenv("MOONDREAM_API_KEY")


class BaseTask(ABC):
    def __init__(self, prompt: str = None):
        self.prompt = prompt

    @abstractmethod
    def run(self, model_name: str, video_scenes: List[Any], video_id: str) -> Dict:
        """Run the task on given video scenes"""
        pass

    @abstractmethod
    def get_scenes(self, video: videodb.video = None) -> List[Any]:
        """get the video scenes"""
        pass

    @abstractmethod
    def num_frames_per_call(self) -> int:
        """Number of frames to process per API call"""
        pass

    def establish_videodb_connection(self) -> tuple[videodb.Connection, str]:
        conn = videodb.connect()
        return conn

    def get_videos(
        self,
        conn: videodb.Connection,
        collection_id: str = None,
        video_ids: List[str] = None,
        num_vids: int = None,
    ) -> List[Any]:
        if not video_ids:
            coll = conn.get_collection(collection_id)
            videos = coll.get_videos()
        else:
            videos = []

            coll = conn.get_collection(collection_id)
            for video_id in video_ids:
                try:
                    videos.append(coll.get_video(video_id))
                except Exception as e:
                    print(f"Error while loading {video_id}, Error: {e}")

        return videos[:num_vids]

    def get_model(self, model_name: str) -> Any:
        if "gemini" in model_name:
            return models.Gemini(model_name, GEMINI_API_KEY)

        elif "gpt" in model_name:
            return models.Openai(model_name, OPENAI_API_KEY)

        elif "claude" in model_name:
            return models.Claude(model_name, ANTHROPIC_API_KEY)

        elif "moondream" in model_name:
            return models.Moondream(model_name, MOONDREAM_API_KEY)

        elif model_name == "rapidocr":
            return models.Rapidocr(model_name)

        elif model_name == "easyocr":
            return models.Easyocr(model_name)

        else:
            raise AttributeError(f"Model '{model_name}' is not implemented.")

    def evaluate(
        self, video_predictions: Dict = None, video_ground_truth: Dict = None
    ) -> Dict:
        """Optional evaluation method"""
        return {}
