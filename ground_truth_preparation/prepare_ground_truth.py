import os
import videodb
import time
import json

from dotenv import load_dotenv

load_dotenv()


collection_id = os.getenv("PREP_GROUND_TRUTH_COLLECTION_ID")
if not collection_id:
    collection_id = input(
        "Please provide the collection_id for which you want to create the ground truth:\n>> "
    )

# Connect to VideoDB
conn = videodb.connect()

coll = conn.get_collection(collection_id)
videos = coll.get_videos()
failed_videos = []

# Extract frames using VideoDB
for video in videos:
    outputs = []

    video_id = video.id
    try:
        extracted_scenes = video.extract_scenes(
            extraction_type=videodb.SceneExtractionType.time_based,
            extraction_config={"time": 1, "select_frames": ["first"]},
        )
        video_scenes = extracted_scenes.scenes
        print(f"Scenes extracted successfully for the {video.name} ({video.id}).")
    except Exception as e:
        print(f"Scene extraction failed for the {video.name} ({video.id}) due to {e}")
        print("Falling back on existing scene collections.")
        scene_collections = video.list_scene_collection()
        for sc in scene_collections:
            if (
                sc["config"]["extraction_type"] == "time"
                and sc["config"]["time"] == "1"
                and sc["config"]["select_frames"] == ["first"]
            ):
                print(f"Found existing scene collection: {sc['scene_collection_id']}")
                video_scenes = video.get_scene_collection(
                    sc["scene_collection_id"]
                ).scenes

    if not video_scenes:
        print("Scene extraction failed for {video.name} ({video.id}).")
        failed_videos.append(video)
        continue

    failed_scenes = []
    # Itereate through frames and describe them
    for scene in video_scenes:
        begin = time.time()
        try:
            out = scene.describe(
                prompt="Perform OCR on this image. Return only the text found in the image as a single continuous string without any newlines, additional text, or commentary. Separate words with single spaces. For any truncated, partially visible, or occluded text, include only the visible portions without attempting to complete or guess the full text. If no text is present, return empty double quotes",
            )
        except Exception:
            failed_scenes.append(scene)
            print(f"Scene description failed for {scene} of {video.name} ({video.id})")
            continue
        processing_time = time.time() - begin

        outputs.append(
            {
                "video_id": video_id,
                "start": scene.start,
                "end": scene.end,
                "frame_time": scene.start,
                "ocr_text": out,
                "processing_time": processing_time,
            }
        )

    os.makedirs("ocr_ground_truths", exist_ok=True)
    with open(
        os.path.join("ocr_ground_truths", f"{video_id}_ground_truth.json"), "w"
    ) as f:
        json.dump(outputs, f)

    if failed_scenes:
        print(f"Failed scenes of video {video.name}({video.id}): {failed_scenes}")


if failed_videos:
    print(f"Failed videos: {failed_videos}")
