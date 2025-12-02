"""
Simplified Hand Tracker - Basic version for testing
"""

import cv2
import numpy as np
import time

print("Starting simple hand tracker...")
print("Press 'q' to quit")

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("ERROR: Cannot open camera")
    exit()

print("Camera opened! Windows should appear...")

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    frame = cv2.flip(frame, 1)
    
    # Simple text
    cv2.putText(frame, "Hand Tracker Test", (10, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.putText(frame, "Press 'q' to quit", (10, 70), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    
    # Draw center circle
    cv2.circle(frame, (320, 240), 100, (0, 255, 255), 2)
    
    cv2.imshow('Simple Test', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
print("Done!")
