import cv2 
import math
import numpy as np 
import matplotlib.pyplot as plt
import pytesseract as teser
from imutils import contours
import glob
from PIL import Image

def meter(im):

    row,col,ch = im.shape

    gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY) 

    thresh = cv2.threshold(gray, 0, 255,cv2.THRESH_BINARY_INV|cv2.THRESH_OTSU)[1]
    kernal = np.ones((3,3),np.uint8)
    edge = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernal,iterations = 1)

    edge = cv2.dilate(edge,kernal, iterations = 1)

    ker = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
    plt.imshow(im)
    plt.show()


    cnt = cv2.findContours(edge,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    i = 0
    preds = []
    final = []
    xx = []
    for c in cnt[0]: 
        (x,y,w,h) = cv2.boundingRect(c) 

        if(w>25 and w<45) and (h>70 and h<100): 
            crop1 = edge[y:y+h,x:x+w]
            crop1 = cv2.resize(crop1,(45,90))
            xx.append(x)
           
            j=0      
            digits = glob.glob('/users/eapplestroe/digits/*.jpg')
           
            for d in digits:
                ref = Image.open(d)
                
                g = cv2.cvtColor(np.uint8(ref),cv2.COLOR_BGR2GRAY)
                g = cv2.threshold(g, 0, 250, cv2.THRESH_BINARY_INV|cv2.THRESH_OTSU)[1] 

                g = cv2.morphologyEx(g,cv2.MORPH_OPEN,kernal,iterations = 1)


                result = cv2.matchTemplate(g,crop1,cv2.TM_CCOEFF)

                (_,pred,_,_) = cv2.minMaxLoc(result)
                preds.append(pred)
            a = np.argmax(preds)
            preds.clear()
            final.append(digits[a][26])
            

    for i in range(np.size(xx)-1):
        y = xx[i]
        for j in range(i,np.size(xx)-1): 
            y = xx[i]
            if y > xx[j+1]:
                temp = final[j+1]
                final[j+1] = final[i]
                final[i] = temp
                t = xx[j+1]
                xx[j+1] = xx[i]
                xx[i] = t
    return final 

if __name__ == '__main__':
    im = cv2.imread('/Users/eapplestroe/Meter/meter1123.jpg') #Path to Image here
    result = meter(im)
    reading = result[0]

    for i in range (len(result)):
        if i == 0:
            continue
        else:
            reading = reading+result[i]
    print('Meter Reading = ',reading)
    final = im.copy()
    cv2.putText(final,'Reading: '+reading, (100,100),cv2.FONT_HERSHEY_COMPLEX, 3, (0,0,255), 5)
    #im = cv2.resize(im,(0,0),fx = 0.25,fy = 0.25)
    #cv2.imwrite("Result.jpg",final)
    cv2.imshow('Original',final) 
    cv2.waitKey(0) 
    cv2.destroyAllWindows()
