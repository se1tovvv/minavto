import cv2
import dlib
from scipy.spatial import distance as dist
import time

# Load the face detector and facial landmark predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# Define eye aspect ratio (EAR) and blink threshold values
EAR_THRESHOLD = 0.25  # You may need to adjust this threshold based on your setup
BLINK_CONSEC_FRAMES = 3
ASLEEP_THRESHOLD_SECONDS = 5

def eye_aspect_ratio(eye):
    # Compute the Euclidean distances between the two sets of vertical eye landmarks
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])

    # Compute the Euclidean distance between the horizontal eye landmarks
    C = dist.euclidean(eye[0], eye[3])

    # Compute the eye aspect ratio
    ear = (A + B) / (2.0 * C)
    return ear

def main():
    cap = cv2.VideoCapture(0)  # You can change the argument to use a different camera

    # Initialize variables for blink detection and drowsiness detection
    blink_counter = 0
    asleep_start_time = None

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the grayscale frame
        faces = detector(gray)

        for face in faces:
            shape = predictor(gray, face)
            shape = shape_to_list(shape)

            left_eye = shape[42:48]
            right_eye = shape[36:42]

            # Calculate the eye aspect ratio for both eyes
            left_ear = eye_aspect_ratio(left_eye)
            right_ear = eye_aspect_ratio(right_eye)

            # Calculate the average eye aspect ratio
            avg_ear = (left_ear + right_ear) / 2.0

            # Check if the average eye aspect ratio is below the threshold
            if avg_ear < EAR_THRESHOLD:
                blink_counter += 1

                if blink_counter >= BLINK_CONSEC_FRAMES:
                    # The driver is drowsy
                    print("Driver is drowsy")

                    # If the driver has been drowsy for a certain duration, consider them asleep
                    if asleep_start_time is None:
                        asleep_start_time = time.time()
                    elif time.time() - asleep_start_time >= ASLEEP_THRESHOLD_SECONDS:
                        print("Driver is asleep")

            else:
                blink_counter = 0
                asleep_start_time = None

        cv2.imshow("Driver Monitoring", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def shape_to_list(shape):
    coordinates = []
    for i in range(0, 68):
        coordinates.append((shape.part(i).x, shape.part(i).y))
    return coordinates

if __name__ == "__main__":
    main()
