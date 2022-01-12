import cv2
import numpy as np


IMG_SIZE = 28
CLASS_NAMES = ['(', ')', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'div', 'minus', 'multi', 'plus']
MODEL_PATH = 'model'
PROB_TH = 0.75

def crop(img):
    height,width = img.shape[:2]
    w = int(width/15)
    h = int(height/15)
    
    return img[h:height-h,w:width-w,:]

def preproc_light(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = 1-gray
    return gray

def preproc(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3,3), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    thresh = cv2.dilate(thresh,(3,3),iterations=3)
    thresh = cv2.erode(thresh,(3,3),iterations=3)
    return thresh

def findContours(img):
    cnts = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    return cnts

def extractChar(img, contour, position=False):
    # Obtain bounding rectangle to get measurements
    x,y,w,h = cv2.boundingRect(contour)

    # Find centroid
    M = cv2.moments(contour)
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])

    # Crop
    roi = img[y:y+h, x:x+w]

    if position:
        return roi,x
    
    return roi

def scaleAndPad(img):
    # To make input images simmilar to train dataset ones,
    # There's a couple of adjustments to be made


    # Make it b&w
    _,img = cv2.threshold(img,150,255,cv2.THRESH_BINARY_INV)

    # Scale the larger side to IMG_SIZE
    height,width = img.shape[:2]
    factor = height/IMG_SIZE if height>width else width/IMG_SIZE
    height = int(height/factor)
    width = int(width/factor)

    img = cv2.resize(img,(width,height))


    # Add white px padding by laying img in the middle of a white background
    white = np.full((IMG_SIZE,IMG_SIZE),255,dtype='float32')
    x_offset, y_offset = int((IMG_SIZE-width)/2), int((IMG_SIZE-height)/2)
    white[y_offset:y_offset+height, x_offset:x_offset+width] = img

    return white

