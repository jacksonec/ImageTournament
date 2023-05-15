import os
import random
import tkinter as tk
from PIL import ImageTk, Image

class image_tourney_window:
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

        root = tk.Tk()
        root.title("Tournament Time!")
        root.geometry(f"{win_width}x{win_height}")

        image_frame = tk.Frame(root)
        image_frame.pack()

        tk_image1 = ImageTk.PhotoImage(self.image1)
        tk_image2 = ImageTk.PhotoImage(self.image2)

        image_display1 = tk.Label(image_frame, image=tk_image1)
        image_display2 = tk.Label(image_frame, image=tk_image2)

        image_display1.pack(side="left")
        image_display2.pack(side="left")

        tie_button = tk.Button(root, text="Draw!", command=self.draw)
        tie_button.
        tie_button.pack()

        # Start the main loop
        root.mainloop()

    def draw(self):
        pass

    def __init__(self, image1_path, image2_path, window_title="Tournament Time"):
        self.image1 = None
        self.image2 = None
        self.image1_path = image1_path
        self.image2_path = image2_path
        self.window_title = window_title
        self.build_window()



blah = image_tourney_window(r"images\1.jpg", r"images\2.jpg")