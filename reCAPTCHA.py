import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import random
import csv
import glob
import time

INDEX = 0
dataset = ['mimicry_result/cifar-10', 'mimicry_result/f-mnist', 'mimicry_result/mnist', 'mimicry_result/svhn']
categories = [["airplane", "automobile", "bird", "cat", "deer", "dog", "frog", "horse", "ship", "truck"],
              ["T-shirt/top",
              "Trouser",
              "Pullover",
              "Dress",
              "Coat",
              "Sandal",
              "Shirt",
              "Sneaker",
              "Bag",
              "Ankle boot"],
              ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
              ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]]


def enumerate_subfolders(root_folder, folder_depth, num_subfolders):
    fourth_level_folders = []

    # Walk through the directory tree
    for dirpath, dirnames, filenames in os.walk(root_folder):
        # Split the current directory path to count the depth
        relative_path = os.path.relpath(dirpath, root_folder)
        depth = relative_path.count(os.sep)

        # Check if the depth is 2 (3rd level from root)
        if depth == folder_depth:
            image_paths = glob.glob(dirpath +'/*.png')
            fourth_level_folders.append(image_paths[0])

    random.shuffle(fourth_level_folders)
    return fourth_level_folders[: num_subfolders]


def record_csv(path, result):
    filepath = 'result.csv'
    # write CSV to file
    if not os.path.exists(filepath):
        # create csv file header
        with open(filepath, 'w', encoding='UTF8') as f:
            writer = csv.writer(f,
                                delimiter=',',
                                quotechar='"',
                                quoting=csv.QUOTE_MINIMAL,
                                lineterminator='\n')
            # write the header
            writer.writerow(['image_path', 'result'])

    with open(filepath, 'a', encoding='UTF8') as f:
        writer = csv.writer(f,
                            delimiter=',',
                            quotechar='"',
                            quoting=csv.QUOTE_MINIMAL,
                            lineterminator='\n')
        writer.writerow([path, result])


class ReCAPTCHAApp:
    def __init__(self, root):
        self.time_start_str = time.strftime("%m-%d %H:%M", time.localtime())
        self.INDEX = 0
        self.root = root
        self.grid_size = 6
        self.reset_UI()

    def reset_UI(self):
        self.image_paths = enumerate_subfolders(dataset[self.INDEX],
                                                folder_depth=3,
                                                num_subfolders=self.grid_size * self.grid_size)
        self.selected_images = set()
        self.disabled_images = dict()
        self.current_digit = 0

        self.root.title("reCAPTCHA App")
        self.create_widgets()
        self.display_images()

    def create_widgets(self):
        self.label = tk.Label(self.root, text=f"Select all images containing >>> {categories[self.INDEX][self.current_digit]} <<<\n " +
                                                "The unselected images will be regarded as unknown type.\n" +
                                                "Press choose carefully, re-selection is not supported :)"
                                              , font=("Helvetica", 16))
        self.label.pack(pady=10)

        self.canvas_frame = tk.Frame(self.root)
        self.canvas_frame.pack()

        self.buttons = [[None for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.image_refs = [[None for _ in range(self.grid_size)] for _ in range(self.grid_size)]

        for i in range(self.grid_size):
            for j in range(self.grid_size):
                self.buttons[i][j] = tk.Button(self.canvas_frame, command=lambda row=i, col=j: self.select_image(row, col), borderwidth=2, highlightthickness=2)
                self.buttons[i][j].grid(row=i, column=j, padx=2, pady=2)

        self.submit_button = tk.Button(self.root, text="Submit", command=self.submit_selection, font=("Helvetica", 14))
        self.submit_button.pack(pady=10)

    def display_images(self):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                image = Image.open(self.image_paths[i * self.grid_size + j])
                image = image.resize((100, 100), Image.BICUBIC)
                photo = ImageTk.PhotoImage(image)
                self.buttons[i][j].config(image=photo, state=tk.NORMAL)
                self.buttons[i][j].image = photo
                idx = i * self.grid_size + j
                if idx in self.disabled_images.keys():
                    self.buttons[i][j].config(bg='gray', state=tk.DISABLED)

    def select_image(self, i, j):
        idx = i * self.grid_size + j
        if idx in self.disabled_images.keys():
            return
        if idx in self.selected_images:
            self.buttons[i][j].config(bg='light grey', borderwidth=4, highlightthickness=2, highlightbackground="light grey")
            self.selected_images.remove(idx)
        else:
            self.buttons[i][j].config(bg='green', borderwidth=4, highlightthickness=4, highlightbackground="green")
            self.selected_images.add(idx)
        print(f"Selected images: {self.selected_images}")

    def submit_selection(self):
        for idx in self.selected_images:
            self.disabled_images[idx] = self.current_digit
            i, j = divmod(idx, self.grid_size)
            self.buttons[i][j].config(bg='gray', state=tk.DISABLED)
            record_csv(self.image_paths[idx], self.current_digit)
            # print(f"Disabled images: {self.disabled_images}")
            print(f"Selected images: {self.image_paths[idx]}")
        self.selected_images.clear()
        self.current_digit += 1
        if self.current_digit > 9:
            if self.INDEX < 3:
                self.INDEX += 1
                print("reset")
                self.clear_widgets()
                self.reset_UI()

            else:
                messagebox.showinfo("Finished", "You have completed the task. Thank you!")
                self.root.quit()

        else:
            self.label.config(text=f"Select all images containing >>> {categories[self.INDEX][self.current_digit]} <<<\n " +
                                                "The unselected images will be regarded as unknown type.\n" +
                                                "Press choose carefully, re-selection is not supported :)")

    def clear_widgets(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    """def reset_selection(self):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if (i * self.grid_size + j) not in self.disabled_images:
                    self.buttons[i][j].config(bg='light grey', borderwidth=2, highlightthickness=2, highlightbackground="light grey")
"""

if __name__ == "__main__":
    root = tk.Tk()
    app = ReCAPTCHAApp(root)

    root.mainloop()