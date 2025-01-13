import cv2
import mediapipe as mp
import math
import time

# Set up hand tracking
hand_model = mp.solutions.hands
hand_tracking = hand_model.Hands()
drawing_utils = mp.solutions.drawing_utils

# Open webcam
camera = cv2.VideoCapture(0)

# Function to calculate distance between two points
def calculate_distance(point1, point2):
    delta_x = point2[0] - point1[0]
    delta_y = point2[1] - point1[1]
    return math.sqrt(delta_x ** 2 + delta_y ** 2)

# Set some constants
hand_size = 19
random_number = 30
finger_tip_indices = [4, 8, 12, 16, 20]
radius = 10

# Flip image horizontally
def flip_image_horizontally(image):
    return cv2.flip(image, 1)

# Convert BGR to RGB
def convert_bgr_to_rgb(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Process hand landmarks
def process_hand_landmarks(image_rgb):
    return hand_tracking.process(image_rgb)

# Draw hand landmarks
def draw_hand_landmarks(image, landmarks):
    drawing_utils.draw_landmarks(image, landmarks, hand_model.HAND_CONNECTIONS)

# Draw finger tip
def draw_finger_tip(image, position, radius):
    cv2.circle(image, position, radius, (0, 0, 0), 2)
    cv2.circle(image, position, radius - 3, (255, 0, 0), -1)

# Draw line between two points
def draw_line(image, start_point, end_point, color, thickness):
    cv2.line(image, start_point, end_point, color, thickness)

# Put text on image
def put_text(image, text, position, font_size=0.4, color=(0, 255, 0), thickness=1):
    cv2.putText(image, text, position, cv2.FONT_HERSHEY_SIMPLEX, font_size, color, thickness, cv2.LINE_AA)

# Main loop
while True:
    ret, frame = camera.read()
    if not ret:
        print("Error: No frame captured")
        break

    # Flip and convert image
    frame = flip_image_horizontally(frame)
    rgb_frame = convert_bgr_to_rgb(frame)

    # Get hand landmarks
    hand_landmarks_results = process_hand_landmarks(rgb_frame)

    if hand_landmarks_results.multi_hand_landmarks:
        for hand_landmarks in hand_landmarks_results.multi_hand_landmarks:
            draw_hand_landmarks(frame, hand_landmarks)

            finger_positions = []
            for finger_tip_index in finger_tip_indices:
                landmark = hand_landmarks.landmark[finger_tip_index]
                x = int(landmark.x * frame.shape[1])
                y = int(landmark.y * frame.shape[0])
                finger_positions.append((x, y))
                draw_finger_tip(frame, (x, y), radius)

            for i in range(len(finger_positions) - 1):
                draw_line(frame, finger_positions[i], finger_positions[i + 1], (255, 255, 255), 2)

            for i in range(len(finger_positions) - 1):
                distance_pixels = calculate_distance(finger_positions[i], finger_positions[i + 1])
                distance_cm = distance_pixels / random_number

                mid_point = ((finger_positions[i][0] + finger_positions[i + 1][0]) // 2,
                             (finger_positions[i][1] + finger_positions[i + 1][1]) // 2)

                put_text(frame, f"{distance_cm:.2f} cm", mid_point)

        print("hand(s) found")

    else:
        print("No hands on screen")

    # Show frame
    cv2.imshow("Hand Tracking", frame)

    # Press ESC to exit
    if cv2.waitKey(1) & 0xFF == 27:
        break

camera.release()
cv2.destroyAllWindows()
