#this is a sample code file uploading for AI in embedded systems course assignment.
# Git training - assignment 3
# this piece of code extracts musical symbols from music sheets using morphology.

import numpy as np
import cv2
from numpy import angle
import math
from typing import Tuple, Union
from deskew import determine_skew



def Showing_Function(winname, img):
    cv2.imshow(winname, img)
    cv2.waitKey(0)
    cv2.destroyWindow(winname)
    
#Loading Source Image
src=cv2.imread("1.jpeg")
Showing_Function("src", src)


#GrayScale
gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
Showing_Function("gray", gray)

# a function to check if the image needs to be deskewed through deskew library
def rotate(image: np.ndarray, angle: float, background: Union[int, Tuple[int, int, int]]) -> np.ndarray:
    old_width, old_height = image.shape[:2]
    angle_radian = math.radians(angle)
    width = abs(np.sin(angle_radian) * old_height) + abs(np.cos(angle_radian) * old_width)
    height = abs(np.sin(angle_radian) * old_width) + abs(np.cos(angle_radian) * old_height)
    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
    rot_mat[1, 2] += (width - old_width) / 2
    rot_mat[0, 2] += (height - old_height) / 2
    return cv2.warpAffine(image, rot_mat, (int(round(height)), int(round(width))), borderValue=background)


# deskewing the image if it's neccessary
angle = determine_skew(gray)
fixed_src = rotate(gray, angle, (255, 255, 255))
Showing_Function("fixed source image", fixed_src)
cv2.imwrite('fixed.jpeg', fixed_src)



# thresholding
ret, thresh1 = cv2.threshold(fixed_src, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
Showing_Function("thresh", thresh1)
cv2.imwrite('thresh.jpeg ', thresh1)

# extract the vertical and horizontal lines of the image
horizontal = np.copy(thresh1)
vertical = np.copy(thresh1)

# Specify size on horizontal and vertical axis
cols = horizontal.shape[1]
horizontal_size = cols // 30
rows = vertical.shape[0]
vertical_size = rows // 30


# Create structuring element for extracting horizontal lines through morphology operations
horizontalSE = cv2.getStructuringElement(cv2.MORPH_RECT, (horizontal_size, 1))

# Apply morphology operations
horizontal = cv2.erode(horizontal, horizontalSE)
horizontal = cv2.dilate(horizontal, horizontalSE)

# Show extracted horizontal lines
Showing_Function("horizontal", horizontal)
cv2.imwrite('horizontal.jpeg ', horizontal)

# Create structuring element for extracting vertical lines through morphology operations
verticalSE = cv2.getStructuringElement(cv2.MORPH_RECT, (1,vertical_size))

# Apply morphology operations
vertical = cv2.erode(vertical, verticalSE)
vertical = cv2.dilate(vertical, verticalSE)

# Show extracted vertical lines
Showing_Function("vertical", vertical)
cv2.imwrite('vertical.jpeg ', vertical)

# Opening on vertical picture - Good for removing noise
kernel = np.ones((2,2), np.uint8)
opening = cv2.morphologyEx(vertical, cv2.MORPH_OPEN, verticalSE)
Showing_Function('Opening', opening)
cv2.imwrite('opening.jpeg ', opening)

    #step 1
edges = cv2.adaptiveThreshold(opening, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 3, -2)
Showing_Function("edges", edges)
cv2.imwrite('edges.jpeg ', edges)

    # Step 2
kernel = np.ones((2, 2), np.uint8)
edges = cv2.dilate(edges, kernel)
Showing_Function("dilate", edges)
cv2.imwrite('dilate.jpeg ', edges)
    # Step 3
smooth = np.copy(opening )

    # Step 4
smooth = cv2.blur(smooth, (2, 2))
cv2.imwrite('smooth.jpeg ', smooth)
    # Step 5
(rows, cols) = np.where(edges != 0)
opening[rows, cols] = smooth[rows, cols]

# Show final result
Showing_Function("smooth - final", opening)
cv2.imwrite('Final_Smooth.jpeg ', opening)

# detecting the contours on the opening image
contours, hierarchy = cv2.findContours(image=opening, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
img = cv2.drawContours(fixed_src, contours, -1, (255,255,255), 1)
boxes = []
for c in contours:
     x,y,w,h = cv2.boundingRect(c)
     cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),1)
     #cv2.rectangle(img,(x-5,y-5),(x+w,y+(h*10)),(0,0,255),1)
     #cv2.rectangle(img,(x-5,y),(x+w*2,y+h),(0,0,255),1)
     #cv2.rectangle(img,(x-5,y),(x+w,y+h),(0,0,255),1)
    
Showing_Function("src - final", img)
cv2.imwrite('Final_Result.jpeg ', img)
cv2.destroyAllWindows()


