import cv2
import numpy as np

# Define a function to apply Canny edge detection and Probabilistic Hough Line Transform
def detect_lines(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 100, 200, apertureSize=3)
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 100, minLineLength=50, maxLineGap=10)

    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv2.line(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)

    return frame

# Define a function to create a mask for a region of interest
def create_mask(frame):
    height, width = frame.shape[:2]
    mask = np.zeros_like(frame)

    # Define a polygonal contour that covers the road
    vertices = np.array([[(0, 250),(0, height), (width, height), (width*80, height*2)]], dtype=np.int32)


    # Fill the contour with white color
    cv2.fillPoly(mask, vertices, (255, 255, 255))

    # Apply a bitwise AND operation between the mask and the frame
    masked = cv2.bitwise_and(frame, mask)

    return masked

# Read the video file
cap = cv2.VideoCapture("Videos/test_video.mp4")
# Loop over the frames
while cap.isOpened():
    ret, frame = cap.read()

    # Check if the frame is valid
    if ret:
        # Apply a mask to the frame
        frame = create_mask(frame)

        # Detect lines on the frame
        frame = detect_lines(frame)

        # Show the frame
        cv2.imshow('video', frame)

        # Wait for a key press or end of video
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

# Release the video capture and destroy the windows
cap.release()
cv2.destroyAllWindows()