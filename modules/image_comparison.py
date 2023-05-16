#import random
#import queue
#import threading
from skimage import metrics
import cv2
#from PIL import Image
import numpy as np
#import os
#import string


class ImageCompare:
    def image_size_different(self):
        height1, width1 = self.image1.shape[:2]
        height2, width2 = self.image2.shape[:2]
        self.image1_dimensions = width1, height1
        self.image2_dimensions = width2, height2

        if (width1 == width2) and (height1 == height2):
            return False

        return True

    def resize_image(self, image, width, height):
        image = cv2.resize(image, (height, width))
        return image

    def __init__(self, file_path1, file_path2, force_resize=True, width=250, height=250):
        self.image1_dimensions = None
        self.image2_dimensions = None
        self.file_path1 = file_path1
        self.file_path2 = file_path2
        self.width = width
        self.height = height
        self.force_resize = force_resize
        self.error = None
        self.image1 = cv2.imread(file_path1)
        self.image2 = cv2.imread(file_path2)

        if not force_resize:
            if self.image_size_different():
                self.image2 = self.resize_image(self.image2, self.image1_dimensions[1], self.image1_dimensions[0])
                self.error = "Images are different resolutions. Resizing to 250x250."
        else:
            self.image1 = self.resize_image(self.image1, width, height)
            self.image2 = self.resize_image(self.image2, width, height)


class ImageCompareHistogram(ImageCompare):
    def __init__(self, file_path1, file_path2, force_resize=True, width=250, height=250):
        super().__init__(file_path1, file_path2, force_resize, width, height)

    @property
    def compare_value(self):
        hist1 = cv2.calcHist([self.image1], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
        hist2 = cv2.calcHist([self.image2], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])

        # Normalize the histograms
        cv2.normalize(hist1, hist1)
        cv2.normalize(hist2, hist2)

        # Compare the histograms using the Chi-Square distance
        distance = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CHISQR)

        return distance


class ImageCompareSSIM(ImageCompare):
    def __init__(self, file_path1, file_path2, force_resize=True, width=250, height=250):
        super().__init__(file_path1, file_path2, force_resize, width, height)

    @property
    def compare_value(self):
        image1 = cv2.cvtColor(self.image1, cv2.COLOR_BGR2GRAY)
        image2 = cv2.cvtColor(self.image2, cv2.COLOR_BGR2GRAY)

        # Calculate the SSIM between the images
        ssim = metrics.structural_similarity(image1, image2)
        return ssim


class ImageCompareMSE(ImageCompare):
    def __init__(self, file_path1, file_path2, force_resize=True, width=250, height=250):
        super().__init__(file_path1, file_path2, force_resize, width, height)

    @property
    def compare_value(self):
        image1 = cv2.cvtColor(self.image1, cv2.COLOR_BGR2GRAY)
        image2 = cv2.cvtColor(self.image2, cv2.COLOR_BGR2GRAY)

        err = np.sum((image1.astype("float") - image2.astype("float")) ** 2)
        err /= float(image1.shape[0] * image2.shape[1])
        return err

