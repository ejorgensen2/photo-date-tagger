"""
Example main file for sample Python package.
"""

import argparse
import os
from os import listdir

import easyocr
import numpy as np
from PIL import Image

IMG_EXTENSIONS = (".png", ".jpg", ".jpeg", ".tiff", ".bmp", ".gif")
ALLOWED_CHARS = {f"{i}" for i in range(10)} | {"'", "-", " "}

ocr_reader = easyocr.Reader(["en"], gpu=False)


def extract_imprinted_date(photo_path: str) -> str | None:
    """Attempt to find an imprinted date string in the photo at <photo_path>.

    Args:
        photo_path (str): Path string of photo.

    Returns:
        str | None: Date string imprinted on photo or None if not found or errored.
    """
    try:
        # Extract text and confidence level from photo, photo cropped to corner, and zoomed cropped photo
        print(f"Checking photo at {photo_path}")
        img = np.array(Image.open(photo_path))
        extracted = ocr_reader.readtext(img, allowlist=ALLOWED_CHARS, width_ths=0.7)
        if img.shape[0] < img.shape[1]:
            img = img[img.shape[0] // 2 :, img.shape[1] // 2 :, :]
        else:
            img = img[img.shape[0] // 2 :, 0 : img.shape[1] // 2, :]
        extracted_cropped = ocr_reader.readtext(img, allowlist=ALLOWED_CHARS, width_ths=0.7)
        extracted_zoomed = ocr_reader.readtext(img[::2, ::2, :], allowlist=ALLOWED_CHARS, width_ths=0.7)

        # Throw away bounding boxes
        extracted = [txt[-2:] for txt in extracted]
        extracted_cropped = [txt[-2:] for txt in extracted_cropped]
        extracted_zoomed = [txt[-2:] for txt in extracted_zoomed]
        print(f"Text found in photo: {extracted}")
        print(f"Text found in cropped photo: {extracted_cropped}")
        print(f"Text found in zoomed photo: {extracted_zoomed}")

        # Grab the highest confidence prediction out of the predictions that have valid length
        all_preds = [pred for pred in extracted + extracted_cropped + extracted_zoomed if 4 <= len(pred[0]) <= 12]
        if len(all_preds):
            extracted_text = max(all_preds, key=lambda x: x[1])
            print(extracted_text)
            return extracted_text[0]

        raise Exception

    except Exception as e:
        print(f"Error extracting imprinted date from photo at {photo_path}: {e}")
        return None


def parse_file_or_dir() -> list:
    """Return list of files in directory argument or filepath provided.

    Raises:
        ValueError: If both file and directory arguments are provided.

    Returns:
        list: List of valid files in provided directory or at provided filepath.
    """
    parser = argparse.ArgumentParser(description="Photos for which to check dates.")
    parser.add_argument("--directory", dest="dir", default=None, help="Directory path (default: ../test_photos/)")
    parser.add_argument("--file", dest="file", default=None, help="Photo path.")

    args = parser.parse_args()
    if args.file and args.dir:
        raise ValueError("Provide either file or directory argument, not both.")
    elif args.file and not args.dir:
        print(f"Checking for date in photo file {args.file}")
        file = args.file if os.path.isabs(args.file) else os.path.join(os.path.dirname(__file__), args.file)
        return [file] if os.path.isfile(file) else []
    else:
        dir = args.dir if args.dir else "../test_photos/"
        dir = dir if os.path.isabs(dir) else os.path.join(os.path.dirname(__file__), dir)
        print(f"Checking for date in photo directory {dir}")
        return [os.path.join(dir, f) for f in listdir(dir) if os.path.isfile(os.path.join(dir, f))]


def check_photo_dates() -> int:
    """
    Example function.

    Returns:
        int: Default run code.
    """
    files = [f for f in parse_file_or_dir() if f.lower().endswith(IMG_EXTENSIONS)]
    print(files)

    for file in files:
        print("")
        date_str = extract_imprinted_date(file)
        print(file, date_str)

    print(f"Finished function <check_photo_dates> within {os.path.realpath(__file__)}")
    return 0


def rename_photos() -> int:
    """
    Example function.

    Returns:
        int: Default run code.
    """
    print(f"Finished EMPTY function <rename_photos> within {os.path.realpath(__file__)}")
    return 0
