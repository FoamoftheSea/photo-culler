import argparse
import json
from pprint import pprint

import ollama
import shutil

from pathlib import Path

PROMPT = """
Assess the quality of the following image based on key photographic criteria: 
focus, composition, exposure, color balance, and subject matter interest.
Rate each of these criteria from 1-10 and store them under appropriate headers in your JSON response.
Include your notes about the image that led to these ratings under a header called "notes".
Then, rate the overall image on a scale from 1 to 10, storing this value under a header called "score".

Example response:
{
    "focus": 3,
    "composition": 7,
    "exposure": 7,
    "color_balance": 6,
    "subject_matter_interest": 5,
    "notes": "Although the composition and color balance compliment the subject matter, the image is quite blurry.
    "score": 5
}
"""


def main(args):

    extensions = ["png", "jpeg", "jpg"]
    img_folder = Path(args.input)
    out_folder = Path(args.output)
    img_paths = []
    for ext in extensions:
        img_paths.extend(list(img_folder.glob(f"*.{ext}")))

    photo_reviews = {}
    photo_scores = {}
    for img_path in img_paths:
        res = ollama.generate(
            model="llava:photo-culler",
            prompt=PROMPT,
            images=[img_path],
            stream=False,
            format="json"
        )
        res_dict = json.loads(res["response"])
        res_dict["url"] = str(img_path)
        pprint(res_dict)
        photo_reviews[img_path.stem] = res_dict
        photo_scores[img_path] = float(res_dict["score"])

    keepers = {k: v for k, v in photo_scores.items() if v >= args.min_score}
    for img_path in sorted(keepers, reverse=True)[:args.num_keepers]:
        out_path = out_folder / img_path.name
        out_path.mkdir(parents=True, exist_ok=True)
        shutil.copy(img_path, out_path)

    if len(photo_reviews) > 0:
        with open(out_folder / "photo_reviews.json", "w") as f:
            json.dump(photo_reviews, f, indent=4)


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Scan folder of photographs and save the keepers to a new folder.")
    parser.add_argument("-i", "--input", type=str, help="Path to folder containing images.")
    parser.add_argument("-o", "--output", default="./keepers/", help="Path to output folder for keepers.")
    parser.add_argument("-ms", "--min-score", default=7, type=int, help="Minimum score (out of 10) to keep a photo.")
    parser.add_argument("-n", "--num-keepers", default=None, type=int, help="Max number of photos to keep.")

    args = parser.parse_args()
    main(args)
