from tkinter import *
from PIL import Image, ImageTk
from tkinter import filedialog
import cv2
import tkinter as tk
import random

root = Tk()
root.geometry("500x200")


# Initialing Function
def select_image():
    # grab a reference to the Image Panels
    global panelA, panelB
    # open a file chooser to select a image
    path = filedialog.askopenfilename()
    # to ensure the path was selected
    if len(path) > 0:
        # Original Label
        Label(root, text='Your Original Image', bg='black', fg='white', font=('calibre', 10, 'bold')).place(relx=0.04,
                                                                                                            rely=0.2)
        # Cartoon Label
        Label(root, text='Cartoon Image', bg='black', fg='white', font=('calibre', 10, 'bold')).place(relx=0.7,
                                                                                                      rely=0.2)

        isSelected = True
        # load the img to desk
        image = cv2.imread(path)
        w = 500
        h = 500
        image = cv2.resize(image, (w, h), interpolation=cv2.INTER_NEAREST)
        b, g, r = cv2.split(image)
        img = cv2.merge((r, g, b))

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.medianBlur(gray, 5)
        edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 7, 7)

        # make cartoon
        color = cv2.bilateralFilter(img, 9, 30, 30)
        cartoon = cv2.bitwise_and(color, color, mask=edges)
        cartoon = cv2.resize(cartoon, (w, h), interpolation=cv2.INTER_NEAREST)

        # CONVERT THE IMAGE TO PIL format

        image = Image.fromarray(img)
        cartoon = Image.fromarray(cartoon)
        r = random.random()
        c = cartoon.save("img_{r}.jpg")

        # and then to Imagetk Format
        image = ImageTk.PhotoImage(image)
        cartoon = ImageTk.PhotoImage(cartoon)

        # root.attributes('-fullscreen', True)
        # make it full screen
        w, h = root.winfo_screenwidth(), root.winfo_screenheight()
        root.geometry("%dx%d+0+0" % (w, h))

        # if the panels are None, initialize them
        if panelA is None or panelB is None:
            # the first panel will store our original image
            panelA = Label(image=image)
            panelA.image = image
            panelA.pack(side="left", padx=10, pady=10)

            # while the second panel will store the edge map
            panelB = Label(image=cartoon)
            panelB.image = cartoon
            panelB.pack(side="right", padx=10, pady=10)

        # otherwise, update the image panels
        else:
            # update the pannels
            panelA.configure(image=image)
            panelB.configure(image=cartoon)
            panelA.image = image
            panelB.image = cartoon


# initialize the window toolkit along with the two image panels
panelA = None
panelB = None

# Button
btn = Button(root, text="Select New image", bg='black', fg='white', font=('calibre', 10, 'bold'), command=select_image)
btn.pack(side="top", padx="10", pady="10")

# Heading
Label(root, text="Make your Image as Cartoon Image", bg="black", fg="white", font=('calibre', 20, 'bold')).place(
    relx=0.08, rely=0.8)

# run main loop
root.mainloop()
