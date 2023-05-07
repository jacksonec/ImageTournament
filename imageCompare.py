import random
import queue
import threading
from skimage import metrics
import cv2
from PIL import Image
import numpy as np
import os
import string

def image_size_different(astrFile1, astrFile2):
    with Image.open(astrFile1) as img:
        width1, height1 = img.size

    with Image.open(astrFile2) as img:
        width2, height2 = img.size

    if (width1 == width2) and (height1 == height2):
        return False
    else:
        return True

def get_width_height(astrFile1):
    with Image.open(astrFile1) as img:
        return img.size

def resize_image(file_path, width_pixels = 250, height_pixels = 250):
    image = cv2.imread(file_path)
    image = cv2.resize(image, (height_pixels, width_pixels))
    return image



def image_compare_histogram(file_path1, file_path2):
    # Calculate the color histograms of the images
    image1 = resize_image(file_path1)
    image2 = resize_image(file_path2)

    hist1 = cv2.calcHist([image1], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
    hist2 = cv2.calcHist([image2], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])

    # Normalize the histograms
    cv2.normalize(hist1, hist1)
    cv2.normalize(hist2, hist2)

    # Compare the histograms using the Chi-Square distance
    distance = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CHISQR)

    return distance

def image_compare_ssim(file_path1, file_path2):
    image1 = resize_image(file_path1)
    image2 = resize_image(file_path2)

    # Convert the images to grayscale
    image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

    # Calculate the SSIM between the images
    ssim = metrics.structural_similarity(image1, image2)
    return ssim

def image_compare_mse(file_path1, file_path2):
    image1 = resize_image(file_path1)
    image2 = resize_image(file_path2)

    image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

    err = np.sum((image1.astype("float") - image2.astype("float")) ** 2)
    err /= float(image1.shape[0] * image2.shape[1])
    return err

def image_compare(file_path1, file_path2):
    result_dictionary = {}
    result_dictionary["histogram"] = image_compare_histogram(file_path1,file_path2)
    result_dictionary["ssim"] = image_compare_ssim(file_path1, file_path2)
    result_dictionary["mse"] = image_compare_mse(file_path1,file_path2)

    return result_dictionary

def image_match(result_dictionary):
    histogram = result_dictionary["histogram"]
    ssim = result_dictionary["ssim"]
    mse = result_dictionary["mse"]

    match = False

    if ssim >= .4:
        match = True
    elif ssim >= .2 and mse < 5500 and histogram < 500:
        match = True
    elif (ssim < .3 and ssim > .15) and histogram <= 10 and mse < 6000:
        match = True

    return match

def image_compare_thread(file_path1, file_path2, results_queue, log, semaphore, threadid):
    match = image_match(image_compare(file_path1, file_path2))
    results = image_compare(file_path1, file_path2)

    #print(threadid + " start.")

    if log:
        histogram = results["histogram"]
        ssim = results["ssim"]
        mse = results["mse"]
        with results_queue.mutex:
            results_dictionary = results_queue.queue[0]
        results_dictionary["log"].append(
            "Match: " +
            str(match) + " " +
            os.path.basename(file_path1) + ":" +
            os.path.basename(file_path2) + " - " + "H: " +
            str(histogram) + "S: " +
            str(ssim) + "M: " +
            str(mse) + " (Thread: " +
            threadid + ")")

    with semaphore:
        with results_queue.mutex:
            results_dictionary = results_queue.queue[0]
        if match:
            results_dictionary["match"].append(file_path2)
        else:
            results_dictionary["diffs"].append(file_path2)
        results_queue.put(results_dictionary)

    #print(threadid + " start.")

def image_compare_bulk(master_image_path, image_path_dictionary, log=False):
    results_queue = queue.Queue()
    results_dictionary = {"match": [], "diffs": []}

    if log:
        results_dictionary = {"match": [], "diffs": [], "log": []}
        results_dictionary["match"].append(master_image_path)

    results_queue.put(results_dictionary)

    semaphore = threading.Semaphore(25)
    threads = []

    for image_path in image_path_dictionary.keys():
        threadid = ''.join(random.choices(string.ascii_uppercase +
                             string.digits, k=8))
        thread = threading.Thread(target=image_compare_thread, args=(master_image_path, image_path, results_queue, log, semaphore, threadid))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return_dictionary = {}
    while not results_queue.empty():
        result = results_queue.get()
        return_dictionary.update(result)

    return return_dictionary