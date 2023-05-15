import os
import random
import tkinter as tk
from PIL import ImageTk, Image

root = tk.Tk()
root.title("My Window")
root.geometry("1000x1000")

# Get a list of all the image file names in the "images" folder
image_folder = "images"
image_files = [os.path.join(image_folder, f) for f in os.listdir(image_folder) if os.path.isfile(os.path.join(image_folder, f))]

# Select two random images from the list
random_images = random.sample(image_files, 2)

# Load the images using Pillow
image1 = Image.open(random_images[0])
image2 = Image.open(random_images[1])

# Resize the images to fit in the window
width = 250
height1 = int((width / float(image1.size[0])) * image1.size[1])
height2 = int((width / float(image2.size[0])) * image2.size[1])
image1 = image1.resize((width, height1))
image2 = image2.resize((width, height2))

# Convert the images to Tkinter PhotoImage objects
tk_image1 = ImageTk.PhotoImage(image1)
tk_image2 = ImageTk.PhotoImage(image2)
# Create a new frame for the radio buttons
radio_frame = tk.Frame(root)
radio_frame.pack()

# Create the radio buttons
left_image_rb = tk.Radiobutton(radio_frame, text="Left Image")
left_image_rb.pack(side="left")
center_image_rb = tk.Radiobutton(radio_frame, text="Center Image")
center_image_rb.pack(side="left")
right_image_rb = tk.Radiobutton(radio_frame, text="Right Image")
right_image_rb.deselect()
right_image_rb.pack(side="left")

# Create two labels to display the images
label1 = tk.Label(root, image=tk_image1)
label1.pack(side="left")
label2 = tk.Label(root, image=tk_image2)
label2.pack(side="left")

root.mainloop()