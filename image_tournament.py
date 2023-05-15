import os
import random
import tkinter as tk
from PIL import ImageTk, Image


class ImageTourneyWindow:
    def draw_result(self):
        self.result = "draw"
        self.destroy_window()

    def image1_result(self, event):
        self.result = self.image1_path
        self.destroy_window()

    def image2_result(self, event):
        self.result = self.image2_path
        self.destroy_window()

    def destroy_window(self):
        self.window_object.destroy()
        pass

    def build_window(self):
        self.image1 = Image.open(self.image1_path)
        self.image2 = Image.open(self.image2_path)

        width = 250
        height1 = int((width / float(self.image1.size[0])) * self.image1.size[1])
        height2 = int((width / float(self.image2.size[0])) * self.image2.size[1])
        self.image1 = self.image1.resize((width, height1))
        self.image2 = self.image2.resize((width, height2))
        win_width = (width * 2) + 50
        win_height = height1 + 50

        self.window_object = tk.Tk()

        root = self.window_object
        root.title("Tournament Time!")
        root.geometry(f"{win_width}x{win_height}")

        image_frame = tk.Frame(root)
        image_frame.pack()

        tk_image1 = ImageTk.PhotoImage(self.image1)
        tk_image2 = ImageTk.PhotoImage(self.image2)

        image_display1 = tk.Label(image_frame, image=tk_image1)
        image_display1.bind("<Button-1>", self.image1_result)
        image_display2 = tk.Label(image_frame, image=tk_image2)
        image_display2.bind("<Button-1>", self.image2_result)

        image_display1.pack(side="left")
        image_display2.pack(side="left")

        tie_button = tk.Button(root, text="Draw", command=self.draw_result)
        tie_button.pack(pady=7)

        # Start the main loop
        root.mainloop()

    def __init__(self, image1_path, image2_path, window_title="Tournament Time"):
        self.image1 = None
        self.image2 = None
        self.image1_path = image1_path
        self.image2_path = image2_path
        self.window_title = window_title
        self.result = None
        self.window_object = None
        self.build_window()


class TourneyBracket:
    def __init__(self, file_list):
        self.file_list = file_list
        self.winners_list = []
        self.losers_list = []
        self.final_winner = None
        self.run_bracket(file_list)

    def random_file(self, file_list):
        return file_list.pop(random.randint(0, len(file_list) - 1))

    def clean_file_list(self, target_list, removal_list):
        for item in removal_list:
            if item in target_list:
                target_list.remove(item)

    def run_bracket(self, file_list):
        round_winner = []
        if divmod(len(file_list), 2) != 0:
            random_file = self.random_file(file_list)
            self.winners_list.append(random_file)


        random.shuffle(file_list)

        for counter in range(0, len(file_list) - 1, 2):
            image_picker = ImageTourneyWindow(file_list[counter], file_list[counter + 1])
            if image_picker.result == "draw":
                self.losers_list.append(image_picker.image1_path)
                self.losers_list.append(image_picker.image2_path)

            round_winner.append(image_picker.result)

        random.shuffle(round_winner)
        if len(round_winner) > 1:
            self.run_bracket(round_winner)
        else:
            self.final_winner = round_winner.pop()


def get_image_files(directory_path):
    image_files = []
    for filename in os.listdir(directory_path):
        if filename.endswith(".jpg".lower()) or filename.endswith(".png".lower()):
            image_files.append(os.path.join(directory_path, filename))
    return image_files


blah = TourneyBracket(get_image_files(r"images"))
print(blah.final_winner)
