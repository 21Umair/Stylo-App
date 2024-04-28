
import tkinter as tk
from tkinter import Tk, Label, Button, Frame, filedialog, messagebox, ttk, colorchooser
from PIL import Image, ImageTk, ImageDraw, ImageFilter, ImageEnhance, ImageOps
import glob
import tensorflow_hub as hub
import tensorflow 
import tensorflow as tf
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import cv2
import os
import datetime
import random
import string
from skimage.metrics import mean_squared_error
from scipy.ndimage import median_filter
from scipy.ndimage import gaussian_filter
import skimage.color
import matplotlib.colors
from skimage import io, filters
from tkinter import Tk, Canvas, filedialog, Entry, Button, messagebox
from PIL import Image, ImageDraw, ImageFont, ImageTk



root = None  # Global variable for the root window

def open_next_screen():
    global root  # Access the global root variable
    root.destroy()  # Close the current screen
    create_second_screen()

def create_screen():
    global root  # Access the global root variable

    # Create the GUI window
    root = tk.Tk()
    root.title("Stylo")
    root.geometry("900x600")
    root.configure(bg='#350505')
    root.resizable(False, False)


    # Open the video file using VideoCapture
    #video = cv2.VideoCapture("C:\\Users\\Umair\\Desktop\\TICS P\\Stylo.avi")

    script_dir = os.path.dirname(os.path.abspath(__file__))
    video_path = os.path.join(script_dir, 'Stylo.avi')
    video = cv2.VideoCapture(video_path)


    # Read the first frame of the video
    success, frame = video.read()

    # Convert the frame to RGB color space
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Create an ImageTk.PhotoImage from the frame
    photo = ImageTk.PhotoImage(image=Image.fromarray(frame))

    # Create a label to display the animation
    animation_label = tk.Label(root, image=photo, bg='#350505')
    animation_label.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

    def update_frame():
        # Read the next frame of the video
        success, frame = video.read()

        if success:
            # Convert the frame to RGB color space
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Create an ImageTk.PhotoImage from the frame
            photo = ImageTk.PhotoImage(image=Image.fromarray(frame))

            # Update the label with the new frame
            animation_label.configure(image=photo)
            animation_label.image = photo

            # Schedule the next frame update
            animation_label.after(30, update_frame)

    # Start updating the frames
    update_frame()



    start_label = tk.Label(root, text = "Click to start______________________________________________________________________________________⥤", font=("Helvetica", 9), bg='#350505', fg='grey')
    start_label.place(x=50, y=540, width=680, height=20)

    # Create the "Let's Style" button
    style_button = tk.Button(root, text="Lets Style", font=("Helvetica", 16), bg='#652525', fg='white', relief=tk.FLAT, padx=0, pady=0, command=open_next_screen)
    style_button.place(relx=0.95, rely=0.95, anchor=tk.SE)

    # Run the GUI event loop
    root.mainloop()


