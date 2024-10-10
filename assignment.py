import streamlit as st
import cv2
from datetime import datetime

st.title('Motion Detection')
start =  st.button('Start Camera')

if start:
    streamlit_image = st.image([])
    camera = cv2.VideoCapture(0)
    now = datetime.now()
    today = now.strftime("%A")  
    current_time = now.strftime("%H:%M:%S") 
    
    combined_text = f"{today}, {current_time}"
    
    while True:
        check, frame = camera.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        cv2.putText(img=frame, text = combined_text, org=(50,50),
                    fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=2, thickness=2,
                    lineType=cv2.LINE_AA)

        streamlit_image.image(frame)