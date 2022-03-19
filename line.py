import cv2 as cv
import numpy as np
import random
import math

#img = cv.imread('/Users/local/Downloads/IMG_9912.jpg') 12 13 17
img = cv.imread('C:/Users/Lucas/Downloads/IMG_9917.jpg')

height = img.shape[0]
width = img.shape[1]
channels = img.shape[2]
#print(height,width)

gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

# Use canny edge detection
edges = cv.Canny(gray, 5000, 8000, apertureSize=5)

kernel_size = 15
edges = cv.GaussianBlur(edges,(kernel_size, kernel_size),0)


lines = cv.HoughLinesP(
      edges, # Input edge image
      1, # Distance resolution in pixels
      np.pi/180, # Angle resolution in radians
      threshold=1000, # Min number of votes for valid line
      minLineLength=1100, # Min allowed length of line
      maxLineGap=10 # Max allowed gap between line for joining them
      )
#print(len(lines))
# #print(lines)
slopelst=[]



for points in lines:
    ##print(points)
    # Extracted points nested in the list
    slope=1
    x1,y1,x2,y2=points[0]
    if x2-x1==0:
        pass
    else:
        slope=(y1-y2)/(x2-x1)

    color1=random.randint(0, 255)
    color2 = random.randint(0, 255)
    color3 = random.randint(0, 255)
    slopelst.append(slope)


##print(lines)
status=True
for x in slopelst:
    if x>0:
        status=False
#True negative false positive
side1=[]
side0=[]
if status==True:
    x1, y1, x2, y2 = lines[0][0]
    #print(f"Reference intercept: {firstintercept}")
    max, min = 0, 100000
    for x in range(len(lines)):
        x1, y1, x2, y2 = lines[x][0]
        slope = slopelst[x]
        yintercept = y1 - (-x1 * slope)
        if yintercept < min:
            min = yintercept
        elif yintercept > max:
            max = yintercept
        # #print(yintercept)
    reference = (max + min) / 2
    #print(f"MAX: {max} MIN: {min}")
    #print(f"REFERENCE: {reference}")
    for x in range(len(lines)):
        x1, y1, x2, y2 = lines[x][0]
        slope = slopelst[x]
        yintercept = y1 - (-x1 * slope)
        #print(f"ycept: {yintercept}")
        # #print(yintercept)
        if yintercept >= reference:

            side1.append([x1, y1, x2, y2])
        else:
            #
            side0.append([x1, y1, x2, y2])
    # 0 is one side, 1 is another side

else:

    x1, y1, x2, y2 = lines[0][0]
    #print(f"Reference intercept: {firstintercept}")
    max,min=0,100000
    for x in range(len(lines)):
        x1, y1, x2, y2 = lines[x][0]
        slope=slopelst[x]
        yintercept=y1-(x1*slope)
        if yintercept<min:
            min=yintercept
        elif yintercept>max:
            max=yintercept
        ##print(yintercept)
    reference=(max+min)/2
    #print(f"MAX: {max} MIN: {min}")
    #print(f"REFERENCE: {reference}")
    for x in range(len(lines)):
        x1, y1, x2, y2 = lines[x][0]
        slope=slopelst[x]
        yintercept=y1-(x1*slope)
        #print(f"ycept: {yintercept}")
        ##print(yintercept)
        distance=100
        if yintercept >=reference :

            #cv.line(img, (x1, y1), (x2, y2), (0, 0, 255), 4)
            side1.append([x1, y1, x2, y2])
        else:
            #cv.line(img, (x1, y1), (x2, y2), (0, 255, 0), 4)
            side0.append([x1, y1, x2, y2])
    #0 is one side, 1 is another side

#print(lines)
#print(sides)
#
# for x in range(len(lines)):
#     x1, y1, x2, y2 = lines[x][0]
#     if sides[x]==1:
#         cv.line(img,(x1,y1),(x2,y2),(0,0,255),4)
#         side1.append([x1, y1, x2, y2])
#     if sides[x]==0:
#         cv.line(img,(x1,y1),(x2,y2),(0,255,0),4)
#         side0.append([x1, y1, x2, y2])

min1x=0
min0x=0
max1y=0
max0y=0

finalset=[[],[]]

for x in side1:
    if x[1]>max1y:
        max1y=x[1]
        max1x=x[0]
        finalset[0]=x
    if x[3]>max1y:
        max1y = x[3]
        max1x = x[2]
        finalset[0] = x
for x in side0:
    if x[1]>max0y:
        max0y=x[1]
        max0x=x[0]
        finalset[1] = x
    if x[3]>max0y:
        max0y = x[3]
        max0x = x[2]
        finalset[1] = x

#print(f"side1: {max1x} {max1y}")
#print(f"side0: {max0x} {max0y}")

midpt=((max0x+max1x)//2,(max0y+max1y)//2)
#(y1-y2)/(x2-x1)

slope1=(finalset[0][1] - finalset[0][3]) / (finalset[0][2] - finalset[0][0])
slope2=(finalset[1][1] - finalset[1][3]) / (finalset[1][2] - finalset[1][0])

#print(slope1)
#print(slope2)
#print(math.atan(slope1))
#print(math.atan(slope2))
if slope1<0 and slope2<0:
    avgangle = (np.pi-math.atan(-slope1) + np.pi-math.atan(-slope2)) / 2

elif slope1<0 and slope2>0:
    avgangle = (np.pi - math.atan(-slope1) + math.atan(slope2)) / 2
elif slope1<0 and slope2>0:
    avgangle = (math.atan(slope1) + np.pi - math.atan(-slope2)) / 2
else:
    avgangle = (math.atan(slope1) + math.atan(slope2)) / 2

#print(avgangle)

length=math.sqrt(1000000/(1+(math.tan(avgangle))**2))
if math.tan(avgangle)>0:
    endpt = (int(midpt[0] + length), int(midpt[1] - length * math.tan(avgangle)))
else:
    endpt = (int(midpt[0] - length), int(midpt[1] + length * math.tan(avgangle)))
#cv.line(img,midpt,endpt,(color1,color2,color3),10)
img = cv.arrowedLine(img, midpt, endpt,(color1,color2,color3), 10)

#cv.namedWindow("output",cv.WINDOW_NORMAL)
cv.imshow('output', img)  # Initial Capture
# cv.imshow('frame1', gray)
#cv.imshow('output', edges)# Transformed Capture

#cv.imwrite('C:/Users/Lucas/Downloads/img3.jpg',img)

cv.waitKey()
img.release()
cv.destroyAllWindows()










