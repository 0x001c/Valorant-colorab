import cv2
import os
from mss import mss
import numpy as np
import win32api
import serial

fov = int(input("FOV: "))
sct = mss()
arduino = serial.Serial('COM5', 115200)

screenshot = sct.monitors[1]
screenshot['left'] = int((screenshot['width'] / 2) - (fov / 2))
screenshot['top'] = int((screenshot['height'] / 2) - (fov / 2))
screenshot['width'] = fov
screenshot['height'] = fov
center = fov/2

embaixo = np.array([141, 112, 196])
emcima = np.array([149, 197, 255])

speed = float(input("SPEED: "))

smooth_x = 0
smooth_y = 0
smoothing_factor = 0.7
def mousemove(x, y):
    if x < 0: 
        x = x + 256 
    if y < 0:
        y = y + 256
        
    x = max(0, min(255, int(x)))
    y = max(0, min(255, int(y)))
 
    pax = [x, y]
    arduino.write(bytearray(pax))
 
while True:
    if win32api.GetAsyncKeyState(0x02) < 0:
        img = np.array(sct.grab(screenshot))
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, embaixo,emcima)
        kernel = np.ones((3,3), np.uint8)
        dilated = cv2.dilate(mask,kernel,iterations= 5)
        thresh = cv2.threshold(dilated, 60, 255, cv2.THRESH_BINARY)[1]
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        if len(contours) != 0:
            closest_contour = None
            min_distance_to_center = float('inf')
            
            for contour in contours:
                x, y, w, h = cv2.boundingRect(contour)
                
                if w < 8 or h < 10:
                    continue
                
                head_center_x = x + w // 2
                head_center_y = y + int(h * 0.20)
                
                distance_to_center = ((head_center_x - center)**2 + (head_center_y - center)**2)**0.5
                
                if distance_to_center < min_distance_to_center:
                    min_distance_to_center = distance_to_center
                    closest_contour = contour
            
            if closest_contour is not None:
                x, y, w, h = cv2.boundingRect(closest_contour)
                
                center_x = x + w // 2
                target_y = y + int(h * 0.20)
                
                diff_x = int(center_x - center)
                diff_y = int(target_y - center)
                
                dead_zone = 5
                
                if abs(diff_x) > dead_zone or abs(diff_y) > dead_zone:
                    distance = (diff_x**2 + diff_y**2)**0.5
                    
                    if distance > 50:
                        speed_multiplier = 1.0
                    elif distance > 25:
                        speed_multiplier = 0.6
                    elif distance > 10:
                        speed_multiplier = 0.3
                    else:
                        speed_multiplier = 0.1
                    
                    alvo_x = diff_x * speed * speed_multiplier
                    alvo_y = diff_y * speed * speed_multiplier
                        
                    mousemove(alvo_x, alvo_y)