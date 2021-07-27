import os
import shutil
from pathlib import Path
from tqdm import tqdm


DUMMY_MODE = False
output_parent_dir = Path(os.path.dirname(os.path.realpath(__file__))) / "out"

while True:
    drive = input("What drive (e.g 'd' for D:/)? ")
    source = Path(f"{drive.upper()}:/")

    pod_number = input("What is the pod number? ")
    target = output_parent_dir / pod_number
    if not DUMMY_MODE:
        target.mkdir(parents=True)

    corrupt_files = []
    total_number_of_items = sum(1 for _ in source.glob('**/*'))
    with tqdm(total=total_number_of_items) as pbar:
        for (root, dirs, files) in os.walk(str(source)):

            # Copy folder structure
            for directory in dirs:
                source_folder_path = Path(root) / directory
                relative_file_path = source_folder_path.relative_to(source)
                target_folder_path = target / relative_file_path
                if str(relative_file_path) == "System Volume Information":
                    pbar.update(1)
                    continue
                # print(str(source_folder_path).ljust(70), "->", target_folder_path)
                if not DUMMY_MODE:
                    target_folder_path.mkdir(parents=True, exist_ok=True)
                pbar.update(1)

            # Copy files
            for file in files:
                source_file_path = Path(root) / file
                relative_file_path = source_file_path.relative_to(source)
                target_file_path = target / relative_file_path
                if str(relative_file_path.parents[0]) == "System Volume Information":
                    pbar.update(1)
                    continue
                # print(str(source_file_path).ljust(70), "->", target_file_path)
                if not DUMMY_MODE:
                    try:
                        shutil.copyfile(source_file_path, target_file_path)
                    except IOError as e:
                        # Deal with corrupt image
                        if source_file_path.suffix == ".jpg":
                            try:
                                os.remove(target_file_path)
                            except FileNotFoundError as e:
                                pass
                            relative_file_path = relative_file_path.parent / (relative_file_path.stem + "CORRUPT.jpg")
                            target_file_path = target_file_path.parent / (target_file_path.stem + "CORRUPT.jpg")
                            shutil.copyfile("corrupt file.jpg", target_file_path)
                            corrupt_files.append(str(relative_file_path))
                        else:
                            raise Exception(f"Problem copying {source_file_path}")
                pbar.update(1)

    # Write list of corrupt files
    if len(corrupt_files) > 0:
        with open(str(target / "corrupt_files.txt"), "w") as file:
            for i in corrupt_files:
                file.write(i)
                file.write("\n")


