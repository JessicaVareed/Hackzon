

import matplotlib.pylab as plt
import cv2
import numpy as np



def region_mask(img, vert):
    mask=np.zeros_like(img)
    #count=img.shape[2]
    match_colour=255
    
    cv2.fillPoly(mask, vert, match_colour)
    maskedImage= cv2.bitwise_and(img,mask)
    return maskedImage


def drawLines(img, lines):
    cpimg=np.copy(img)
    blankImage= np.zeros((cpimg.shape[0], img.shape[1], 3), dtype= np.uint8)
    
    for line in lines:
        for x1, y1, x2, y2 in line:
            cv2.line(img, (x1,y1), (x2,y2), (0,255,0), thickness=3)

    img=cv2.addWeighted(img, 0.8, blankImage, 1, 0.0)
    return img



def process(image):
    print(image.shape)
    height= image.shape[0]
    width= image.shape[1]
    
    region_vertice=[(0,height),
            (width/2,height/2),
            (width,height)]
    
    
    grayImage=cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    
    cannyImage= cv2.Canny(grayImage, 100, 120)
    
    cropImage= region_mask(cannyImage, np.array([region_vertice],np.int32))
    
    line= cv2.HoughLinesP(cropImage, rho=2, theta=np.pi/60, threshold=50,
                           lines=np.array([]),
                           minLineLength=40, maxLineGap=25)
    
    imageLines=drawLines(image, line)
    return imageLines

#image processing

image =cv2.imread('lane.jpg')
image= cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
f1=process(image)
plt.imshow(f1)
plt.show()



#video processing

cap= cv2.VideoCapture('test_video.mp4')

while(cap.isOpened()):
    ret, frame= cap.read()
    frame= process(frame)
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()
    