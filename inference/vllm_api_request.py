"""
A simple command-line tool for making multimodal API requests to vLLM-compatible endpoints.

Features:
- Auto-detects media type (video/image) based on file extension
- Supports both local files and web URLs
- Configurable API parameters via command line
- Single media file per request (video OR image, not both)

Supported formats:
- Videos: .mp4, .avi, .mov
- Images: .jpg, .png, .jpeg

Usage examples:
  python vllm_api_request.py --media-path "/path/video.mp4" --text "Analyze this video"
  python vllm_api_request.py --media-path "https://example.com/image.jpg" --text "Describe image"
  python vllm_api_request.py --media-path "/path/file.png" --text "What's this?" --temperature 0.5

Note: Only one media file (video OR image) can be processed per request.
"""

import argparse
import os

from openai import OpenAI


def get_media_type(file_path):
    video_extensions = {".mp4", ".avi", ".mov"}
    image_extensions = {".jpg", ".jpeg", ".png"}
    _, ext = os.path.splitext(file_path.lower())
    return (
        "video_url"
        if ext in video_extensions
        else "image_url"
        if ext in image_extensions
        else None
    )


def create_content_item(media_path, media_type):
    if media_path.startswith(("http://", "https://")):
        url = media_path
    else:
        url = "file://" + media_path

    if media_type == "video_url":
        return {"type": "video_url", "video_url": {"url": url}}
    else:
        return {"type": "image_url", "image_url": {"url": url}}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--api-key", default="EMPTY")
    parser.add_argument("--base-url", default="http://127.0.0.1:8000/v1")
    parser.add_argument("--model", default="THUDM/GLM-4.1V-9B-Thinking")
    parser.add_argument("--media-path", required=True)
    parser.add_argument("--text", required=True)
    parser.add_argument("--max-tokens", type=int, default=25000)
    parser.add_argument("--temperature", type=float, default=1.0)
    parser.add_argument("--repetition_penalty", type=float, default=1.0)
    parser.add_argument("--top-p", type=float, default=None)

    args = parser.parse_args()
    media_type = get_media_type(args.media_path)
    client = OpenAI(api_key=args.api_key, base_url=args.base_url)
    messages = [
        {
            "role": "user",
            "content": [
                create_content_item(args.media_path, media_type),
                {"type": "text", "text": args.text},
            ],
        }
    ]
    print("=========Messages=========")
    print(messages)
    response = client.chat.completions.create(
        model=args.model,
        messages=messages,
        max_tokens=args.max_tokens,
        temperature=args.temperature,
        top_p=args.top_p,
        extra_body={
            "skip_special_tokens": False,
            "repetition_penalty": args.repetition_penalty,
        },
    )
    print("=========Answer=========")
    print(response.choices[0].message.content.strip())


if __name__ == "__main__":
    main()
