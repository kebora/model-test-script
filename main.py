import cv2
import mediapipe as mp

# Load the MediaPipe Task for gesture recognition
mp_tasks = mp.tasks
GestureRecognizer = mp_tasks.vision.GestureRecognizer

# Load the gesture recognizer model from the .task file
with GestureRecognizer.create_from_model_path('ishara.task') as recognizer:
    # Initialize webcam feed
    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Convert the BGR image to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Create a MediaPipe Image object
        mp_image = mp.Image(mp.ImageFormat.SRGB, rgb_frame)

        # Perform gesture recognition
        gesture_result = recognizer.recognize(mp_image)

        if gesture_result.gestures:
            # Extract the top recognized gesture and its confidence
            gesture = gesture_result.gestures[0][0].category_name
            confidence = gesture_result.gestures[0][0].score

            # Display the recognized gesture and confidence on the frame
            cv2.putText(frame, f'Gesture: {gesture} ({confidence:.2f})', (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

        # Show the frame with recognized gestures
        cv2.imshow('Gesture Recognition', frame)

        # Exit on pressing 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the resources
    cap.release()
    cv2.destroyAllWindows()
