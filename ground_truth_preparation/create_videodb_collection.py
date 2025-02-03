import os
import json
import videodb
from typing import List, Union
from dotenv import load_dotenv

load_dotenv()


def get_user_input(prompt: str) -> str:
    return input(prompt).strip()


def get_videos_from_directory(directory: str) -> List[str]:
    if not os.path.exists(directory):
        raise ValueError(f"Videos directory not found: {directory}")
    return [os.path.join(directory, f) for f in os.listdir(directory)]


def get_videos_from_json(json_path: str) -> List[str]:
    if not os.path.exists(json_path):
        raise ValueError(f"JSON file not found: {json_path}")
    with open(json_path, "r") as f:
        data = json.load(f)
        if not isinstance(data, dict) or "urls" not in data:
            raise ValueError(
                "JSON file must contain a 'urls' key with a list of video URLs"
            )
        return data["urls"]


def upload_videos(coll: videodb.collection, videos: List[Union[str, dict]]) -> None:
    for video in videos:
        try:
            if isinstance(video, str):
                if video.startswith(("http://", "https://")):
                    video_object = coll.upload(url=video)
                    print(f"Uploaded URL {video} with id {video_object.id}")
                else:
                    video_object = coll.upload(file_path=video)
                    print(
                        f"Uploaded file: {os.path.basename(video)} with id {video_object.id}"
                    )
        except Exception as e:
            print(f"Failed to upload {video}: {str(e)}")


def main():
    # Connect to VideoDB
    conn = videodb.connect()

    # Get collection details from user
    collection_name = get_user_input("Enter collection name: ")
    collection_description = get_user_input("Enter collection description: ")

    # Create collection
    coll = conn.create_collection(collection_name, collection_description)
    print(f"Created collection: {collection_name} with collection id: {coll.id}")

    # Ask user for video source
    source_type = get_user_input("Enter video source type (files/urls): ").lower()

    videos = []
    if source_type == "files":
        videos_dir = get_user_input("Enter the directory path containing videos: ")
        videos = get_videos_from_directory(videos_dir)
    elif source_type == "urls":
        json_path = get_user_input(
            "Enter the path to JSON file containing video URLs: "
        )
        videos = get_videos_from_json(json_path)
    else:
        print("Invalid source type. Please choose 'files' or 'urls'")
        return

    # Upload videos
    upload_videos(coll, videos)


if __name__ == "__main__":
    main()
