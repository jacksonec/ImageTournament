import imageCompare
import os
import shutil
from itertools import chain

def get_file_dictionary(directory):
    file_dictionary = {}
    for filename in os.listdir(directory):
        # Check if the file is an image file (optional)
        if filename.endswith(".jpg") or filename.endswith(".png"):
            # Create the full file path
            file_path = os.path.join(image_dir, filename)
            # Add the file path to the dictionary
            file_dictionary[file_path] = None
    return file_dictionary

#For each file in the directory, create a list entry
image_dir = r"C:\Users\jacks\PycharmProjects\ImageTournament\images"  # directory path
image_dict = get_file_dictionary(image_dir)  # dictionary to store image paths

matched_images = {}
diffs_images = []
image_dict_compare = image_dict.copy()
counter = 0
log_on = True
log = []

#loop through the master file list
for master_image in image_dict.keys():
    print("Checking " + master_image)
    if master_image in image_dict_compare:
        del image_dict_compare[master_image]
    results = imageCompare.image_compare_bulk(master_image, image_dict_compare, log_on)
    matches_count = len(results["match"])
    print("Found " + str(matches_count) + ".")
    for match in results["match"]:
        if match in image_dict_compare.keys():
            del image_dict_compare[match]

    if len(results["match"]) > 1:
        matched_images[counter] = results["match"]
        counter += 1

    if len(results["match"]) == 1:
        diffs_images.append(results["match"])

    if len(results["diffs"]) > 0:
        diffs_images.append(results["diffs"])

    if log_on:
        log.append(results["log"])

    print(str(len(image_dict_compare.keys())) + " more to compare.")

diffs_images = list(chain.from_iterable(diffs_images))
diffs_images = list(set(diffs_images))

for key in matched_images.keys():
    str_dir = ".\\images\\" + str(key)
    if not os.path.exists(str_dir):
        os.makedirs(str_dir)
    for image in matched_images[key]:
        shutil.copy(image, str_dir)
        if image in diffs_images:
            diffs_images.remove(image)

str_dir = ".\\images\\unmatched"
if not os.path.exists(str_dir):
    os.makedirs(str_dir)

for image_path in diffs_images:
    shutil.copy(image_path, str_dir)

if log_on:
    with open(r"images\match_log.txt", "w") as file:
        for item in log:
            for line in item:
                print(line, file=file)
