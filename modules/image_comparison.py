from skimage import metrics
import cv2
import numpy as np


class ImageCompare:
    def image_dimensions(self, image):
        height, width = self.image1.shape[:2]
        return width, height

    def image_size_different(self):
        width1 = self.image1_dimensions[0]
        width2 = self.image2_dimensions[0]
        height1 = self.image1_dimensions[1]
        height2 = self.image2_dimensions[1]

        if (width1 == width2) and (height1 == height2):
            return False

        return True

    def resize_image(self, image, width, height):
        image = cv2.resize(image, (width, height))
        return image

    def __init__(self, file_path1, file_path2, force_resize=False, width=250, height=250,
                 calc_ssim=True, calc_mse=True, calc_histogram=True):
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
        self.image1_dimensions = self.image_dimensions(self.image1)
        self.image2_dimensions = self.image_dimensions(self.image2)

        if not force_resize:
            if self.image_size_different():
                self.image2 = self.resize_image(self.image2, self.image1_dimensions[0], self.image1_dimensions[1])
        else:
            self.image1 = self.resize_image(self.image1, width, height)
            self.image2 = self.resize_image(self.image2, width, height)

        self.histogram = self.calc_histogram()
        self.ssim = self.calc_ssim()
        self.mse = self.calc_mse()


    def calc_histogram(self):
        hist1 = cv2.calcHist([self.image1], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
        hist2 = cv2.calcHist([self.image2], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])

        # Normalize the histograms
        cv2.normalize(hist1, hist1)
        cv2.normalize(hist2, hist2)

        # Compare the histograms using the Chi-Square distance
        distance = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CHISQR)

        return distance


    def calc_ssim(self):
        image1 = cv2.cvtColor(self.image1, cv2.COLOR_BGR2GRAY)
        image2 = cv2.cvtColor(self.image2, cv2.COLOR_BGR2GRAY)

        # Calculate the SSIM between the images
        ssim = metrics.structural_similarity(image1, image2)
        return ssim


    def calc_mse(self):
        image1 = cv2.cvtColor(self.image1, cv2.COLOR_BGR2GRAY)
        image2 = cv2.cvtColor(self.image2, cv2.COLOR_BGR2GRAY)

        err = np.sum((image1.astype("float") - image2.astype("float")) ** 2)
        err /= float(image1.shape[0] * image2.shape[1])
        return err