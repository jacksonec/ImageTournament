import image_comparison
import threading
import queue
import os


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
        self.debug_mode = False
        self.status = None
        self.cancel = False

    @property
    def debug_mode(self):
        return self.debug_mode

    @debug_mode.setter
    def debug_mode(self, value):
        self.debug_mode = value

    def compare_thread(self, primary_file_path, compare_image_path, semaphore, results_queue):
        measures_dictionary = {"image1": primary_file_path, "image2": compare_image_path, "ssim": None,
                               "mse": None, "histogram": None}
        semaphore.acquire()
        try:
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

    @property
    def results_list(self):
        if len(self.results_list) == 0:
            self.compare_images()
        return self.results_list

    @results_list.setter
    def results_list(self, value):
        self.compare_images()

    @property
    def cancel(self):
        return self.cancel

    @cancel.setter
    def cancel(self, value):
        self.cancel = value

# A class for an ungrouped list of images
class ImageList:
    def __init__(self, image_path_list, compare_ssim=True, compare_histogram=True, compare_mse=True):
        # Takes an argument of image paths in a list
        self.image_list = image_path_list
        self.compare_mse = compare_mse
        self.compare_histogram = compare_histogram
        self.compare_ssim = compare_ssim


    def group_images(self):
        for image_path in self.image_list:
            temp_image_list = self.image_list
            temp_image_list.remove(image_path)
            new_compare = ImageDifferential(image_path, temp_image_list)
            thread = threading.Thread(target=new_compare.results_list)
            thread.start




new_compare = image_comparison.ImageCompare(r"C:\Users\jacks\PycharmProjects\ImageTournament\images\1.jpg", r"C:\Users\jacks\PycharmProjects\ImageTournament\images\2.jpg")
print(new_compare.ssim)