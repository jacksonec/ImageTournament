import image_comparison
import threading
import queue
import os
import file_stuff

def get_image_files(path):
    image_files = []

    for file in os.listdir(path):
        if file.endswith(".jpg") or file.endswith(".png"):
            image_files.append(file)

    return image_files


# A class for an image and values of matching for the different image comparisons
class ImageDifferential:
    def __init__(self, primary_image_path, compare_image_path_list,
                 ssim_compare=True, mse_compare=True, histogram_compare=True,
                 threads=25, force_resize=True, width=250, height=250):
        self.primary_image_path = primary_image_path
        self.compare_image_path_list = compare_image_path_list
        self.threads = threads
        self.force_resize = force_resize
        self.width = width
        self.height = height
        self.ssim_compare = ssim_compare
        self.histogram_compare = histogram_compare
        self.mse_compare = mse_compare
        self.results_list = []
        self.status = None
        self._cancel = False
        self._debug_mode = False

    @property
    def debug_mode(self):
        return self._debug_mode

    @debug_mode.setter
    def debug_mode(self, value):
        self._debug_mode = value

    def compare_thread(self, primary_file_path: str, compare_image_path: str, semaphore: threading.Semaphore, results_queue: queue.Queue) -> None:
        """
        Singular thread to compare two images together. Sub function of compare_images
        :param primary_file_path: The master image to be compared
        :param compare_image_path: The paired image to compare
        :param semaphore: Semaphore object to hold or go based on threading
        :param results_queue: A threading queue, holds the data till all the threads are done
        """
        measures_dictionary = {"image1": primary_file_path, "image2": compare_image_path, "ssim": None,
                               "mse": None, "histogram": None}
        semaphore.acquire()
        try:
            if not results_queue.empty():
                for check_dictionary in results_queue.queue:
                    if primary_file_path in check_dictionary and compare_image_path in check_dictionary:
                        return

            comparison = image_comparison.ImageCompare(primary_file_path, compare_image_path, self.force_resize,
                                                       self.width, self.height)
            if self.ssim_compare:
                measures_dictionary["ssim"] = comparison.ssim
            if self.mse_compare:
                measures_dictionary["mse"] = comparison.mse
            if self.histogram_compare:
                measures_dictionary["histogram"] = comparison.histogram

            results_queue.put(measures_dictionary)
        finally:
            semaphore.release()

    def compare_images(self):
        results_queue = queue.Queue()
        threads = []
        semaphore = threading.Semaphore(self.threads)
        results = []
        processed_images = 0
        total_images = len(self.compare_image_path_list)

        for image_path in self.compare_image_path_list:
            thread = threading.Thread(target=self.compare_thread,
                                      args=(self.primary_image_path, image_path, semaphore, results_queue))

            threads.append(thread)
            thread.start()
            processed_images += 1
            progress = processed_images / total_images
            progress_message = f"Progress: {progress * 100:.2f}%"
            if self.debug_mode:
                print(progress_message)  # Print the progress
            self.status = progress_message

        for thread in threads:
            if self.debug_mode:
                print("Thread complete")
            thread.join(timeout=0.1)

        while not results_queue.empty():
            result = results_queue.get()
            results.append(result)

        self.results_list = results
        return self.results_list

    @property
    def cancel(self):
        return self._cancel

    @cancel.setter
    def cancel(self, value):
        self._cancel = value


# A class for an ungrouped list of images, compares them, returning a list of images in their
# comparison values to any other image
class ImageDiffList:
    def __init__(self, image_path_list=None, compare_ssim=True, compare_histogram=True, compare_mse=True):
        # Takes an argument of image paths in a list
        self.image_path_list = image_path_list

        if self.image_path_list is None:
            self.image_path_list = []

        self.compare_mse = compare_mse
        self.compare_histogram = compare_histogram
        self.compare_ssim = compare_ssim
        self._force_resize = True
        self._threads = 25
        self._width = 250
        self._height = 250

    def add(self, value):
        self.image_path_list.append(value)

    def remove(self, value):
        self.image_path_list.remove(value)

    def clear(self):
        self.image_path_list = []

    def build_image_table(self):

        for image_path in self.image_path_list:
            temp_image_list = self.image_path_list
            temp_image_list.remove(image_path)
            new_compare = ImageDifferential(image_path, temp_image_list, self.compare_ssim,
                                            self.compare_mse, self.compare_histogram, self.threads,
                                            self.force_resize, self.width, self.height)

            new_compare.compare_images()
            temp_var = len(new_compare.results_list)
            print(f"Len: {temp_var}: {new_compare.results_list}")

    @property
    def force_resize(self):
        return self._force_resize

    @force_resize.setter
    def force_resize(self, value):
        self._force_resize = value

    @property
    def threads(self):
        return self._threads

    @threads.setter
    def threads(self, value):
        self._threads = value

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        self._width = value

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        self._height = value


file_list = file_stuff.FileList(r"C:\Users\jacks\PycharmProjects\ImageTournament\images", [".jpg", ".png"], False)

imageDiff = ImageDiffList(file_list.files)
imageDiff.threads = 25
imageDiff.force_resize = False
imageDiff.build_image_table()

