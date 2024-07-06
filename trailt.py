import cv2
import mediapipe as mp
import pyautogui

# Initialize webcam
cam = cv2.VideoCapture(0)

# Initialize MediaPipe Face Mesh
face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)

# Get screen width and height
screen_w, screen_h = pyautogui.size()

# Set the speed multiplier
speed_multiplier = 2  # Adjust this value to increase or decrease the speed

while True:
    # Read frame from webcam
    _, frame = cam.read()
    frame = cv2.flip(frame, 1)
    
    # Convert the frame to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Process the frame to find face landmarks
    output = face_mesh.process(rgb_frame)
    landmark_points = output.multi_face_landmarks
    
    frame_h, frame_w, _ = frame.shape
    
    if landmark_points:
        landmarks = landmark_points[0].landmark
        
        # Draw landmarks and move mouse pointer
        for id, landmark in enumerate(landmarks[474:478]):
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            cv2.circle(frame, (x, y), 3, (0, 255, 0))
            if id == 1:
                screen_x = screen_w * landmark.x * speed_multiplier
                screen_y = screen_h * landmark.y * speed_multiplier
                pyautogui.moveTo(screen_x, screen_y)
        
        # Check for blink to simulate click
        left = [landmarks[145], landmarks[159]]
        for landmark in left:
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            cv2.circle(frame, (x, y), 3, (0, 255, 255))
        if (left[0].y - left[1].y) < 0.004:
            pyautogui.click()
            pyautogui.sleep(1)
    
    # Display the frame
    cv2.imshow('Eye Controlled Mouse', frame)
    cv2.waitKey(1)
