import numpy as np
import cv2
from matplotlib import pyplot as plt


# Load the image
img = cv2.imread('./images/gun.jpg')
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# Prepocess
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blur = cv2.blur(gray, (3, 3), 1)
flag, thresh = cv2.threshold(blur, 69, 255, cv2.THRESH_BINARY_INV)

# Find contours
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contours = sorted(contours, key=cv2.contourArea, reverse=True)
mask = np.zeros(img.shape, np.uint8)
cv2.drawContours(mask, contours[0:3], -1, (0, 0, 255), thickness=cv2.FILLED)

# Select long perimeters only
perimeters = [cv2.arcLength(contours[i], True) for i in range(len(contours))]
listindex = [i for i in range(15) if perimeters[i] > perimeters[0] / 2]
numcards = len(listindex)

# Show images side by side using Matplotlib
fig = plt.figure(figsize=(15, 5))

# Original image
ax1 = fig.add_subplot(151)
ax1.imshow(img)
ax1.set_title('Original Image')
ax1.axis('off')

# Grayscale image
ax2 = fig.add_subplot(152)
ax2.imshow(gray, cmap='gray')
ax2.set_title('Grayscale')
ax2.axis('off')

# Blurred image
ax3 = fig.add_subplot(153)
ax3.imshow(blur, cmap='gray')
ax3.set_title('Blurred')
ax3.axis('off')

# Thresholded image
ax4 = fig.add_subplot(154)
ax4.imshow(thresh, cmap='gray')
ax4.set_title('Thresholded')
ax4.axis('off')

# Contours masked on the original image
ax5 = fig.add_subplot(155)
imgcont = img.copy()
[cv2.drawContours(imgcont, [contours[i]], -1, (0, 255, 0), -1) for i in listindex]
filled = cv2.addWeighted(img, 0.5, imgcont, 1 - 0.5, 0)
ax5.imshow(filled)
ax5.set_title('Segmented Image')
ax5.axis('off')

plt.tight_layout()
plt.show()