def create_second_screen():
    # Create the second screen window
    second_screen = tk.Tk()
    second_screen.title("Stylo")
    second_screen.geometry("900x600")
    second_screen.configure(bg='#350505')
    second_screen.resizable(False, False)

    # Create the top frame
    top_frame = tk.Frame(second_screen, bg='#494242', height=11)
    top_frame.pack(side=tk.TOP, fill=tk.X)



    def tools():

        global tool_image_frame
        tool_image_frame = None

        #tool_window = tk.Tk()
        tool_window = tk.Toplevel()
        tool_window.geometry("900x700")
        tool_window.title("Tools")
        tool_window.config(bg='#350505')
        tool_window.resizable(False, False)

        # Create the top frame
        tool_top_frame = tk.Frame(tool_window, bg='#494242', height=11)
        tool_top_frame.pack(side=tk.TOP, fill=tk.X)

        tool_image_frame = tk.Frame(tool_window, width=620, height=620, bg='#2C0D0D')
        tool_image_frame.place(x=450, y=365, anchor=tk.CENTER)

        global image1
        image1 = None
        global image1_path 
        image1_path = None
        global filtered_image
        filtered_image = None
        global resized_image
        resized_image = None

        global photo1
        photo1 = None
        
        current_image_label = None
        main_image_path = None

        def select_image():
            nonlocal current_image_label, main_image_path
            global image1, image1_path, resized_image
            # Open a file dialog to select an image file
            filetypes = [("Image Files", "*.jpg;*.jpeg")]
            image_path = tk.filedialog.askopenfilename(filetypes=filetypes)
            image1_path = image_path

            # Check if an image file was selected
            if image_path:
                # Load the selected image file using PIL
                image = Image.open(image_path)
                image1 = image
                # Resize the image to fit the tool_image_frame
                width, height = image.size
                max_size = min(tool_image_frame.winfo_width(), tool_image_frame.winfo_height())
                if width > height:
                    new_width = max_size
                    new_height = int((new_width / width) * height)
                else:
                    new_height = max_size
                    new_width = int((new_height / height) * width)
                resized_image = image.resize((new_width, new_height))
                

                # Create a PhotoImage object from the resized image
                photo = ImageTk.PhotoImage(resized_image)
                # image_resized = photo

                # Create a label inside the tool_image_frame and assign the PhotoImage to its image attribute
                label = tk.Label(tool_image_frame, image=photo)
                label.image = photo  # Store a reference to prevent garbage collection
                label.pack()


                # Remove the previous image label, if it exists
                if current_image_label:
                    current_image_label.pack_forget()

                # Update the current image label
                current_image_label = label
                current_image_label.image_path = image_path

                # Update the main image path
                main_image_path = image_path



        open_button = tk.Button(tool_top_frame, text="Open", font=("Helvetica", 9), bg='#494242', fg='white', relief=tk.FLAT, command=select_image)
        open_button.pack(side=tk.LEFT, padx=10, pady=2)



        def jumpfunc():
            global resized_image
            save_image_to_gallery(resized_image)

        # Function to handle saving the image to the gallery directory
        def save_image_to_gallery(image):
            if image is None:
                tk.messagebox.showerror("Error", "Please select an image first.")
                return
            # Open a file dialog to prompt the user for the image name
            filetypes = [("JPEG Image", "*.jpg")]
            image_path = tk.filedialog.asksaveasfilename(filetypes=filetypes, defaultextension=".jpg")
            
            # Check if the user selected a file name
            if image_path:
                image.save(image_path)
                tk.messagebox.showinfo("Success", "Image saved.")
            else:
                tk.messagebox.showerror("Error", "File not saved.")

        save_button = tk.Button(tool_top_frame, text="Save", font=("Helvetica", 9), bg='#494242', fg='white', relief=tk.FLAT, command=jumpfunc)
        save_button.pack(side=tk.LEFT, padx=10, pady=2)


        def rotate_image():
            global image1, tool_image_frame, resized_image
            nonlocal current_image_label

            if resized_image is None:
                messagebox.showerror("Error", "Please select an image first.")
                return
            elif image1:
                # Rotate the image by 90 degrees clockwise
                image2 = resized_image.rotate(-90)
                if current_image_label:
                    current_image_label.pack_forget()

                # Update the resized_image variable with the rotated image
                resized_image = image2.resize(resized_image.size)

                # Create a PhotoImage object from the rotated image
                photo = ImageTk.PhotoImage(image2)


                # Create a label inside the tool_image_frame and assign the PhotoImage to its image attribute
                label = tk.Label(tool_image_frame, image=photo)
                label.image = photo  # Store a reference to prevent garbage collection
                label.pack()

                # Update the current image label
                current_image_label = label

                # Update the tool_window layout to adjust for the new image size
                tool_window.update()



        rotate_button = tk.Button(tool_top_frame, text="Rotate", font=("Helvetica", 9), bg='#494242', fg='white', relief=tk.FLAT, command=rotate_image)
        rotate_button.pack(side=tk.LEFT, padx=10, pady=2)

        def flip_image_horizontally():
            global image1, tool_image_frame, resized_image
            nonlocal current_image_label
            if resized_image is None:
                messagebox.showerror("Error", "Please select an image first.")
                return
            elif image1:
                # Flip the image horizontally
                image2 = resized_image.transpose(Image.FLIP_LEFT_RIGHT)
                if current_image_label:
                    current_image_label.pack_forget()

                # Update the resized_image variable with the flipped image
                resized_image = image2.resize(resized_image.size)

                # Create a PhotoImage object from the flipped image
                photo = ImageTk.PhotoImage(image2)

                # Create a label inside the tool_image_frame and assign the PhotoImage to its image attribute
                label = tk.Label(tool_image_frame, image=photo)
                label.image = photo  # Store a reference to prevent garbage collection
                label.pack()

                # Update the current image label
                current_image_label = label

                # Update the tool_window layout to adjust for the new image size
                tool_window.update()


        fliph_button = tk.Button(tool_top_frame, text="Flip H", font=("Helvetica", 9), bg='#494242', fg='white', relief=tk.FLAT, command=flip_image_horizontally)
        fliph_button.pack(side=tk.LEFT, padx=10, pady=2)


        def flip_image_vertically():
            global image1, tool_image_frame, resized_image
            nonlocal current_image_label
            if resized_image is None:
                messagebox.showerror("Error", "Please select an image first.")
                return
            elif image1:
                # Flip the image vertically
                image2 = resized_image.transpose(Image.FLIP_TOP_BOTTOM)
                if current_image_label:
                    current_image_label.pack_forget()

                # Update the resized_image variable with the flipped image
                resized_image = image2.resize(resized_image.size)

                # Create a PhotoImage object from the flipped image
                photo = ImageTk.PhotoImage(image2)

                # Create a label inside the tool_image_frame and assign the PhotoImage to its image attribute
                label = tk.Label(tool_image_frame, image=photo)
                label.image = photo  # Store a reference to prevent garbage collection
                label.pack()

                # Update the current image label
                current_image_label = label

                # Update the tool_window layout to adjust for the new image size
                tool_window.update()


        flipv_button = tk.Button(tool_top_frame, text="Flip V", font=("Helvetica", 9), bg='#494242', fg='white', relief=tk.FLAT, command=flip_image_vertically)
        flipv_button.pack(side=tk.LEFT, padx=10, pady=2)




        def refresh():
            tool_window.destroy()
            tools()

        refresh_button = tk.Button(tool_top_frame, text="Refresh", font=("Helvetica", 9), bg='#494242', fg='white', relief=tk.FLAT, command=refresh)
        refresh_button.pack(side=tk.RIGHT, padx=10, pady=2)

            


        tool_window.mainloop()


    # Create the options buttons for top frame
    files_button = tk.Button(top_frame, text="Tools", font=("Helvetica", 9), bg='#494242', fg='white', relief=tk.FLAT, command=tools)
    files_button.pack(side=tk.LEFT, padx=10, pady=2)





    def color_tools():

        global color_tool_image_frame
        color_tool_image_frame = None

        #color_tool_window = tk.Tk()
        color_tool_window = tk.Toplevel()
        color_tool_window.geometry("900x700")
        color_tool_window.title("Colors")
        color_tool_window.config(bg='#350505')
        color_tool_window.resizable(False, False)

        # Create the top frame
        tool_top_frame = tk.Frame(color_tool_window, bg='#494242', height=11)
        tool_top_frame.pack(side=tk.TOP, fill=tk.X)

        color_tool_image_frame = tk.Frame(color_tool_window, width=620, height=620, bg='#2C0D0D')
        color_tool_image_frame.place(x=450, y=365, anchor=tk.CENTER)

        global image1
        image1 = None
        global image1_path 
        image1_path = None
        global filtered_image
        filtered_image = None
        global resized_image
        resized_image = None

        global photo1
        photo1 = None
        
        current_image_label = None
        main_image_path = None

        def select_image():
            nonlocal current_image_label, main_image_path
            global image1, image1_path, resized_image
            # Open a file dialog to select an image file
            filetypes = [("Image Files", "*.jpg;*.jpeg")]
            image_path = tk.filedialog.askopenfilename(filetypes=filetypes)
            image1_path = image_path

            # Check if an image file was selected
            if image_path:
                # Load the selected image file using PIL
                image = Image.open(image_path)

                # Resize the image to fit the color_tool_image_frame
                width, height = image.size
                max_size = min(color_tool_image_frame.winfo_width(), color_tool_image_frame.winfo_height())
                if width > height:
                    new_width = max_size
                    new_height = int((new_width / width) * height)
                else:
                    new_height = max_size
                    new_width = int((new_height / height) * width)
                resized_image = image.resize((new_width, new_height))

                # Create a PhotoImage object from the resized image
                photo = ImageTk.PhotoImage(resized_image)

                # Create a label inside the color_tool_image_frame and assign the PhotoImage to its image attribute
                label = tk.Label(color_tool_image_frame, image=photo)
                label.image = photo  # Store a reference to prevent garbage collection
                label.pack()

                # Remove the previous image label, if it exists
                if current_image_label:
                    current_image_label.pack_forget()

                # Update the current image label
                current_image_label = label
                current_image_label.image_path = image_path

                # Update the main image path
                main_image_path = image_path



        open_button = tk.Button(tool_top_frame, text="Open", font=("Helvetica", 9), bg='#494242', fg='white', relief=tk.FLAT, command=select_image)
        open_button.pack(side=tk.LEFT, padx=10, pady=2)



        def jumpfunc():
            global resized_image
            # Save the stylized image to a directory
            save_image_to_gallery(resized_image)

        # Function to handle saving the image to the gallery directory
        def save_image_to_gallery(image):
            if image is None:
                tk.messagebox.showerror("Error", "Please select an image first.")
                return
            # Open a file dialog to prompt the user for the image name
            filetypes = [("JPEG Image", "*.jpg")]
            image_path = tk.filedialog.asksaveasfilename(filetypes=filetypes, defaultextension=".jpg")
            
            # Check if the user selected a file name
            if image_path:
                image.save(image_path)
                tk.messagebox.showinfo("Success", "Image saved.")
            else:
                tk.messagebox.showerror("Error", "File not saved.")

        save_button = tk.Button(tool_top_frame, text="Save", font=("Helvetica", 9), bg='#494242', fg='white', relief=tk.FLAT, command=jumpfunc)
        save_button.pack(side=tk.LEFT, padx=10, pady=2)



        def slider_changed(value):
            global active_button, adjusted_contrast_image, adjusted_brightness_image, adjusted_saturation_image, adjusted_vibrance_image, adjusted_warmth_image
            print("Slider value:", value)
            if active_button == "Contrast":
                change_contrast(value)
            elif active_button == "Brightness":
                change_brightness(value)
            elif active_button == "Saturation":
                change_saturation(value)
            elif active_button == "Vibrance":
                change_vibrance(value)
            elif active_button == "Warmth":
                change_warmth(value)

            
            # Update the adjusted image variables based on the active button
            if active_button == "Contrast":
                adjusted_contrast_image = current_image_label.image
            elif active_button == "Brightness":
                adjusted_brightness_image = current_image_label.image
            elif active_button == "Saturation":
                adjusted_saturation_image = current_image_label.image
            elif active_button == "Vibrance":
                adjusted_vibrance_image = current_image_label.image
            elif active_button == "Warmth":
                adjusted_warmth_image = current_image_label.image



        def set_active_button(button):
            global active_button, contrast_level, brightness_level, saturation_level, vibrance_level, warmth_level
            if active_button == "Contrast":
                contrast_level = slider.get()
            elif active_button == "Brightness":
                brightness_level = slider.get()
            elif active_button == "Saturation":
                saturation_level = slider.get()
            elif active_button == "Vibrance":
                vibrance_level = slider.get()
            elif active_button == "Warmth":
                warmth_level = slider.get()


            active_button = button
            # Update the slider command based on the active button
            if active_button == "Contrast":
                if resized_image is None:
                    messagebox.showerror("Error", "Please select an image first.")
                    return
                else:
                    slider.set(contrast_level)
                    slider.configure(command=lambda value: change_contrast(value))
            elif active_button == "Brightness":
                if resized_image is None:
                    messagebox.showerror("Error", "Please select an image first.")
                    return
                else:
                    slider.set(brightness_level)
                    slider.configure(command=lambda value: change_brightness(value))
            elif active_button == "Saturation":
                if resized_image is None:
                    messagebox.showerror("Error", "Please select an image first.")
                    return
                else:
                    slider.set(saturation_level)
                    slider.configure(command=lambda value: change_saturation(value))
            elif active_button == "Vibrance":
                if resized_image is None:
                    messagebox.showerror("Error", "Please select an image first.")
                    return
                else:
                    slider.set(vibrance_level)
                    slider.configure(command=lambda value: change_vibrance(value))
            elif active_button == "Warmth":
                if resized_image is None:
                    messagebox.showerror("Error", "Please select an image first.")
                    return
                else:
                    slider.set(warmth_level)
                    slider.configure(command=lambda value: change_warmth(value))
            
            # Show or hide the slider based on the active button
            if active_button is None:
                slider.place_forget()
            else:
                slider.place(x=50, y=200)


        slider = tk.Scale(color_tool_window, from_=-100, to=100, orient=tk.VERTICAL, length=200, command=slider_changed, bg = "grey")



        global contrast_level
        contrast_level = 0

        global brightness_level
        brightness_level = 0

        global saturation_level
        saturation_level = 0

        global vibrance_level
        vibrance_level = 0

        global warmth_level
        warmth_level = 0

        global active_button
        active_button = None



        adjusted_contrast_level = 0
        adjusted_brightness_level = 0
        adjusted_saturation_level = 0
        adjusted_vibrance_level = 0
        adjusted_warmth_level = 0

        def change_contrast(value):
            global active_button, resized_image
            nonlocal current_image_label, adjusted_contrast_level

            adjusted_contrast_level = int(value)
            update_displayed_image()

            if resized_image is None:
                messagebox.showerror("Error", "Please select an image first.")
                return



        contrast_button = tk.Button(tool_top_frame, text="Contrast", font=("Helvetica", 9), bg='#494242', fg='white', relief=tk.FLAT, command=lambda: set_active_button("Contrast"))
        contrast_button.pack(side=tk.LEFT, padx=10, pady=2)


        def change_brightness(value):
            global active_button, resized_image
            nonlocal current_image_label, adjusted_brightness_level


            adjusted_brightness_level = int(value)
            if resized_image is None:
                messagebox.showerror("Error", "Please select an image first.")
                return
            update_displayed_image()


        brightness_button = tk.Button(tool_top_frame, text="Brightness", font=("Helvetica", 9), bg='#494242', fg='white', relief=tk.FLAT, command=lambda: set_active_button("Brightness"))
        brightness_button.pack(side=tk.LEFT, padx=10, pady=2)


        def change_saturation(value):
            global active_button, resized_image
            nonlocal current_image_label, adjusted_saturation_level

            adjusted_saturation_level = int(value)

            if resized_image is None:
                messagebox.showerror("Error", "Please select an image first.")
                return

            update_displayed_image()



        saturation_button = tk.Button(tool_top_frame, text="Saturation", font=("Helvetica", 9), bg='#494242', fg='white', relief=tk.FLAT, command=lambda: set_active_button("Saturation"))
        saturation_button.pack(side=tk.LEFT, padx=10, pady=2)


        def change_vibrance(value):
            global active_button, resized_image
            nonlocal current_image_label, adjusted_vibrance_level


            adjusted_vibrance_level = int(value)
            update_displayed_image()

            if resized_image is None:
                messagebox.showerror("Error", "Please select an image first.")
                return

        vibrance_button = tk.Button(tool_top_frame, text="Vibrance", font=("Helvetica", 9), bg='#494242', fg='white', relief=tk.FLAT, command=lambda: set_active_button("Vibrance"))
        vibrance_button.pack(side=tk.LEFT, padx=10, pady=2)



        def change_warmth(value):
            global active_button, resized_image
            nonlocal current_image_label, adjusted_warmth_level

            adjusted_warmth_level = int(value)
            update_displayed_image()

            if resized_image is None:
                messagebox.showerror("Error", "Please select an image first.")
                return
            
        warmth_button = tk.Button(tool_top_frame, text="Warmth", font=("Helvetica", 9), bg='#494242', fg='white', relief=tk.FLAT, command=lambda: set_active_button("Warmth"))
        warmth_button.pack(side=tk.LEFT, padx=10, pady=2)



        
        def update_displayed_image():
            global resized_image
            nonlocal current_image_label, adjusted_contrast_level, adjusted_brightness_level, adjusted_saturation_level, adjusted_vibrance_level, adjusted_warmth_level

            # Check if an image is loaded
            if resized_image is None:
                return

            # Create a copy of the resized image
            adjusted_image = resized_image.copy()

            # Apply the contrast adjustment if non-zero
            if adjusted_contrast_level != 0:
                enhancer = ImageEnhance.Contrast(adjusted_image)
                adjusted_image = enhancer.enhance(1 + adjusted_contrast_level / 100)

            # Apply the brightness adjustment if non-zero
            if adjusted_brightness_level != 0:
                enhancer = ImageEnhance.Brightness(adjusted_image)
                adjusted_image = enhancer.enhance(1 + adjusted_brightness_level / 100)

            # Apply the saturation adjustment if non-zero
            if adjusted_saturation_level != 0:
                image_hsv = adjusted_image.convert("HSV")
                h, s, v = image_hsv.split()
                adjusted_s = s.point(lambda x: x + adjusted_saturation_level)
                adjusted_hsv = Image.merge("HSV", (h, adjusted_s, v))
                adjusted_image = adjusted_hsv.convert("RGB")

            # Apply the vibrance adjustment if non-zero
            if adjusted_vibrance_level != 0:
                #adjusted_image = adjusted_image.copy()
                enhancer = ImageEnhance.Color(adjusted_image)
                adjusted_image = enhancer.enhance(1 + adjusted_vibrance_level / 100)

            # Apply the warmth adjustment if non-zero
            if adjusted_warmth_level != 0:
                image_lab = adjusted_image.convert("LAB")
                l, a, b = image_lab.split()
                
                # Adjust the A channel (green-red component) to add warmth
                adjusted_a = a.point(lambda x: x + adjusted_warmth_level)
                
                # Merge the channels back into a LAB image
                adjusted_lab = Image.merge("LAB", (l, adjusted_a, b))
                
                # Convert the adjusted LAB image back to RGB
                adjusted_image = adjusted_lab.convert("RGB")




            # Update the displayed image
            photo = ImageTk.PhotoImage(adjusted_image)
            current_image_label.configure(image=photo)
            current_image_label.image = photo



        def refresh():
            color_tool_window.destroy()
            color_tools()

        refresh_button = tk.Button(tool_top_frame, text="Refresh", font=("Helvetica", 9), bg='#494242', fg='white', relief=tk.FLAT, command=refresh)
        refresh_button.pack(side=tk.RIGHT, padx=10, pady=2)

            


        color_tool_window.mainloop()

    files_button = tk.Button(top_frame, text="Colors", font=("Helvetica", 9), bg='#494242', fg='white', relief=tk.FLAT, command=color_tools)
    files_button.pack(side=tk.LEFT, padx=10, pady=2)


    def attributes():

        global tool_image_frame
        tool_image_frame = None

        #attribute_window = tk.Tk()
        attribute_window = tk.Toplevel()
        attribute_window.geometry("900x700")
        attribute_window.title("Attributes")
        attribute_window.config(bg='#350505')
        attribute_window.resizable(False, False)

        # Create the top frame
        tool_top_frame = tk.Frame(attribute_window, bg='#494242', height=11)
        tool_top_frame.pack(side=tk.TOP, fill=tk.X)

        tool_image_frame = tk.Frame(attribute_window, width=620, height=620, bg='#2C0D0D')
        tool_image_frame.place(x=450, y=365, anchor=tk.CENTER)

        global image1
        image1 = None
        global image1_path 
        image1_path = None
        global filtered_image
        filtered_image = None
        global resized_image
        resized_image = None

        global photo1
        photo1 = None
        
        current_image_label = None
        main_image_path = None

        def select_image():
            nonlocal current_image_label, main_image_path
            global image1, image1_path, resized_image
            # Open a file dialog to select an image file
            filetypes = [("Image Files", "*.jpg;*.jpeg")]
            image_path = tk.filedialog.askopenfilename(filetypes=filetypes)
            image1_path = image_path

            # Check if an image file was selected
            if image_path:
                # Load the selected image file using PIL
                image = Image.open(image_path)
                image1 = image
                # Resize the image to fit the tool_image_frame
                width, height = image.size
                max_size = min(tool_image_frame.winfo_width(), tool_image_frame.winfo_height())
                if width > height:
                    new_width = max_size
                    new_height = int((new_width / width) * height)
                else:
                    new_height = max_size
                    new_width = int((new_height / height) * width)
                resized_image = image.resize((new_width, new_height))
                

                # Create a PhotoImage object from the resized image
                photo = ImageTk.PhotoImage(resized_image)
                # image_resized = photo

                # Create a label inside the tool_image_frame and assign the PhotoImage to its image attribute
                label = tk.Label(tool_image_frame, image=photo)
                label.image = photo  # Store a reference to prevent garbage collection
                label.pack()


                # Remove the previous image label, if it exists
                if current_image_label:
                    current_image_label.pack_forget()

                # Update the current image label
                current_image_label = label
                current_image_label.image_path = image_path

                # Update the main image path
                main_image_path = image_path



        open_button = tk.Button(tool_top_frame, text="Open", font=("Helvetica", 9), bg='#494242', fg='white', relief=tk.FLAT, command=select_image)
        open_button.pack(side=tk.LEFT, padx=10, pady=2)



        def jumpfunc():
            global resized_image
            # Save the stylized image to a directory
            save_image_to_gallery(resized_image)

        # Function to handle saving the image to the gallery directory
        def save_image_to_gallery(image):
            if image is None:
                tk.messagebox.showerror("Error", "Please select an image first.")
                return
            # Open a file dialog to prompt the user for the image name
            filetypes = [("JPEG Image", "*.jpg")]
            image_path = tk.filedialog.asksaveasfilename(filetypes=filetypes, defaultextension=".jpg")
            
            # Check if the user selected a file name
            if image_path:
                image.save(image_path)
                tk.messagebox.showinfo("Success", "Image saved.")
            else:
                tk.messagebox.showerror("Error", "File not saved.")

        save_button = tk.Button(tool_top_frame, text="Save", font=("Helvetica", 9), bg='#494242', fg='white', relief=tk.FLAT, command=jumpfunc)
        save_button.pack(side=tk.LEFT, padx=10, pady=2)



        def slider_changed(value):
            global active_button, adjusted_sharp_image, adjusted_noise_image, adjusted_exposure_image
            print("Slider value:", value)
            if active_button == "Sharpness":
                change_custom_sharpness(value)
            elif active_button == "Noice Reduction":
                change_custom_noise(value)
            elif active_button == "Exposure":
                change_custom_exposure(value)
           

            
            # Update the adjusted image variables based on the active button
            if active_button == "Sharpness":
                adjusted_sharp_image = current_image_label.image
            elif active_button == "Noice Reduction":
                adjusted_noise_image = current_image_label.image
            elif active_button == "Exposure":
                adjusted_exposure_image = current_image_label.image
            



        def set_active_button(button):
            global active_button, sharpness_level, noise_level, exposure_level
            if active_button == "Sharpness":
                sharpness_level = slider.get()
            elif active_button == "Noice Reduction":
                noise_level = slider.get()
            elif active_button == "Exposure":
                exposure_level = slider.get()


            active_button = button
            # Update the slider command based on the active button
            if active_button == "Sharpness":
                if resized_image is None:
                    messagebox.showerror("Error", "Please select an image first.")
                    return
                else:
                    slider.set(sharpness_level)
                    slider.configure(command=lambda value: change_custom_sharpness(value))
            elif active_button == "Noice Reduction":
                if resized_image is None:
                    messagebox.showerror("Error", "Please select an image first.")
                    return
                else:
                    slider.set(noise_level)
                    slider.configure(command=lambda value: change_custom_noise(value))
            elif active_button == "Exposure":
                if resized_image is None:
                    messagebox.showerror("Error", "Please select an image first.")
                    return
                else:
                    slider.set(exposure_level)
                    slider.configure(command=lambda value: change_custom_exposure(value))
            
            
            # Show or hide the slider based on the active button
            if active_button is None:
                slider.place_forget()
            else:
                slider.place(x=50, y=200)


        slider = tk.Scale(attribute_window, from_=-100, to=100, orient=tk.VERTICAL, length=200, command=slider_changed, bg = "grey")



        global sharpness_level
        sharpness_level = 0

        global noise_level
        noise_level = 0

        global exposure_level
        exposure_level = 0



        global active_button
        active_button = None



        adjusted_sharpness_level = 0
        adjusted_noise_level = 0
        adjusted_exposure_level = 0


        def change_custom_sharpness(value):
            global active_button, resized_image
            nonlocal current_image_label, adjusted_sharpness_level

            adjusted_sharpness_level = int(value)
            update_displayed_image()

            if resized_image is None:
                messagebox.showerror("Error", "Please select an image first.")
                return



        contrast_button = tk.Button(tool_top_frame, text="Sharp/Smooth", font=("Helvetica", 9), bg='#494242', fg='white', relief=tk.FLAT, command=lambda: set_active_button("Sharpness"))
        contrast_button.pack(side=tk.LEFT, padx=10, pady=2)


        def change_custom_noise(value):
            global active_button, resized_image
            nonlocal current_image_label, adjusted_noise_level


            adjusted_noise_level = int(value)
            if resized_image is None:
                messagebox.showerror("Error", "Please select an image first.")
                return
            update_displayed_image()


        brightness_button = tk.Button(tool_top_frame, text="Noice Reduction", font=("Helvetica", 9), bg='#494242', fg='white', relief=tk.FLAT, command=lambda: set_active_button("Noice Reduction"))
        brightness_button.pack(side=tk.LEFT, padx=10, pady=2)


        def change_custom_exposure(value):
            global active_button, resized_image
            nonlocal current_image_label, adjusted_exposure_level

            adjusted_exposure_level = int(value)
            update_displayed_image()

            if resized_image is None:
                messagebox.showerror("Error", "Please select an image first.")
                return



        contrast_button = tk.Button(tool_top_frame, text="Exposure", font=("Helvetica", 9), bg='#494242', fg='white', relief=tk.FLAT, command=lambda: set_active_button("Exposure"))
        contrast_button.pack(side=tk.LEFT, padx=10, pady=2)


      


        
        def update_displayed_image():
            global resized_image
            nonlocal current_image_label, adjusted_sharpness_level, adjusted_noise_level

            # Check if an image is loaded
            if resized_image is None:
                return

            # Create a copy of the resized image
            adjusted_image = resized_image.copy()

            # Apply the sharpness adjustment if non-zero
            if adjusted_sharpness_level != 0:
                enhancer = ImageEnhance.Sharpness(adjusted_image)
                adjusted_image = enhancer.enhance(adjusted_sharpness_level / 100)


            # Apply the non-reduction adjustment if non-zero
            if adjusted_noise_level != 0:
                sigma = adjusted_noise_level / 100
                adjusted_image = adjusted_image.filter(ImageFilter.GaussianBlur(sigma))
            
            if adjusted_exposure_level != 0:
                enhancer = ImageEnhance.Contrast(adjusted_image)
                adjusted_image = enhancer.enhance(1 + adjusted_exposure_level / 100)





            # Update the displayed image
            photo = ImageTk.PhotoImage(adjusted_image)
            current_image_label.configure(image=photo)
            current_image_label.image = photo





        def refresh():
            attribute_window.destroy()
            attributes()

        refresh_button = tk.Button(tool_top_frame, text="Refresh", font=("Helvetica", 9), bg='#494242', fg='white', relief=tk.FLAT, command=refresh)
        refresh_button.pack(side=tk.RIGHT, padx=10, pady=2)

            


        attribute_window.mainloop()

    attribute_button = tk.Button(top_frame, text="Attributes", font=("Helvetica", 9), bg='#494242', fg='white', relief=tk.FLAT, command=attributes)
    attribute_button.pack(side=tk.LEFT, padx=10, pady=2)

    exit_button = tk.Button(top_frame, text="Exit", font=("Helvetica", 9), bg='#494242', fg='white', relief=tk.FLAT, command=second_screen.destroy)
    exit_button.pack(side=tk.LEFT, padx=10, pady=2)

    #Label to display the active tab
    selected_option_label = tk.Label(second_screen, text="", font=("Helvetica", 24), fg="grey", bg='#350505')
    selected_option_label.place(x=214, y=90)
    #selected_option_label.pack(pady=20)

    



    # Create the main content frame using a Canvas widget
    content_frame = tk.Canvas(second_screen, width=655, height=439, bg='#2C0D0D', highlightthickness=0)
    content_frame.place(x=214, y=132.5)

    content_frame.create_window(0, 0, anchor='nw')

    #To delete the widgets on content frame
    def clear_content_frame():
       # Destroy all widgets within the content_frame
        for widget in content_frame.winfo_children():
            widget.destroy()




    def open_styling():
        clear_content_frame()
        # Variable to store the currently displayed image label and its path
        current_image_label = None
        main_image_path = None
        design_image_path = None

        #model = hub.load('C:\\Users\\Umair\\Desktop\\TICS P\\magenta_arbitrary-image-stylization-v1-256_2')
        script_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(script_dir, 'style_model')
        model = hub.load(model_path)
        
        global pil_image1

        pil_image1 = None

        #Label 1 of choosing Main Image
        choose_main_label = tk.Label(content_frame, text="Choose Main Image:", font=("Helvetica", 10), bg='#2C0D0D', fg='white')
        choose_main_label.place(x=10, y=35, width=150, height=17)
        #Label2 of choosing design Image
        choose_design_label = tk.Label(content_frame, text="Choose Design Image:", font=("Helvetica", 10), bg='#2C0D0D', fg='white')
        choose_design_label.place(x=17, y=225, width=150, height=17)

        # Create the "Main Image" frame
        main_image_frame = tk.Frame(content_frame, width=150, height=150, bg='#350505')
        main_image_frame.place(x=109, y=135, anchor=tk.CENTER)
        # Create the "Design Image" frame
        design_image_frame = tk.Frame(content_frame, width=150, height=150, bg='#350505')
        design_image_frame.place(x=109, y=325, anchor=tk.CENTER)

        #Labels for opening  of main image
        choose_main_label = tk.Label(content_frame, text="Select from:", font=("Helvetica", 10), bg='#2C0D0D', fg='white')
        choose_main_label.place(x=200, y=160, width=70, height=14)


        # Variable to store the currently displayed image label
        current_image_label = None

        # Function to handle image selection
        def select_image():
            nonlocal current_image_label, main_image_path
            # Open a file dialog to select an image file
            filetypes = [("Image Files", "*.jpg;*.jpeg")]
            image_path = tk.filedialog.askopenfilename(filetypes=filetypes)

            # Check if an image file was selected
            if image_path:
                # Load the selected image file using PIL
                image = Image.open(image_path)
                # Resize the image to fit the main image frame
                width, height = image.size
                max_size = min(main_image_frame.winfo_width(), main_image_frame.winfo_height())
                if width > height:
                    new_width = max_size
                    new_height = int((new_width / width) * height)
                else:
                    new_height = max_size
                    new_width = int((new_height / height) * width)
                resized_image = image.resize((new_width, new_height))

                # Create a PhotoImage object from the resized image
                photo = ImageTk.PhotoImage(resized_image)

                # Create a label inside the main image frame and assign the PhotoImage to its image attribute
                label = tk.Label(main_image_frame, image=photo)
                label.image = photo  # Store a reference to prevent garbage collection
                label.pack()

                # Remove the previous image label, if it exists
                if current_image_label:
                    current_image_label.pack_forget()

                # Update the current image label
                current_image_label = label
                current_image_label.image_path = image_path

                # Update the main image path
                main_image_path = image_path



        browse_button = tk.Button(content_frame, text="Browse", font=("Helvetica", 10), width=8, height=1, bg='#350505', fg='white', relief=tk.GROOVE, command=select_image)
        browse_button.place(x=200, y=182) 


        #Label for opening design image
        choose_main_label = tk.Label(content_frame, text="Select from:", font=("Helvetica", 10), bg='#2C0D0D', fg='white')
        choose_main_label.place(x=200, y=351, width=70, height=14)

        # Variable to store the currently displayed design image label
        current_design_label = None
        # Function to handle browsing design image selection
        def browse_image():
            nonlocal current_design_label, design_image_path

            # Open a file dialog to select a design image file
            filetypes = [("Image Files", "*.jpg;*.jpeg")]
            design_image_path = filedialog.askopenfilename(filetypes=filetypes)

            # Check if a design image file was selected
            if design_image_path:
                # Load the selected design image file using PIL
                design_image = Image.open(design_image_path)

                # Resize the image to fit the design image frame
                width, height = design_image.size
                max_size = min(design_image_frame.winfo_width(), design_image_frame.winfo_height())
                if width > height:
                    new_width = max_size
                    new_height = int((new_width / width) * height)
                else:
                    new_height = max_size
                    new_width = int((new_height / height) * width)
                resized_image = design_image.resize((new_width, new_height))

                # Create a PhotoImage object from the resized image
                photo = ImageTk.PhotoImage(resized_image)

                # Create a label inside the design image frame and assign the PhotoImage to its image attribute
                label = tk.Label(design_image_frame, image=photo)
                label.image = photo  # Store a reference to prevent garbage collection
                label.pack()

                # Remove the previous design image label, if it exists
                if current_design_label:
                    current_design_label.pack_forget()

                # Update the current design image label
                current_design_label = label
                current_design_label.image_path = design_image_path

        # Create the "Browse" button
        browse_button = tk.Button(content_frame, text="Browse", font=("Helvetica", 10), width=8, height=1, bg='#350505', fg='white', relief=tk.GROOVE, command=browse_image)
        browse_button.place(x=200, y=372)  # Adjust the placement as desire


        #Result frame
        result_frame = tk.Frame(content_frame, width=320, height=320, bg='#350505')
        result_frame.place(x=465, y=200, anchor=tk.CENTER)

        # Function to load an image
        def load_image(img_path):
            img = tensorflow.io.read_file(img_path)
            img = tensorflow.image.decode_image(img, channels=3)
            img = tensorflow.image.convert_image_dtype(img, tensorflow.float32)
            img = img[tensorflow.newaxis, :]
            return img
        
        #random string generator
        def generate_random_string(length):
            """Generate a random string of specified length."""
            letters = string.ascii_letters
            return ''.join(random.choice(letters) for _ in range(length))

        # Function to handle transformation
        def transform_image():

            nonlocal main_image_path, design_image_path
            global pil_image1

            global stylized_image 
            stylized_image = None


            # Check if a main image is selected
            if main_image_path is None or main_image_path == "":
                tk.messagebox.showerror("Error", "Please select a Main image.")
                return
            
            if design_image_path is None or design_image_path == "":
                tk.messagebox.showerror("Error", "Please select a Design image.")
                return

            # Get the path of the selected main image and design image
            main_image_path = current_image_label.image_path
            design_image_path = current_design_label.image_path

            # Load the selected images
            content_image = load_image(main_image_path)
            style_image = load_image(design_image_path)

            # Apply style transfer
            stylized_image = model(tf.constant(content_image), tf.constant(style_image))[0]

            # Convert the stylized image to PIL format

            stylized_image = np.squeeze(stylized_image, axis=0) 
            pil_image = Image.fromarray(np.uint8(stylized_image * 255))
            pil_image1 = pil_image

            # Resize the image to fit the result frame
            width, height = pil_image.size
            max_size = min(result_frame.winfo_width(), result_frame.winfo_height())
            if width > height:
                new_width = max_size
                new_height = int((new_width / width) * height)
            else:
                new_height = max_size
                new_width = int((new_height / height) * width)
            resized_image = pil_image.resize((new_width, new_height))

                # Clear the result_frame
            for widget in result_frame.winfo_children():
                widget.destroy()

            # Create a PhotoImage object from the resized image
            photo = ImageTk.PhotoImage(resized_image)

            # Create a label inside the result frame and assign the PhotoImage to its image attribute
            label = tk.Label(result_frame, image=photo)
            label.image = photo  # Store a reference to prevent garbage collection
            label.pack()


            #auto saving for history
            base_directory = os.path.dirname(os.path.abspath(__file__))
            save_directory = os.path.join(base_directory, "History") 
            timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            random_string = generate_random_string(4)
            save_filename = f"filtered_image_{timestamp}_{random_string}.jpg"

            save_path = os.path.join(save_directory, save_filename)
            pil_image.save(save_path)

        # Create the "Transform" button
        transform_button = tk.Button(content_frame, text="Transform", font=("Helvetica", 10), width=11, height=1, bg='#493737', fg='white', relief=tk.GROOVE, command=transform_image)
        transform_button.place(x=304, y=372)


        def jumpfunc():
            # Save the stylized image to a directory
            save_image_to_gallery(pil_image1)

        # Function to handle saving the image to the gallery directory
        def save_image_to_gallery(image):
            if image is None:
                tk.messagebox.showerror("Error", "Please generate a stylized image first.")
                return
            # Open a file dialog to prompt the user for the image name
            filetypes = [("JPEG Image", "*.jpg")]
            image_path = tk.filedialog.asksaveasfilename(filetypes=filetypes, defaultextension=".jpg")
            
            # Check if the user selected a file name
            if image_path:
                image.save(image_path)
                tk.messagebox.showinfo("Success", "Image saved.")
            else:
                tk.messagebox.showerror("Error", "File Not saved.")
                

        # Create the "Add to Gallery" button
        result_library_button = tk.Button(content_frame, text="Add to Gallery", font=("Helvetica", 10), width=12, height=1, bg='#350505', fg='white', relief=tk.GROOVE, command=jumpfunc)
        result_library_button.place(x=411, y=372) 

        refresh_button = tk.Button(content_frame, text="Refresh", font=("Helvetica", 10), width=11, height=1, bg='#270C0C', fg='white', relief=tk.GROOVE, command=open_styling)
        refresh_button.place(x=526, y=372)



    def open_image_details():
        clear_content_frame()
        global image1
        image1 = None
        global image1_path 
        image1_path = None

        # Variable to store the currently displayed image label and its path
        current_image_label = None
        main_image_path = None
        #Label 1 of choosing Image
        choose_main_label = tk.Label(content_frame, text="Choose Image:", font=("Helvetica", 10), bg='#2C0D0D', fg='white')
        choose_main_label.place(x=10, y=35, width=150, height=17)
        # Create the "Image" frame
        image_frame = tk.Frame(content_frame, width=150, height=150, bg='#350505')
        image_frame.place(x=109, y=135, anchor=tk.CENTER)
        #Labels for opening  of main image
        choose_main_label = tk.Label(content_frame, text="Select from:", font=("Helvetica", 10), bg='#2C0D0D', fg='white')
        choose_main_label.place(x=200, y=160, width=70, height=14)

        #Histogram frame
        hist_frame = tk.Frame(content_frame, width=320, height=200, bg='#350505')
        hist_frame.place(x=465, y=135, anchor=tk.CENTER)

        #Info frame
        info_frame = tk.Frame(content_frame, width=590.5, height=110, bg='#350505')
        info_frame.place(x=329, y=350, anchor=tk.CENTER)

        # Function to handle image selection
        def select_image():
            nonlocal current_image_label, main_image_path
            global image1,image1_path
            # Open a file dialog to select an image file
            filetypes = [("Image Files", "*.jpg;*.jpeg")]
            image_path = tk.filedialog.askopenfilename(filetypes=filetypes)
            image1_path = image_path

            # Check if an image file was selected
            if image_path:
                # Load the selected image file using PIL
                image = Image.open(image_path)
                image1 = image
                # Resize the image to fit the main image frame
                width, height = image.size
                max_size = min(image_frame.winfo_width(), image_frame.winfo_height())
                if width > height:
                    new_width = max_size
                    new_height = int((new_width / width) * height)
                else:
                    new_height = max_size
                    new_width = int((new_height / height) * width)
                resized_image = image.resize((new_width, new_height))

                # Create a PhotoImage object from the resized image
                photo = ImageTk.PhotoImage(resized_image)

                # Create a label inside the main image frame and assign the PhotoImage to its image attribute
                label = tk.Label(image_frame, image=photo)
                label.image = photo  # Store a reference to prevent garbage collection
                label.pack()

                # Remove the previous image label, if it exists
                if current_image_label:
                    current_image_label.pack_forget()

                # Update the current image label
                current_image_label = label
                current_image_label.image_path = image_path

                # Update the main image path
                main_image_path = image_path

        def display_histogram():
            # Calculate and display the histogram
            calculate_and_display_histogram(image1)

        def display_info():
            #Display Image details
            display_image_details(image1)


        def calculate_and_display_histogram(image1):
            #global image1_path
            if image1 is None or image1 == "":
                tk.messagebox.showerror("Error", "Please select an Image.")
                return

            # Convert the image to grayscale
            grayscale_image = image1.convert("L")

            # Check if the image has a valid size
            if grayscale_image.size[0] == 0 or grayscale_image.size[1] == 0:
                return

            # Calculate the histogram
            histogram = grayscale_image.histogram()

            # Normalize the histogram values
            max_count = max(histogram)
            normalized_histogram = [count / max_count for count in histogram]

            # Create a new image with the histogram plot
            plot_image = Image.new("L", (256, 100), color=255)  # White background
            draw = ImageDraw.Draw(plot_image)

            # Plot the histogram
            for i, value in enumerate(normalized_histogram):
                height = int(value * 100)
                draw.line((i, 100, i, 100 - height), fill=0)  # Black line

            # Convert the plot image to RGB
            plot_image_rgb = plot_image.convert("RGB")

            # Create a PhotoImage object from the plot image
            photo = ImageTk.PhotoImage(plot_image_rgb)

            # Clear the hist_frame
            for widget in hist_frame.winfo_children():
                widget.destroy()

            # Create a label inside the hist_frame and assign the PhotoImage to its image attribute
            label = tk.Label(hist_frame, image=photo)
            label.image = photo  # Store a reference to prevent garbage collection
            label.pack()


        browse_button = tk.Button(content_frame, text="Browse", font=("Helvetica", 10), width=8, height=1, bg='#350505', fg='white', relief=tk.GROOVE, command=select_image)
        browse_button.place(x=200, y=182)  # Adjust the placement as desired
        #Button to display general histogram
        display_histogram_button = tk.Button(content_frame, text="Histogram", font=("Helvetica", 10), width=11, height=1, bg='#350505', fg='white', relief=tk.GROOVE, command=display_histogram)
        display_histogram_button.place(x=304, y=240)


        def calculate_white_balance(image):
            # Convert the image to numpy array
            image_array = np.array(image)

            # Calculate the average pixel values for each color channel
            average_channel_values = np.mean(image_array, axis=(0, 1))

            # Normalize the average channel values to sum up to 1
            normalized_values = average_channel_values / np.sum(average_channel_values)

            # Calculate the white balance percentage for each channel
            white_balance_percentages = normalized_values * 100

            # Calculate the overall white balance percentage
            white_balance_percentage = np.mean(white_balance_percentages)

            return white_balance_percentage
        
        def calculate_exposure(image):
            # Convert the image to grayscale
            grayscale_image = image.convert("L")

            # Convert the grayscale image to a numpy array
            image_array = np.array(grayscale_image)

            # Calculate the total number of pixels
            total_pixels = image_array.shape[0] * image_array.shape[1]

            # Calculate the histogram of pixel intensities
            histogram, _ = np.histogram(image_array.flatten(), bins=256, range=[0, 256])

            # Calculate the cumulative distribution function (CDF) of the histogram
            cdf = histogram.cumsum()

            # Normalize the CDF values to range between 0 and 1
            cdf_normalized = cdf / total_pixels

            # Calculate the exposure percentage as the CDF value at intensity 128
            exposure_percentage = cdf_normalized[128] * 100

            return exposure_percentage
        
        def calculate_saturation(image):
            # Convert the image to the HSV color space
            hsv_image = image.convert("HSV")

            # Extract the saturation channel
            saturation_channel = hsv_image.split()[1]

            # Calculate the mean saturation value
            mean_saturation = sum(saturation_channel.getdata()) / (255 * image.width * image.height)

            # Calculate the saturation percentage
            saturation_percentage = mean_saturation * 100

            return saturation_percentage
        
        def calculate_sharpness(image):
            # Convert the image to grayscale
            gray_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)

            # Apply the Sobel operator to compute gradients
            gradient_x = cv2.Sobel(gray_image, cv2.CV_64F, 1, 0, ksize=3)
            gradient_y = cv2.Sobel(gray_image, cv2.CV_64F, 0, 1, ksize=3)

            # Calculate the magnitude of the gradients
            gradient_magnitude = np.sqrt(gradient_x**2 + gradient_y**2)

            # Calculate the sharpness as the mean gradient magnitude
            sharpness = np.mean(gradient_magnitude)

            # Normalize the sharpness value to a percentage
            sharpness_percentage = sharpness / 255 * 100

            return sharpness_percentage
        
        def calculate_contrast(image):
            # Convert the image to grayscale
            grayscale_image = image.convert("L")

            # Convert the grayscale image to a NumPy array
            image_array = np.array(grayscale_image)

            # Calculate the standard deviation of pixel intensities
            contrast = np.std(image_array)

            # Normalize the contrast value to a percentage
            contrast_percentage = contrast / 255 * 100

            return contrast_percentage
        
        def calculate_dynamic_range(image):
            # Convert the image to grayscale
            grayscale_image = image.convert("L")

            # Convert the grayscale image to a NumPy array
            image_array = np.array(grayscale_image)

            # Calculate the minimum and maximum pixel intensities
            min_intensity = np.min(image_array)
            max_intensity = np.max(image_array)

            # Calculate the dynamic range
            dynamic_range = max_intensity - min_intensity

            # Normalize the dynamic range value to a percentage
            dynamic_range_percentage = (dynamic_range / 255) * 100

            return dynamic_range_percentage

        def calculate_noise(image):
            # Convert the image to grayscale
            grayscale_image = image.convert("L")

            # Convert the grayscale image to a NumPy array
            image_array = np.array(grayscale_image)

            # Apply median filtering to obtain a denoised version of the image
            denoised_image_array = median_filter(image_array, size=3)

            # Calculate the mean squared error between the original and denoised images
            mse = mean_squared_error(image_array, denoised_image_array)

            # Normalize the MSE value to a percentage
            noise_percentage = (mse / (255**2)) * 100

            return noise_percentage



        def display_image_details(image):

            if image1 is None or image1 == "":
                tk.messagebox.showerror("Error", "Please select an Image.")
                return
            
            white_balance = calculate_white_balance(image)
            exposure = calculate_exposure(image)
            saturation = calculate_saturation(image)
            sharpness = calculate_sharpness(image)
            contrast = calculate_contrast(image)
            dynamic_range = calculate_dynamic_range(image)
            noise = calculate_noise(image)

            # Clear the info_frame
            for widget in info_frame.winfo_children():
                widget.destroy()

            # Create and place the labels in the info_frame
            white_balance_label = tk.Label(info_frame, text=f"White Balance: {white_balance}%", font=("Helvetica", 8))
            exposure_label = tk.Label(info_frame, text=f"Exposure: {exposure}%", font=("Helvetica", 8))
            saturation_label = tk.Label(info_frame, text=f"Saturation: {saturation}%", font=("Helvetica", 8))
            sharpness_label = tk.Label(info_frame, text=f"Sharpness: {sharpness}%", font=("Helvetica", 8))
            contrast_label = tk.Label(info_frame, text=f"Contrast: {contrast}%", font=("Helvetica", 8))
            dynamic_range_label = tk.Label(info_frame, text=f"Dynamic Range: {dynamic_range}%", font=("Helvetica", 8))
            noise_label = tk.Label(info_frame, text=f"Noise: {noise}%", font=("Helvetica", 8))

            white_balance_label.place(x=10, y=15)
            exposure_label.place(x=10, y=45)
            saturation_label.place(x=10, y=75)
            sharpness_label.place(x=215, y=15)
            contrast_label.place(x=215, y=45)
            dynamic_range_label.place(x=215, y=75)
            noise_label.place(x=419, y=15)

        #Info Button
        info_button = tk.Button(content_frame, text="Info", font=("Helvetica", 10), width=12, height=1, bg='#350505', fg='white', relief=tk.GROOVE, command=display_info)
        info_button.place(x=411, y=240)
        #Refresh Button
        refresh_button = tk.Button(content_frame, text="Refresh", font=("Helvetica", 10), width=11, height=1, bg='#270C0C', fg='white', relief=tk.GROOVE, command=open_image_details)
        refresh_button.place(x=526, y=240)


    def open_library():
        clear_content_frame()

        # Create a canvas within the content frame to enable scrolling
        canvas = tk.Canvas(content_frame, width=655, height=439, bg='#2C0D0D', highlightthickness=0)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create a frame inside the canvas to hold the images
        gallery_frame = tk.Frame(canvas, bg='#2C0D0D')
        gallery_frame.pack(side=tk.TOP, padx=10, pady=10)

        # Configure the canvas to scroll the frame
        canvas.create_window((0, 0), window=gallery_frame, anchor='nw')
        canvas.configure(yscrollcommand=lambda e, s: canvas.configure(scrollregion=canvas.bbox("all")))
        scrollbar = tk.Scrollbar(content_frame, orient="vertical", command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.configure(yscrollcommand=scrollbar.set)

        # Determine the path where the images are located
        base_directory = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(base_directory, "Gallery")

        # Retrieve the list of image files from the specified path
        image_files = glob.glob(image_path + "/*.jpg") + glob.glob(image_path + "/*.jpeg")


        # Iterate over the image files and create labels for each image
        row = 0
        col = 0
        for i, image_file in enumerate(image_files):
            # Load the image file using PIL
            image = Image.open(image_file)

            # Calculate the resized width and height while maintaining the aspect ratio
            max_size = 150  # Maximum size for the images
            width, height = image.size
            aspect_ratio = width / height
            new_width = max_size
            new_height = int(new_width / aspect_ratio)

            # Resize the image while maintaining the aspect ratio
            resized_image = image.resize((new_width, new_height))

            # Create a PhotoImage object from the resized image
            photo = ImageTk.PhotoImage(resized_image)

            # Create a label and assign the PhotoImage to its image attribute
            label = tk.Label(gallery_frame, image=photo)
            label.image = photo  # Store a reference to prevent garbage collection
            label.grid(row=row, column=col, padx=10, pady=10)

            # Update the column and row for the next image
            col += 1
            if col == 3:  # Adjust the number of columns as needed
                col = 0
                row += 1

        # Update the scroll region of the canvas to include all the images
        canvas.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))


    def open_filters():
        clear_content_frame()

        global image1
        image1 = None
        global image1_path 
        image1_path = None
        global filtered_image
        filtered_image = None
        main_image_path = None

        # Variable to store the currently displayed image label and its path
        current_image_label = None
        main_image_path = None

        #Label 1 of choosing Image
        choose_main_label = tk.Label(content_frame, text="Choose Image:", font=("Helvetica", 10), bg='#2C0D0D', fg='white')
        choose_main_label.place(x=10, y=35, width=150, height=17)
        # Create the "Image" frame
        image_frame = tk.Frame(content_frame, width=150, height=150, bg='#350505')
        image_frame.place(x=109, y=135, anchor=tk.CENTER)
        #Labels for opening  of main image
        choose_main_label = tk.Label(content_frame, text="Select from:", font=("Helvetica", 10), bg='#2C0D0D', fg='white')
        choose_main_label.place(x=200, y=160, width=70, height=14)
        #Result frame
        result_frame = tk.Frame(content_frame, width=320, height=320, bg='#350505')
        result_frame.place(x=465, y=200, anchor=tk.CENTER)


        # Function to handle image selection
        def select_image():
            nonlocal current_image_label, main_image_path
            global image1,image1_path
            # Open a file dialog to select an image file
            filetypes = [("Image Files", "*.jpg;*.jpeg")]
            image_path = tk.filedialog.askopenfilename(filetypes=filetypes)
            image1_path = image_path

            # Check if an image file was selected
            if image_path:
                # Load the selected image file using PIL
                image = Image.open(image_path)
                image1 = image
                # Resize the image to fit the main image frame
                width, height = image.size
                max_size = min(image_frame.winfo_width(), image_frame.winfo_height())
                if width > height:
                    new_width = max_size
                    new_height = int((new_width / width) * height)
                else:
                    new_height = max_size
                    new_width = int((new_height / height) * width)
                resized_image = image.resize((new_width, new_height))

                # Create a PhotoImage object from the resized image
                photo = ImageTk.PhotoImage(resized_image)

                # Create a label inside the main image frame and assign the PhotoImage to its image attribute
                label = tk.Label(image_frame, image=photo)
                label.image = photo  # Store a reference to prevent garbage collection
                label.pack()

                # Remove the previous image label, if it exists
                if current_image_label:
                    current_image_label.pack_forget()

                # Update the current image label
                current_image_label = label
                current_image_label.image_path = image_path

                # Update the main image path
                main_image_path = image_path

        browse_button = tk.Button(content_frame, text="Browse", font=("Helvetica", 10), width=8, height=1, bg='#350505', fg='white', relief=tk.GROOVE, command=select_image)
        browse_button.place(x=200, y=182)


        choose_filter_label = tk.Label(content_frame, text="Choose Filter:", font=("Helvetica", 10), bg='#2C0D0D', fg='white')
        choose_filter_label.place(x=10, y=250, width=150, height=14)


        #Drop down menu selection
        def on_select(event):
            selected_filter = filter_var.get()
            filter_label.config(text=selected_filter)

        filters = ["Sharpening Filter", "Hard Sharpening", "Smoothing Filter", "Noise Reduction", "Saturation", "Negative Filter","De-Saturize", "Contrast Enhancement", "Increase Exposure", "Decrease Exposure", "Color Balance", "Emboss Filter", "Water Color Filter", "Solarize Filter", "Posterize Filter", "Sepia Filter"]

        filter_var = tk.StringVar()
        filter_var.set(filters[0])

        filter_label = tk.Label(content_frame, text="Select Filter:", height=1, bg ='#350505', fg='white', relief=tk.GROOVE)
        filter_label.place(x=35, y=272, width= 143)

        style = ttk.Style()
        style.configure("Custom.TCombobox", background="#350505", foreground="grey")

        filter_dropdown = ttk.Combobox(content_frame, textvariable=filter_var, values=filters, width=20, state= 'readonly', style="Custom.TCombobox")
        filter_dropdown.bind("<<ComboboxSelected>>", on_select)
        filter_dropdown.place(x=35, y=295)

        #Code for the filters starts here
        def apply_sharpening_filter(image):
            # Apply sharpening filter to the image
            # Replace this with your actual implementation
            sharpened_image = image.filter(ImageFilter.SHARPEN)
            return sharpened_image
        
        def apply_hard_sharp_filter(image):
            r, g, b = image.split()

            # Apply unsharp mask to each RGB channel
            r_sharpened = r.filter(ImageFilter.UnsharpMask(radius=2, percent=150, threshold=3))
            g_sharpened = g.filter(ImageFilter.UnsharpMask(radius=2, percent=150, threshold=3))
            b_sharpened = b.filter(ImageFilter.UnsharpMask(radius=2, percent=150, threshold=3))

            # Merge the sharpened RGB channels back into an image
            sharpened_image = Image.merge("RGB", (r_sharpened, g_sharpened, b_sharpened))

            return sharpened_image    
        
        def apply_smoothing_filter(image):
            # Apply smoothing filter to the image
            # Replace this with your actual implementation
            smoothed_image = image.filter(ImageFilter.SMOOTH)
            return smoothed_image
        
        def apply_noise_reduction(image):
            # Convert the image to a numpy array
            image_array = np.array(image)

            # Apply the noise reduction filter
            filtered_image = gaussian_filter(image_array, sigma=1.0)

            # Convert the filtered image back to PIL Image format
            filtered_image = Image.fromarray(filtered_image)

            return filtered_image
        
        def apply_de_saturize_filter(image, saturation = 0.5):
            enhancer = ImageEnhance.Color(image)
            adjusted_image = enhancer.enhance(saturation)
            return adjusted_image
        
        def apply_saturation(image, saturation = 1.5):
            """
            Adjust the saturation of an image.

            Args:
                image (PIL.Image.Image): The input image.
                saturation (float): The saturation factor. Use a value of 1.0 for no change,
                                    less than 1.0 for desaturation, and greater than 1.0 for saturation.

            Returns:
                PIL.Image.Image: The adjusted image.
            """
            enhancer = ImageEnhance.Color(image)
            adjusted_image = enhancer.enhance(saturation)
            return adjusted_image        
        
        def apply_negative_filter(image):
            # Convert the image to RGB mode if it's not already
            image = image.convert("RGB")

            # Get the pixel data of the image
            pixels = image.load()

            # Iterate over each pixel and apply the negative transformation
            width, height = image.size
            for y in range(height):
                for x in range(width):
                    r, g, b = pixels[x, y]
                    pixels[x, y] = (255 - r, 255 - g, 255 - b)

            # Return the modified image
            return image
        
        def apply_contrast_enhancement(image, factor=1.5):
            """
            Apply contrast enhancement to the image.

            Args:
                image (PIL.Image.Image): The input image.
                factor (float): The contrast enhancement factor. Default is 1.5.

            Returns:
                PIL.Image.Image: The contrast-enhanced image.
            """
            # Create an enhancer object for contrast
            enhancer = ImageEnhance.Contrast(image)

            # Apply contrast enhancement
            enhanced_image = enhancer.enhance(factor)

            return enhanced_image

        def apply_increase_exposure_filter(image, factor=1.5):
            """
            Adjust the exposure of the image.

            Args:
                image (PIL.Image.Image): The input image.
                factor (float): The exposure adjustment factor. Default is 1.5.

            Returns:
                PIL.Image.Image: The image with adjusted exposure.
            """
            # Create an enhancer object for exposure
            enhancer = ImageEnhance.Brightness(image)

            # Adjust the exposure
            adjusted_image = enhancer.enhance(factor)

            return adjusted_image
        
        def apply_decrease_exposure_filter(image, factor=0.5):
            """
            Adjust the exposure of the image.

            Args:
                image (PIL.Image.Image): The input image.
                factor (float): The exposure adjustment factor. Default is 1.5.

            Returns:
                PIL.Image.Image: The image with adjusted exposure.
            """
            # Create an enhancer object for exposure
            enhancer = ImageEnhance.Brightness(image)

            # Adjust the exposure
            adjusted_image = enhancer.enhance(factor)

            return adjusted_image

        def adjust_color_balance(image, red_factor=1.0, green_factor=1.0, blue_factor=1.0):
            """
            Adjust the color balance of the image.

            Args:
                image (PIL.Image.Image): The input image.
                red_factor (float): The red channel adjustment factor. Default is 1.0.
                green_factor (float): The green channel adjustment factor. Default is 1.0.
                blue_factor (float): The blue channel adjustment factor. Default is 1.0.

            Returns:
                PIL.Image.Image: The image with adjusted color balance.
            """
            # Convert image to RGB mode if it's not already
            if image.mode != "RGB":
                image = image.convert("RGB")

            # Split the image into color channels
            red, green, blue = image.split()

            # Apply color balance adjustments
            adjusted_red = red.point(lambda x: int(x * red_factor))
            adjusted_green = green.point(lambda x: int(x * green_factor))
            adjusted_blue = blue.point(lambda x: int(x * blue_factor))

            # Merge the adjusted color channels
            adjusted_image = Image.merge("RGB", (adjusted_red, adjusted_green, adjusted_blue))

            return adjusted_image

        def apply_emboss_filter(image):
            """
            Apply the emboss filter to the image.

            Args:
                image (PIL.Image.Image): The input image.

            Returns:
                PIL.Image.Image: The image with the emboss filter applied.
            """
            # Apply the emboss filter to the image
            embossed_image = image.filter(ImageFilter.EMBOSS)

            return embossed_image

        def apply_watercolor_filter(image):
            # Apply watercolor effect using ImageFilter
            watercolor_image = image.filter(ImageFilter.GaussianBlur(radius=2))
            watercolor_image = watercolor_image.filter(ImageFilter.MedianFilter(size=9))
            watercolor_image = ImageEnhance.Color(watercolor_image).enhance(0.5)
            watercolor_image = ImageEnhance.Brightness(watercolor_image).enhance(1.2)
            watercolor_image = ImageEnhance.Contrast(watercolor_image).enhance(1.1)

            return watercolor_image

        def apply_solarize_filter(image, threshold=128):
            # Apply solarize filter using ImageOps
            solarized_image = ImageOps.solarize(image, threshold)

            return solarized_image

        def apply_posterize_filter(image, bits=4):
            # Apply posterize filter using ImageOps
            posterized_image = ImageOps.posterize(image, bits)

            return posterized_image

        def apply_sepia_filter(image):
            # Apply sepia filter using ImageOps
            sepia_image = ImageOps.colorize(image.convert("L"), "#704214", "#C0C080")

            return sepia_image
        

        #function to generate random string for naming
        def generate_random_string(length):
            """Generate a random string of specified length."""
            letters = string.ascii_letters
            return ''.join(random.choice(letters) for _ in range(length))

        

        def apply_filter():
            global filtered_image
            if image1 is None or image1 == "":
                tk.messagebox.showerror("Error", "Please select an Image.")
                return
            
            selected_filter = filter_var.get()
            

            # if selected_filter is False:
            #     tk.messagebox.showerror("Error", "Please select a filter.")
            #     return


            if selected_filter == "Sharpening Filter":
                filtered_image = apply_sharpening_filter(image1)
            elif selected_filter == "Smoothing Filter":
                filtered_image = apply_smoothing_filter(image1)
            elif selected_filter == "Noise Reduction":
                filtered_image = apply_noise_reduction(image1)
            elif selected_filter == "Saturation":
                filtered_image = apply_saturation(image1)
            elif selected_filter == "Negative Filter":
                filtered_image = apply_negative_filter(image1)
            elif selected_filter == "De-Saturize":
                filtered_image = apply_de_saturize_filter(image1)
            elif selected_filter == "Hard Sharpening":
                filtered_image = apply_hard_sharp_filter(image1)
            elif selected_filter == "Contrast Enhancement":
                filtered_image = apply_contrast_enhancement(image1)
            elif selected_filter == "Increase Exposure":
                filtered_image = apply_increase_exposure_filter(image1)
            elif selected_filter == "Decrease Exposure":
                filtered_image = apply_decrease_exposure_filter(image1)
            elif selected_filter == "Color Balance":
                filtered_image = adjust_color_balance(image1)
            elif selected_filter == "Emboss Filter":
                filtered_image = apply_emboss_filter(image1)
            elif selected_filter == "Water Color Filter":
                filtered_image = apply_watercolor_filter(image1)
            elif selected_filter == "Solarize Filter":
                filtered_image = apply_solarize_filter(image1)
            elif selected_filter == "Posterize Filter":
                filtered_image = apply_posterize_filter(image1)
            elif selected_filter == "Sepia Filter":
                filtered_image = apply_sepia_filter(image1)
            # elif selected_filter == "Restore":
            #     #error
            #     filtered_image = restore_filter(image1)
            else:
                tk.messagebox.showerror("Error", "No filter selected.")
                return

            # Create a PhotoImage object from the filtered image
            filtered_photo = ImageTk.PhotoImage(filtered_image)

            # Resize the image to fit the result_frame
            width, height = filtered_image.size
            max_size = min(result_frame.winfo_width(), result_frame.winfo_height())
            if width > height:
                new_width = max_size
                new_height = int((new_width / width) * height)
            else:
                new_height = max_size
                new_width = int((new_height / height) * width)
            resized_image = filtered_image.resize((new_width, new_height))

            # Create a PhotoImage object from the resized image
            filtered_photo = ImageTk.PhotoImage(resized_image)

            # Create a label inside the result frame and assign the PhotoImage to its image attribute
            result_label = tk.Label(result_frame, image=filtered_photo)
            result_label.image = filtered_photo

            # Remove any previous result labels
            for child in result_frame.winfo_children():
                child.pack_forget()

            # Display the filtered image
            result_label.pack()

            


            #auto saving for history
            base_directory = os.path.dirname(os.path.abspath(__file__))
            save_directory = os.path.join(base_directory, "History")  # Replace with your desired save directory
            timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            random_string = generate_random_string(4)
            save_filename = f"filtered_image_{timestamp}_{random_string}.jpg"

            save_path = os.path.join(save_directory, save_filename)
            filtered_image.save(save_path)
            
            # Show a success message
            #tk.messagebox.showinfo("Success", f"The filtered image has been saved to:\n{save_path}")


        # Create the "Apply Filter" button
        apply_filter_button = tk.Button(content_frame, text="Apply Fliter", font=("Helvetica", 10), width=12, height=1, bg='#350505', fg='white', relief=tk.GROOVE, command=apply_filter)
        apply_filter_button.place(x=304, y=372)

        def jumpfunc():
            # Save the stylized image to a directory
            save_image_to_gallery(filtered_image)

        # Function to handle saving the image to the gallery directory
        def save_image_to_gallery(image):
            #global fil_image1
            if image is None:
                tk.messagebox.showerror("Error", "Please Apply filter first.")
                return
            # Open a file dialog to prompt the user for the image name
            filetypes = [("JPEG Image", "*.jpg")]
            image_path = tk.filedialog.asksaveasfilename(filetypes=filetypes, defaultextension=".jpg")
            
            # Check if the user selected a file name
            if image_path:
                image.save(image_path)
                tk.messagebox.showinfo("Success", "Image saved.")
                

        # Create the "Add to Gallery" button
        result_library_button = tk.Button(content_frame, text="Add to Gallery", font=("Helvetica", 10), width=12, height=1, bg='#350505', fg='white', relief=tk.GROOVE, command=jumpfunc)
        result_library_button.place(x=415, y=372)
        # Create the "Refresh" button
        refresh_button = tk.Button(content_frame, text="Refresh", font=("Helvetica", 10), width=11, height=1, bg='#270C0C', fg='white', relief=tk.GROOVE, command=open_filters)
        refresh_button.place(x=526, y=372)



    def open_history():
        clear_content_frame()

        # Create a canvas within the content frame to enable scrolling
        canvas = tk.Canvas(content_frame, width=655, height=439, bg='#2C0D0D', highlightthickness=0)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create a frame inside the canvas to hold the images
        gallery_frame = tk.Frame(canvas, bg='#2C0D0D')
        gallery_frame.pack(side=tk.TOP, padx=10, pady=10)

        # Configure the canvas to scroll the frame
        canvas.create_window((0, 0), window=gallery_frame, anchor='nw')
        canvas.configure(yscrollcommand=lambda e, s: canvas.configure(scrollregion=canvas.bbox("all")))
        scrollbar = tk.Scrollbar(content_frame, orient="vertical", command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.configure(yscrollcommand=scrollbar.set)

        # Determine the path where the images are located
        base_directory = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(base_directory, "History")

        # Retrieve the list of image files from the specified path
        #image_files = glob.glob(image_path + "/*.jpg")
        image_files = glob.glob(image_path + "/*.jpg") + glob.glob(image_path + "/*.jpeg")

        if len(image_files) == 0:
            # If there are no image files, display a message in the content_frame
            no_files_label = tk.Label(content_frame, text="No files are in History.", font=("Helvetica", 15), bg='#270C0C', fg='grey')
            no_files_label.place(x = 310, y= 200, anchor=tk.CENTER)
        else:
            # Iterate over the image files and create labels for each image
            row = 0
            col = 0

            for i, image_file in enumerate(image_files):
                # Load the image file using PIL
                image = Image.open(image_file)

                # Calculate the resized width and height while maintaining the aspect ratio
                max_size = 150  # Maximum size for the images
                width, height = image.size
                aspect_ratio = width / height
                new_width = max_size
                new_height = int(new_width / aspect_ratio)

                # Resize the image while maintaining the aspect ratio
                resized_image = image.resize((new_width, new_height))

                # Create a PhotoImage object from the resized image
                photo = ImageTk.PhotoImage(resized_image)

                # Create a label and assign the PhotoImage to its image attribute
                label = tk.Label(gallery_frame, image=photo)
                label.image = photo  # Store a reference to prevent garbage collection
                label.grid(row=row, column=col, padx=10, pady=10)

                # Update the column and row for the next image
                col += 1
                if col == 3:  # Adjust the number of columns as needed
                    col = 0
                    row += 1

            # Update the scroll region of the canvas to include all the images
            canvas.update_idletasks()
            canvas.configure(scrollregion=canvas.bbox("all"))
            


        #function to delete history
        def delete_files(directory):
            
            try:
                # Iterate over files in the directory
                for filename in os.listdir(directory):
                    file_path = os.path.join(directory, filename)
                    # Check if the path is a file and delete it
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                
                messagebox.showinfo("Success", "Files deleted successfully!")
                open_history()
                
            except Exception as e:
                messagebox.showerror("Error", str(e))


        def confirm_delete_files():
            base_directory = os.path.dirname(os.path.abspath(__file__))
            directory = os.path.join(base_directory, "History")
            confirmation = messagebox.askquestion("Confirmation", f"Are you sure you want to delete the files in '{directory}'?")
        
            if confirmation == "yes":
                delete_files(directory)
            else:
                messagebox.showinfo("Canceled", "Deletion canceled.")

        clear_history_button = tk.Button(content_frame, text="Clear History", font=("Helvetica", 10), width=11, height=1, bg='#270C0C', fg='white', relief=tk.GROOVE, command=confirm_delete_files)
        clear_history_button.place(x=540, y=400)  # Adjust the placement as desired




    def open_manual():
        clear_content_frame()

        # Create a canvas within the content frame to enable scrolling
        canvas = tk.Canvas(content_frame, width=655, height=439, bg="#2C0D0D", highlightthickness=0)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create a frame inside the canvas to hold the manual text
        gallery_frame = tk.Frame(canvas, bg="#2C0D0D")
        gallery_frame.pack(side=tk.TOP, padx=10, pady=10)

        # Configure the canvas to scroll the frame
        canvas.create_window((0, 0), window=gallery_frame, anchor="nw")
        canvas.configure(yscrollcommand=lambda e, s: canvas.configure(scrollregion=canvas.bbox("all")))
        scrollbar = tk.Scrollbar(content_frame, orient="vertical", command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.configure(yscrollcommand=scrollbar.set)

        # Open and read the manual file
        base_directory = os.path.dirname(os.path.abspath(__file__))
        manual_path = os.path.join(base_directory, "readme.txt")
        with open(manual_path, "r") as file:
            manual_contents = file.read()

        # Create a Text widget to display the manual
        manual_text = tk.Text(gallery_frame, height=27, width=81, bg="#2C0D0D", fg="white")
        manual_text.insert(tk.END, manual_contents)
        manual_text.config(state=tk.DISABLED)
        manual_text.pack()

        # Update the scroll region of the canvas to include the manual text
        canvas.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))
    
    def create_side_frame():
        # Create the side frame
        side_frame = tk.Frame(second_screen, width=200, bg='#300808')
        side_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Load the icon image for the side frame
        base_directory = os.path.dirname(os.path.abspath(__file__))
        side_icon_path = os.path.join(base_directory, "icon1.png")  # Specify the path to your side frame icon image

        try:
            # Load the icon image for the side frame
            side_icon_image = Image.open(side_icon_path)
            side_icon_image = side_icon_image.resize((80, 80))  # Resize the image if needed
            side_icon_photo = ImageTk.PhotoImage(side_icon_image)

            # Create a label to display the side frame icon
            side_icon_label = Label(side_frame, image=side_icon_photo, bg='#300808')
            side_icon_label.image = side_icon_photo  # Store a reference to the image to prevent it from being garbage collected
            side_icon_label.pack(pady=10)
        except Exception as e:
            print(f"Error loading side frame icon: {e}")

        # Create the options with separators
        options = ["Styling", "Details", "Gallery", "Filters", "History", "Manual"]

        for i, option in enumerate(options):
            # Create the option button
            option_button = tk.Button(side_frame, text=option, font=("Helvetica", 12), bg='#2C0D0D', fg='white', bd=0, relief=tk.FLAT, padx=10, pady=10, command=lambda o=option: handle_option(o))
            option_button.pack(fill=tk.X)

            # Add a separator after each option, except for the last one
            if i < len(options) - 1:
                separator = tk.Frame(side_frame, height=1, width=180, bg='grey')
                separator.pack(fill=tk.X)

        # Update the side frame's height to fill the entire window vertically
        second_screen.update()
        side_frame.configure(height=second_screen.winfo_height())



    def handle_option(option):
        if option == "Styling":
            open_styling()
        elif option == "Details":
            open_image_details()
        elif option == "Gallery":
            open_library()
        elif option == "Filters":
            open_filters()
        elif option == "History":
            open_history()
        elif option == "Manual":
            open_manual()
        
        selected_option_label.config(text=option)

    # Create the side frame
    create_side_frame()

    # Run the second screen window
    second_screen.mainloop()

create_screen()
