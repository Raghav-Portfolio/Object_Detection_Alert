import cv2
import time
from emailing import send_email

video = cv2.VideoCapture(0)
time.sleep(1)

first_frame = None

while True:
    status = 0
    status_list = []
    
    check, frame = video.read()
    grayscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    grayscale_gaussian = cv2.GaussianBlur(grayscale, (21,21), 0) 
    
    if first_frame is None:
        first_frame = grayscale_gaussian
    
    delta_frame = cv2.absdiff(first_frame, grayscale_gaussian)
    thresh = cv2.threshold(delta_frame, 70, 255, cv2.THRESH_BINARY)[1] #The objective is to make the foreground as light as possible and the background as dark as possible
    dil_frame = cv2.dilate(thresh, None, iterations=2)
    
    contours, check = cv2.findContours(dil_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    for contour in contours:
        if cv2.contourArea(contour)<5000: # if this is a small object, it's a false positive and should be skipped
            continue
        
        x,y,w,h = cv2.boundingRect(contour)
        rectangle = cv2.rectangle(frame, (x,y), (x+w,y+h), (0, 255, 0), 3)
        if rectangle.any():
            status = 1
            
    status_list.append(status)
    print(status_list)
    status_list =  status_list[-2:]
    
    if status_list[0] == 1 and status_list[1] == 0:
        send_email()
        
    cv2.imshow("My Video", frame)
    key = cv2.waitKey()
    
    if key == ord('q'):
        break

video.release()    
