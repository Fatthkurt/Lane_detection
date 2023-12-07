import cv2
import numpy as np

def detect_lines(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 100, 200, apertureSize=3)
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 100, minLineLength=50, maxLineGap=10)

    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv2.line(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)

    return frame

# create a mask 
def create_mask(frame):
    height, width = frame.shape[:2]
    mask = np.zeros_like(frame)

    vertices = np.array([[(0, 250),(0, height), (width, height), (width*80, height*2)]], dtype=np.int32)


    cv2.fillPoly(mask, vertices, (255, 255, 255))

    masked = cv2.bitwise_and(frame, mask)

    return masked

# Read the video file
cap = cv2.VideoCapture("Videos/test_video.mp4")
# Loop over the frames
while cap.isOpened():
    ret, frame = cap.read()

    if ret:
        frame = create_mask(frame)

        frame = detect_lines(frame)

        cv2.imshow('video', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()
