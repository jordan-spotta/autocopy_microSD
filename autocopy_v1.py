import shutil
from pathlib import Path
import os


usb_mounting_point = Path("D:/")
output_parent_dir = Path(os.path.dirname(os.path.realpath(__file__))) / "out"
print(f"Copying contents of {usb_mounting_point} to {output_parent_dir}\n")

while True:
    folder_name = input("What is the pod number? ")
    output_dir = output_parent_dir / folder_name
    if usb_mounting_point.exists():
        shutil.copytree(str(usb_mounting_point), output_dir)
        system_volume_information = output_dir / "System Volume Information"
        if system_volume_information.exists():
            shutil.rmtree(str(system_volume_information))
        else:
            print("Warning: Didn't remove System Volume Information folder")
        print("Copying Done")
    else:
        print("Error: usb not inserted")

