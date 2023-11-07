import matplotlib
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import cv2 as cv
from tkinter import filedialog
import numpy as np
from skimage.filters import threshold_niblack

def bernsen_threshold(image):
    return cv.adaptiveThreshold(image, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 15, 15)

def niblack_threshold(image):
    thresh_niblack = threshold_niblack(image, window_size=15, k= -0.2)
    binary_niblack = image > thresh_niblack
    return binary_niblack

def low_pass_filter(image):
   return cv.GaussianBlur(image, (11, 11), 0)

def update(image):
    thresh_bernsen = bernsen_threshold(image)
    thresh_niblack = niblack_threshold(image)
    low_pass_gauss = low_pass_filter(image)
    plt.subplot(2, 2, 1).imshow(image, cmap=plt.cm.gray)
    plt.subplot(2, 2, 2).imshow(low_pass_gauss, cmap=plt.cm.gray)
    plt.subplot(2, 2, 3).imshow(thresh_niblack, cmap=plt.cm.gray)
    plt.subplot(2, 2, 4).imshow(thresh_bernsen, cmap=plt.cm.gray)
    plt.draw()
    
def open(self):
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png *.jpeg *.gif *.bmp")])
    if file_path:
        photo = cv.imread(file_path)
        photo = cv.cvtColor(photo, cv.COLOR_BGR2GRAY) 
        photo = photo.astype(np.uint8)
        global image
        update(photo)
    
matplotlib.rcParams['font.size'] = 9

plt.figure(figsize=(8, 7))
plt.subplot(2, 2, 1)
plt.title('Original(gray)')
plt.axis('off')

plt.subplot(2, 2, 2)
plt.title('Low pass filter')
plt.axis('off')

plt.subplot(2, 2, 3)
plt.title('Niblack Threshold')
plt.axis('off')

plt.subplot(2, 2, 4)
plt.title('Bernsen Threshold')
plt.axis('off')
axes = plt.axes([0.45, 0.000001, 0.1, 0.075])
bnext = Button(axes, 'open')
bnext.on_clicked(open)
plt.show()