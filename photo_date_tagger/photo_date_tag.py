"""
Example main file for sample Python package.
"""

import argparse
import os
from os import listdir

import easyocr
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image  # , ImageOps

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
        # Extract text and confidence level from photo and several augmented forms of the photo.
        print(f"Checking photo at {photo_path}")
        img_forms = {"orig": np.array(Image.open(photo_path))}

        M, N, _ = img_forms["orig"].shape
        img_forms["downsamp"] = img_forms["orig"][::2, ::2, :]

        img_forms["50perc_crop"] = (
            img_forms["orig"][M // 2 :, N // 2 :, :] if M < N else img_forms["orig"][M // 2 :, 0 : N // 2, :]
        )
        img_forms["50perc_crop_downsamp"] = img_forms["50perc_crop"][::2, ::2, :]

        img_forms["33perc_crop"] = (
            img_forms["orig"][2 * M // 3 :, 2 * N // 3 :, :]
            if M < N
            else img_forms["orig"][2 * M // 3 :, 0 : N // 3, :]
        )
        img_forms["33perc_crop_downsamp"] = img_forms["33perc_crop"][::2, ::2, :]

        # Plot image manipulations and their respective color histograms.
        _, ax = plt.subplots(2, len(img_forms), figsize=(len(img_forms) * 3.5, 7))
        for i, key in enumerate(img_forms):
            # Plot image
            ax[0, i].imshow(img_forms[key])
            ax[0, i].set_title(f"{key} - {img_forms[key].shape}")
            ax[0, i].set_xticks([])
            ax[0, i].set_yticks([])

            # Plot channel histogram
            for ch, col in [(0, "r"), (1, "g"), (2, "b")]:
                hist, bins = np.histogram(img_forms[key][ch].flatten(), bins=256, range=(0, 256))
                ax[1, i].plot(bins[:-1], hist, color=col, lw=0.5)
        plt.tight_layout()
        plt.show()

        # Run OCR to extract text
        extracted_text = {
            k: ocr_reader.readtext(v, allowlist=ALLOWED_CHARS, width_ths=0.7) for k, v in img_forms.items()
        }
        extracted_text = {k: [txt[-2:] for txt in v] for k, v in extracted_text.items()}

        # Grab the highest confidence prediction out of the predictions that have valid length
        all_preds = [x for x in sum(extracted_text.values(), []) if 4 <= len(x[0]) <= 12]
        if len(all_preds):
            print(max(all_preds, key=lambda x: x[1]))
            return max(all_preds, key=lambda x: x[1])[0]

        raise ValueError

    except ValueError as e:
        print(f"Error extracting imprinted date from photo at {photo_path}: {e}")
        return None


def parse_file_or_dir() -> list:
    """Return list of files in directory argument or filepath provided via Command Line.

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
    if args.file and not args.dir:
        print(f"Checking for date in photo file {args.file}")
        file = args.file if os.path.isabs(args.file) else os.path.join(os.path.dirname(__file__), args.file)
        return [os.path.abspath(file)] if os.path.isfile(file) else []

    directory = args.dir if args.dir else "../test_photos/"
    directory = directory if os.path.isabs(directory) else os.path.join(os.path.dirname(__file__), directory)
    print(f"Checking for date in photo directory {directory}")
    return [
        os.path.abspath(os.path.join(directory, f))
        for f in listdir(directory)
        if os.path.isfile(os.path.join(directory, f))
    ]


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

    print(f"\nFinished function <check_photo_dates> within {os.path.realpath(__file__)}")
    return 0


def rename_photos() -> int:
    """
    Example function.

    Returns:
        int: Default run code.
    """
    print(f"Finished EMPTY function <rename_photos> within {os.path.realpath(__file__)}")
    return 0
