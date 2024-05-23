import tkinter as tk
from PIL import Image, ImageTk
import os, json, random

# model = 'HQ'
# model = 'LQ'

image_paths = []
model_folder = os.path.join('./img', model)
for class_folder in os.listdir(model_folder):
    class_path = os.path.join(model_folder, class_folder)
    if os.path.isdir(class_path):
        for seed in os.listdir(class_path):
            seed_path = os.path.join(class_path, seed)
            if os.path.isdir(seed_path):
                for img in os.listdir(seed_path):
                    img_path = os.path.join(seed_path, img)
                    if img.endswith('.png'):
                        image_paths.append(img_path)

random.shuffle(image_paths)

# Current image index
current_index = 0
total_images = len(image_paths)

# Setup the GUI
root = tk.Tk()
root.title("GAN Labeling App")

# Remaining images indicator
remaining_label = tk.Label(root, text=f"Remaining images: {total_images - current_index}", font=("Helvetica", 22))
remaining_label.pack()

# Display area for MNIST images
canvas = tk.Canvas(root, width=580, height=600)
canvas.pack()


# Function to update image
def update_image(index):
    image = Image.open(image_paths[index])
    image = image.resize((560, 560), Image.BICUBIC)  # 10x zoom
    photo = ImageTk.PhotoImage(image)
    canvas.create_image(10, 10, image=photo, anchor='nw')
    canvas.image = photo  # Keep a reference!
    remaining_label.config(text=f"Remaining images: {total_images - index - 1}")


# Function to handle button click
def button_click(digit):
    global current_index
    path = image_paths[current_index]
    data = {
        "model": model,
        "image_path": path,
        "label": str(digit),
        "accepted": (str(digit) == str(path.split('/')[3]))
    }
    with open(f'./{model}-labels.txt', 'a') as file:
        json.dump(data, file)
        file.write('\n')
    current_index += 1
    if current_index >= len(image_paths):
        tk.messagebox.showinfo("Result", "No more images left. Thank you!")
        root.destroy()
    else:
        update_image(current_index)


def key_press(event):
    # Check if the key press is a number key
    if event.char.isdigit():
        button_click(int(event.char))
    elif event.keysym in ['Return', 'KP_Enter']:
        button_click("Unknown")

root.bind('<Key>', key_press)


# Buttons for labeling
for i in range(10):
    button = tk.Button(root, text=str(i), command=lambda i=i: button_click(i), height=2, width=2)
    button.pack(side=tk.LEFT)

# Add unknown button
unknown_button = tk.Button(root, text="Unknown", command=lambda: button_click("Unknown"), height=2, width=10)
unknown_button.pack(side=tk.LEFT)

update_image(current_index)

root.mainloop()
