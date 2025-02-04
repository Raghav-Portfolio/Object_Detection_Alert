import glob
import os
import cv2
import time
from emailing import send_email
from threading import Thread

video = cv2.VideoCapture(0)
time.sleep(1)

first_frame = None
status_list = []
count = 1

def clean_folder():
    print('clean_folder started')
    images = glob.glob('images/*.png')
    for image in images:
        os.remove(image)
    print('clean_folder has ended')
while True:
    status = 0
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
            cv2.imwrite(f"images/{count}.png", frame)
            count += 1
            all_images = glob.glob('images/*.png')
            # grab the frame in the middle from the time an object enters to the time they exit the video:
            index = int(len(all_images)/2) 
            image_with_object = all_images[index]
        
    status_list.append(status)
    status_list =  status_list[-2:]
    
    if status_list[0] == 1 and status_list[1] == 0:
        email_thread = Thread(target=send_email, args=(image_with_object, ))
        email_thread.daemon = True
        clean_thread = Thread(target=clean_folder)
        clean_thread.daemon = True
        
        email_thread.start()
        
        
    cv2.imshow("My Video", frame)
    key = cv2.waitKey()
    
    if key == ord('q'):
        break

video.release()    
clean_thread.start() # images should only be deleted after the press of the 'q' key