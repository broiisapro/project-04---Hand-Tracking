Hand Tracking with Finger Tip Distance Measurement
This project utilizes MediaPipe for hand tracking and OpenCV to calculate and visualize the distances between the tips of the fingers in millimeters. The code uses a webcam to track the user's hand, draw landmarks on the finger tips, connect the tips with lines, and display the real-world distance between them.

Features
Hand Tracking: Detects hand landmarks using MediaPipe.
Finger Tip Landmarks: Highlights the finger tips with blue dots and black outlines.
Distance Measurement: Displays the distance between each pair of adjacent finger tips in millimeters, calculated from pixel distances using a scaling factor based on an average hand size.
Real-time Video: Displays the webcam feed with overlaid hand tracking landmarks and distances.
Requirements
To run the project, you need to install the following dependencies:

Python 3.x (Recommended: Python 3.7+)
OpenCV: For video capture and drawing functions.
MediaPipe: For hand tracking and landmark detection.
You can install the necessary Python libraries with pip:

bash
Copy code
pip install opencv-python mediapipe
Usage
Clone the repository or download the script.

Run the script using Python:

bash
Copy code
python hand_tracking_distance.py
The program will open your webcam feed and start detecting hand landmarks. It will display:

Blue dots at the tips of your fingers with black outlines.
White lines connecting adjacent finger tips.
Distance in millimeters displayed at the midpoint of each line connecting finger tips.
To exit the application, press the Esc key.

Calibration
The distance between the finger tips is calculated in millimeters using a scaling factor (PIXELS_PER_CM). The default value is 30 pixels per centimeter, but this may need to be calibrated based on your camera's resolution and the distance of your hand from the camera.

You can calibrate the scaling factor by:

Measuring the real-world distance between two known landmarks (e.g., from the thumb tip to the pinky tip).
Measuring the pixel distance between the same landmarks in the webcam feed.
Adjusting the PIXELS_PER_CM value until the distance in millimeters matches the real-world measurement.
Code Overview
Hand Tracking: The script uses MediaPipe's Hands module to detect hand landmarks in real-time.
Finger Tip Detection: We extract the coordinates of the finger tips (indices 4, 8, 12, 16, and 20).
Distance Calculation: The Euclidean distance between each adjacent pair of finger tips is calculated in pixels, then converted to millimeters using a scaling factor (PIXELS_PER_CM).
Visualization: OpenCV is used to draw blue circles at the finger tips, connect them with white lines, and display the calculated distance at the midpoint of each line.
Example Output
The application will display the following:

Finger tips: Blue circles with black outlines.
Connecting lines: White lines connecting adjacent finger tips.
Distance (mm): Real-world distance (in mm) displayed between each pair of finger tips.
Troubleshooting
If the distances seem off, try adjusting the PIXELS_PER_CM value to match your camera setup.
Ensure that the camera is positioned in a well-lit area for better landmark detection accuracy.
