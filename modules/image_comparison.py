from skimage import metrics
import cv2
import numpy as np


def get_md5_hash(file_path):
    import hashlib

    md5_hash = hashlib.md5()

    with open(file_path, "rb") as file:
        for chunk in iter(lambda: file.read(4096), b""):
            md5_hash.update(chunk)

    return md5_hash.hexdigest()


class ImageCompare:

    def resize_image(self, image, width, height):
        image = cv2.resize(image, (width, height))
        return image

    def __init__(self, file_path1, file_path2, force_resize=False, width=250, height=250,
                 calc_ssim=True, calc_mse=True, calc_histogram=True):
        self.file_path1 = file_path1
        self.file_path2 = file_path2
        self.width = width
        self.height = height
        self.force_resize = force_resize
        self.error = None
        self.image1_hash = None
        self.image2_hash = None
        self.image1 = cv2.imread(file_path1)
        self.image2 = cv2.imread(file_path2)
        self.image1_dimensions = self.image1.shape[:2]
        self.image2_dimensions = self.image2.shape[:2]
        self.ssim = None
        self.histogram = None
        self.mse = None

        self.image1_hash = get_md5_hash(file_path1)
        self.image2_hash = get_md5_hash(file_path2)

        if self.image1_hash == self.image2_hash:
            self.ssim = 1
            self.histogram = 1
            self.mse = 0

        if not force_resize:
            if self.image1_dimensions[0] != self.image2_dimensions[0] or self.image1_dimensions[1] != \
                    self.image2_dimensions[1]:
                self.image2 = cv2.resize(self.image2, (self.image1_dimensions[1], self.image1_dimensions[0]))
            else:
                self.image1 = cv2.resize(self.image1, (width, height))
                self.image2 = cv2.resize(self.image2, (width, height))
        else:
            self.image1 = cv2.resize(self.image1, (width, height))
            self.image2 = cv2.resize(self.image2, (width, height))

        if calc_histogram and self.histogram is None:
            self.histogram = self.calc_histogram()
        if calc_ssim and self.ssim is None:
            self.ssim = self.calc_ssim()
        if calc_mse and self.mse is None:
            self.mse = self.calc_mse()

    def calc_histogram(self):
        hist1 = cv2.calcHist([self.image1], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
        hist2 = cv2.calcHist([self.image2], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])

        # Normalize the histograms
        cv2.normalize(hist1, hist1)
        cv2.normalize(hist2, hist2)

        # Compare the histograms using the Chi-Square distance
        distance = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CHISQR)

        self.histogram = distance
        return distance


    def calc_ssim(self):
        image1 = cv2.cvtColor(self.image1, cv2.COLOR_BGR2GRAY)
        image2 = cv2.cvtColor(self.image2, cv2.COLOR_BGR2GRAY)

        # Calculate the SSIM between the images
        ssim = metrics.structural_similarity(image1, image2)
        self.ssim = ssim
        return ssim


    def calc_mse(self):
        image1 = cv2.cvtColor(self.image1, cv2.COLOR_BGR2GRAY)
        image2 = cv2.cvtColor(self.image2, cv2.COLOR_BGR2GRAY)

        err = np.sum((image1.astype("float") - image2.astype("float")) ** 2)
        err /= float(image1.shape[0] * image2.shape[1])

        self.mse = err
        return err