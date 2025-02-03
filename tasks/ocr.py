from .base_task import BaseTask

from typing import List, Dict, Any
import re
from collections import Counter
import Levenshtein
from tqdm import tqdm
import videodb


class OCR(BaseTask):
    def __init__(self, prompt: str = None):
        super().__init__(prompt)
        self.num_frames_per_call()

    def get_scenes(self, video: videodb.video = None) -> List[Any]:
        try:
            extracted_scenes = video.extract_scenes(
                extraction_type=videodb.SceneExtractionType.time_based,
                extraction_config={"time": 1, "select_frames": ["first"]},
            )

            video_scenes = extracted_scenes.scenes

        except Exception as e:
            scene_collections = video.list_scene_collection()

            # get the scene collection with the desired configuration
            for sc in scene_collections:
                if (
                    sc["config"]["extraction_type"] == "time"
                    and sc["config"]["time"] == "1"
                    and sc["config"]["select_frames"] == ["first"]
                ):
                    print(
                        f"Found existing scene collection: {sc['scene_collection_id']}"
                    )
                    video_scenes = video.get_scene_collection(
                        sc["scene_collection_id"]
                    ).scenes
                    return video_scenes

        return video_scenes

    def run(self, model_name: str, video_scenes: List[Any], video_id: str) -> Dict:
        outputs = []

        model = self.get_model(model_name)

        with tqdm(total=len(video_scenes), desc=f"Processing scenes for video {video_id}", unit="scene") as pbar:
            for scene in video_scenes:
                frame_urls = []
                # Iterate through each frame in the scene
                for frame in scene.frames:
                    frame_urls.append(frame.url)

                processing_time, out = model.describe(frame_urls, self.prompt)

                outputs.append(
                    {
                        "video_id": video_id,
                        "scene_start_time": scene.start,
                        "scene_end_time": scene.end,
                        "processing_time": processing_time,
                        "image": frame_urls,
                        "model_output": out,
                    }
                )
                pbar.update(1)

        return outputs

    def num_frames_per_call(self) -> int:
        """Number of frames to process per API call"""
        self.num_frames = 1

    def evaluate(
        self, video_predictions: Dict = None, video_ground_truth: Dict = None
    ) -> Dict:
        def preprocess_text(text):
            # Remove any surrounding quotes
            text = text.strip('"')
            # Remove newlines and extra whitespace
            text = re.sub(r"\s+", " ", text)
            return text.strip()

        def calculate_character_error_rate(ground_truth, ocr_text):
            """
            Calculate the Character Error Rate (CER) between ground truth and OCR text.

            CER = (S + D + I) / N
            where:
            S is the number of substitutions,
            D is the number of deletions,
            I is the number of insertions,
            N is the number of characters in the ground truth.
            """
            distance = Levenshtein.distance(ground_truth, ocr_text)
            return distance / len(ground_truth) if ground_truth else 1.0

        def calculate_word_error_rate(ground_truth, ocr_text):
            """
            Calculate the Word Error Rate (WER) between ground truth and OCR text.

            WER = (S + D + I) / N
            where:
            S is the number of substituted words,
            D is the number of deleted words,
            I is the number of inserted words,
            N is the number of words in the ground truth.
            """

            ground_truth_words = ground_truth.split()
            ocr_words = ocr_text.split()
            distance = Levenshtein.distance(ground_truth_words, ocr_words)
            return distance / len(ground_truth_words) if ground_truth_words else 1.0

        def calculate_accuracy(ground_truth, ocr_text):
            """
            Calculate the accuracy of the OCR text compared to the ground truth.

            Accuracy = (1 - CER) * 100
            """
            cer = calculate_character_error_rate(ground_truth, ocr_text)
            return (1 - cer) * 100

        def calculate_order_agnostic_accuracy(ground_truth, ocr_text):
            """
            Calculate order-agnostic word accuracy between ground truth and OCR text.

            Word Accuracy = (Number of correct words) / (Total words in ground truth)

            Args:
                ground_truth (str): The ground truth text
                ocr_text (str): The OCR output text

            Returns:
                float: Word accuracy score between 0 and 100
            """

            if not ground_truth:
                return 0.0

            # optmizing the search
            ground_truth_set = set(ground_truth)

            ground_truth_freq = Counter(ground_truth)
            ocr_freq = Counter(ocr_text)

            # Count matching words
            matching_words = sum(
                min(ground_truth_freq[word], ocr_freq[word])
                for word in ground_truth_freq
            )

            accuracy = matching_words / len(ground_truth)

            return accuracy * 100

        results = []
        for scene_pred, scene_ground_truth in zip(
            video_predictions, video_ground_truth
        ):
            # import pdb
            # pdb.set_trace()
            if (
                scene_pred["scene_start_time"] == scene_ground_truth["start"]
                and scene_pred["scene_end_time"] == scene_ground_truth["end"]
            ):
                model_output = preprocess_text(scene_pred["model_output"])
                ground_truth = preprocess_text(scene_ground_truth["ocr_text"])

                cer = calculate_character_error_rate(ground_truth, model_output)
                wer = calculate_word_error_rate(ground_truth, model_output)
                accuracy = calculate_accuracy(ground_truth, model_output)
                order_agnostic_accuray = calculate_order_agnostic_accuracy(
                    ground_truth, model_output
                )

                results.append(
                    {
                        "video_id": scene_pred["video_id"],
                        "scene_start": scene_pred["scene_start_time"],
                        "Scene_end": scene_pred["scene_end_time"],
                        "image": scene_pred["image"],
                        "ground_truth": ground_truth,
                        "ocr": model_output,
                        "cer": cer,
                        "wer": wer,
                        "accuracy": accuracy,
                        "order_agnostic_accuray": order_agnostic_accuray,
                        "processing_time": scene_pred["processing_time"],
                    }
                )

        return results
