import tkinter as tk
from tkinter import Label, Button
from PIL import Image, ImageTk
import requests
import os
import random

class CatFactsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cat Facts App")

        # API endpoint for cat facts
        self.api_url = "https://meowfacts.herokuapp.com/"

        # Path to the folder containing cat images
        self.image_folder_path = "images/"

        # List to store image filenames
        self.image_filenames = []

        # Load cat images
        self.load_cat_images()

        # Initialize GUI components
        self.create_widgets()

    def load_cat_images(self):
        try:
            # Get a list of all files in the image folder
            self.image_filenames = [file for file in os.listdir(self.image_folder_path) if file.endswith(('.png', '.jpg', '.jpeg'))]
        except Exception as e:
            print(f"Error loading cat images: {e}")

    def create_widgets(self):
        # Cat image placeholder
        self.cat_image_label = Label(self.root)
        self.cat_image_label.pack(pady=10)

        # Cat fact label
        self.cat_fact_label = Label(self.root, wraplength=400, justify="left", font=("Helvetica", 10))
        self.cat_fact_label.pack(pady=10)

        # Regenerate button
        self.regenerate_button = Button(self.root, text="Regenerate", command=self.regenerate_cat_fact)
        self.regenerate_button.pack(pady=10)

        # Initial cat fact fetch
        self.regenerate_cat_fact()

    def regenerate_cat_fact(self):
        try:
            # Fetch cat fact from the API
            response = requests.get(self.api_url)
            data = response.json()

            if response.status_code == 200:
                cat_fact = data['data'][0]
                self.cat_fact_label.config(text=cat_fact)

                # Display a random cat image
                if len(self.image_filenames) > 0:
                    random_image_filename = random.choice(self.image_filenames)
                    cat_image_path = os.path.join(self.image_folder_path, random_image_filename)
                    self.display_cat_image(cat_image_path)
                else:
                    print("No cat images found in the folder.")
                    self.display_default_image()

            else:
                self.cat_fact_label.config(text=f"Error: {data.get('message', 'Unknown error')}")
                self.display_default_image()

        except Exception as e:
            self.cat_fact_label.config(text=f"An error occurred: {e}")
            self.display_default_image()

    def display_cat_image(self, image_path):
        try:
            # Open the image using Pillow
            image = Image.open(image_path)
            image = ImageTk.PhotoImage(image)

            # Update cat image label
            self.cat_image_label.config(image=image)
            self.cat_image_label.image = image  # Keep a reference to avoid garbage collection

        except Exception as e:
            print(f"Error loading image: {e}")
            self.display_default_image()

    def display_default_image(self):
        # Display a default image if there's an error loading the cat image
        default_image = Image.open("images/error.jpg")
        default_image = ImageTk.PhotoImage(default_image)
        self.cat_image_label.config(image=default_image)
        self.cat_image_label.image = default_image

if __name__ == "__main__":
    root = tk.Tk()
    app = CatFactsApp(root)
    root.mainloop()
