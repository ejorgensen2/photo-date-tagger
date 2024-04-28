## Photo Date Tagger

This repository is designed to extract imprinted dates from film photos and give the option to prepend the extracted
date onto the photo's filename.

### Setup instructions

1. `git clone` the repository.
2. Ensure poetry is installed. 
3. `cd photo-date-tagger`
4. `poetry shell`
5. `poetry install`
6. `pre-commit install`. This runs based on a `.pre-commit-config.yaml` file in the repository. To run checks, use `pre-commit run -a`.

### Usage

#### Extract photo date (w/o changing filename)
- `poetry run check-photo-dates` Extract photo date strings from images in default `test_photos/` directory.
- `poetry run check-photo-dates --directory <path>` Extract photo date strings from images in `path` directory.
- `poetry run check-photo-dates --file <filepath>` Extract photo date string from the image at `filepath`.

#### Extract photo date and Rename
- `poetry run rename-photos` Not Yet Implemented.