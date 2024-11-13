import cv2
import mediapipe as mp
import math

# Initialize MediaPipe Hands and drawing utils
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils

# Initialize the camera
camera = cv2.VideoCapture(0)

# Function to calculate Euclidean distance between two points
def calculate_distance(point1, point2):
    return math.sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2)

# Define average hand size (in centimeters)
AVG_HAND_SIZE_CM = 19  # Typical hand size in cm

# Estimate pixels per cm based on average hand size
# This is an adjustable value that can be fine-tuned based on your camera and distance setup
PIXELS_PER_CM = 30  # Estimated pixels per cm (this might need to be calibrated)

# List of landmark indices for finger tips
FINGER_TIPS = [4, 8, 12, 16, 20]  # Thumb, Index, Middle, Ring, Pinky

# Larger radius for finger tip landmarks
TIP_RADIUS = 9  # Increase this value for larger dots at finger tips

# Color selection for the distance between finger tips
rgb_color = (255, 255, 255) #RGB format, adjust based on your backgound, mine is dark so the text is white

while True:
    # Capture frame-by-frame
    ret, image = camera.read()

    if not ret:
        print("Failed to grab frame")
        break

    # Flip the image horizontally for a mirror effect
    image = cv2.flip(image, 1)

    # Convert the image to RGB (required by MediaPipe)
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Process the image and get hand landmarks
    results = hands.process(rgb_image)

    # Check if any hands are detected
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Draw connections between landmarks (white lines)
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Store coordinates for each finger tip
            finger_coords = []

            for tip_index in FINGER_TIPS:
                lm = hand_landmarks.landmark[tip_index]
                x, y = int(lm.x * image.shape[1]), int(lm.y * image.shape[0])
                finger_coords.append((x, y))
                # Draw blue circle at each finger tip with a black outline
                cv2.circle(image, (x, y), TIP_RADIUS, (0, 0, 0), 2)  # Black outline
                cv2.circle(image, (x, y), TIP_RADIUS - 2, (255, 0, 0), -1)  # Blue fill

            # Connect the finger tips with white lines
            for i in range(len(finger_coords) - 1):
                cv2.line(image, finger_coords[i], finger_coords[i + 1], (255, 255, 255), 2)

            # Calculate and display the distances between each pair of adjacent fingers
            for i in range(len(finger_coords) - 1):
                # Calculate pixel distance
                dist_pixels = calculate_distance(finger_coords[i], finger_coords[i + 1])

                # Convert pixel distance to millimeters using the estimated scaling factor
                dist_mm = dist_pixels / PIXELS_PER_CM * 10  # Convert to mm (1 cm = 10 mm)

                # Midpoint for the line connecting the two finger tips
                mid_point = ((finger_coords[i][0] + finger_coords[i + 1][0]) // 2,
                             (finger_coords[i][1] + finger_coords[i + 1][1]) // 2)

                # Display the distance in mm at the midpoint of the line
                cv2.putText(image, f"{dist_mm:.1f} mm", mid_point, cv2.FONT_HERSHEY_SIMPLEX, 0.5, rgb_color, 1, cv2.LINE_AA)

    # Display the image with landmarks and distances
    cv2.imshow("Hand Tracking with Finger Tip Distances", image)

    # Exit the loop when the 'Esc' key is pressed
    if cv2.waitKey(1) & 0xFF == 27:
        break

# Release the camera and close OpenCV windows
camera.release()
cv2.destroyAllWindows()
