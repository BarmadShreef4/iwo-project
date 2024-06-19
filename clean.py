import glob
import os

from shutil import rmtree


def clean():
    for name in ("my-experiment", "ioh_data", "population_progress"):
        for path in glob.glob(f"{name}*"):
            if os.path.isfile(path):
                os.remove(path)
                print(f"Removed file:      {path}")
            if os.path.isdir(path):
                rmtree(path, ignore_errors=True)
                print(f"Removed directory: {path}")


if __name__ == "__main__":
    # Clean up any previous runs
    clean()
