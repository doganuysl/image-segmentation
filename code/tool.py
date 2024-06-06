import cv2
import numpy as np

def callback(x):
    pass

img = cv2.imread('./images/gun.jpg', 0)  # read image as grayscale
img = cv2.GaussianBlur(img, (5, 5), 1)

canny = cv2.Canny(img, 85, 255)

cv2.namedWindow('image')  # make a window with name 'image'
cv2.createTrackbar('L', 'image', 0, 255, callback)  # lower threshold trackbar for window 'image
cv2.createTrackbar('U', 'image', 0, 255, callback)  # upper threshold trackbar for window 'image

while True:
    # Resize the image for display
    resized_img = cv2.resize(img, (500, 500))  # Resize to 500x500
    resized_canny = cv2.resize(canny, (500, 500))  # Resize to match img

    numpy_horizontal_concat = np.concatenate((resized_img, resized_canny), axis=1)  # to display image side by side
    cv2.imshow('image', numpy_horizontal_concat)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:  # escape key
        break
    l = cv2.getTrackbarPos('L', 'image')
    u = cv2.getTrackbarPos('U', 'image')
    canny = cv2.Canny(img, l, u)

    contours, hierarchy = cv2.findContours(canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    result = canny.copy()
    if hierarchy is not None:
        hierarchy = hierarchy[0]
        for component in zip(contours, hierarchy):
            cntr = component[0]
            hier = component[1]

            if hier[3] > -1 and hier[2] < 0:
                cv2.drawContours(result, [cntr], 0, (0, 0, 255), 1)

cv2.destroyAllWindows()
