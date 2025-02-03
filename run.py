import argparse
import json
import os
import videodb
import yaml

from datetime import datetime
from pathlib import Path
from tqdm import tqdm

from utils import create_directories, setup_logging, save_summary
from tasks import get_task


def load_yaml_config(file_path: str) -> dict:
    yaml_path = Path(file_path)
    if not yaml_path.exists():
        raise FileNotFoundError(f"YAML file not found: {file_path}")

    with open(yaml_path, "r") as file:
        config = yaml.safe_load(file)
    return config


def get_args_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        "Vision Language Models Benchmarking", add_help=False
    )

    parser.add_argument(
        "--model",
        default="gpt-4o",
        type=str,
        nargs="+",
        choices=[
            "all",
            "benchmark",
            "openai",
            "google",
            "anthropic",
            "gpt-4o",
            "gpt-4o-mini",
            "chatgpt-4o-latest",
            "gpt-4-turbo",
            "gemini-1.5-flash",
            "gemini-1.5-flash-8b",
            "claude-3-5-sonnet-latest",
            "easyocr",
            "rapidocr",
        ],
    )

    parser.add_argument("--num_vids", default=100, type=int)

    return parser


def main(args):
    # get the task name and config
    task, config = get_task("ocr")

    # setup directories to store the result
    args.openai_results_dir = config.OPENAI_RESULTS_DIR
    args.anthropic_results_dir = config.ANTHROPIC_RESULTS_DIR
    args.google_results_dir = config.GOOGLE_RESULTS_DIR
    args.ocr_results_dir = config.OCR_RESULTS_DIR

    args.openai_evaluation_dir = config.OPENAI_EVALUATION_DIR
    args.anthropic_evaluation_dir = config.ANTHROPIC_EVALUATION_DIR
    args.google_evaluation_dir = config.GOOGLE_EVALUATION_DIR
    args.ocr_evaluation_dir = config.OCR_EVALUATION_DIR

    args.save_paths = create_directories(args)

    current_run = f"ocr_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"

    # get prompt
    yaml_file = load_yaml_config("prompts.yaml")
    prompt = yaml_file["ocr"]

    # get the task processor
    processor = task(prompt)

    # establish VideoDB connection and get the data
    conn = processor.establish_videodb_connection()

    # get videos
    try:
        if config.VIDEO_IDS:
            videos = processor.get_videos(
                conn=conn,
                video_ids=config.VIDEO_IDS.values(),
                collection_id=config.COLLECTION_ID,
                num_vids=args.num_vids,
            )
        else:
            videos = processor.get_videos(
                conn=conn, collection_id=config.COLLECTION_ID, num_vids=args.num_vids
            )
    except videodb.exceptions.AuthenticationError:
        print(
            "Please make sure VIDEO_DB_API_KEY is set in your .env like VIDEO_DB_API_KEY=sk-****-****"
        )
        return
    except Exception as e:
        print(f"Run failed due to {e}")
        return

    # itereate through all the models
    for path in args.save_paths:
        model_name = os.path.basename(path)

        logger, current_run_dir = setup_logging(path, current_run)

        logger.info(
            f"################################ Running {model_name} Model on OCR Prompt ################################\n"
        )

        # iterate through all the videos
        
        for video in tqdm(videos, desc="Processing videos", unit="video"):
          
            video_scenes = processor.get_scenes(video)
            outputs = processor.run(model_name, video_scenes, video.id)

            if outputs is not None:
                json_file = os.path.join(current_run_dir, f"{video.id}_output.json")
                with open(json_file, "w") as file:
                    json.dump(outputs, file)
                logger.info(f"model results of {video.id} saved to {json_file}")

            else:
                logger.info(f"failed to save model results of {video.id}")

            # Evaluation

            # load ground truth
            gt_file = os.path.join(
                config.OCR_GROUND_TRUTH_DIR, f"{video.id}_ground_truth.json"
            )
            with open(gt_file, "r") as file:
                video_ground_truth = json.load(file)

            video_result = processor.evaluate(outputs, video_ground_truth)

            # save it in evaluation directory
            os.makedirs(os.path.join(current_run_dir, "evaluations"), exist_ok=True)

            eval_json_file = os.path.join(
                current_run_dir, "evaluations", f"{video.id}.json"
            )
            with open(eval_json_file, "w") as file:
                json.dump(video_result, file)

            logger.info(f"results evaluations of {video.id} saved to {eval_json_file}")

    # Evaluation summary
    save_summary(current_run)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        "Vision Languange Models Benchmarking", parents=[get_args_parser()]
    )
    args = parser.parse_args()

    main(args)
