import os
import json
import shutil
import glob


def copy_misbehaving_files(src_folder, dst_folder):
    # Ensure the source folder exists
    assert os.path.isdir(src_folder), "Source folder does not exist"
    src_folder = os.path.join(src_folder, 'archive')

    if os.path.exists(src_folder):
        # Ensure the destination folder exists, create it if it doesn't exist
        if not os.path.exists(dst_folder):
            os.makedirs(dst_folder)

        # Iterate through all files in the source folder
        for filename in os.listdir(src_folder):
            if filename.endswith('.json'):
                file_path = os.path.join(src_folder, filename)
                # Read and parse the JSON file
                with open(file_path, 'r') as file:
                    try:
                        data = json.load(file)
                        # Check if "misbehaviour" is "True"
                        if data.get("misbehaviour") == "True":
                            # Copy the file to the destination folder
                            shutil.copy(file_path, dst_folder)
                            shutil.copy(file_path.replace('.json', '.png'), dst_folder)
                            print(f"Copied: {filename}")
                    except json.JSONDecodeError as e:
                        print(f"Error decoding JSON in file {filename}: {e}")


srcs = ["DeepJanus-Fashion-MNIST", "DeepJanus-MNIST", "DeepJanus-SVHN-gray"]
dsts = ["f-minist", "mnist", "svhn"]

for src, dst in zip(srcs, dsts):
    for class_id in range(10):
        src_folder = glob.glob(f'/home/xchen/Projects/deepjanus-usi/deepjanus/{src}/runs/label_{class_id}*')
        assert len(src_folder) >= 1, "Source folder does not exist"

        dst_folder = f'mimicry_result/DJ/{dst}/{class_id}/'  # Replace with the path to your destination folder
        copy_misbehaving_files(src_folder[0], dst_folder)