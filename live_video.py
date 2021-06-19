import cv2
import joblib
import numpy as np

from utils import ShapeTransformer  # needed when loading the pickled model

RESOLUTION = (1280, 720)
TOP_LEFT_CORNER = (1078, 574)  # top left corner
BOTTOM_RIGHT_CORNER = (1195, 676)  # bottom right corner
DETECTION_THRESHOLD = 0.6

video = cv2.VideoCapture(0, cv2.CAP_DSHOW)
# video = cv2.VideoCapture(".\\img\\vid\\2021051618455200_s.mp4", cv2.CAP_DSHOW)
video.set(3, RESOLUTION[0])
video.set(4, RESOLUTION[1])
video.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))

with open("trained_model.pkl", "rb") as f:
    model = joblib.load(f)

while True:
    ret, frame = video.read()
    if ret == 0:
        print("video finished or error")
        break
    cv2.imshow("live", frame)

    # crop the image to focus on the position
    cropped_frame = frame[
        TOP_LEFT_CORNER[1] : BOTTOM_RIGHT_CORNER[1],
        TOP_LEFT_CORNER[0] : BOTTOM_RIGHT_CORNER[0],
    ]

    gray_cropped_frame = cv2.cvtColor(cropped_frame, cv2.COLOR_BGR2GRAY)

    # Get the probabilities of each category
    # looks like : [5%, 5%, 60%, 5%, 0%, 3%, 10%, 5%, 5%, 0%, 0%, 2%]
    probabilities = list(model.predict_proba(np.array([gray_cropped_frame]))[0])

    # The best prediction's index correspond to the position in the race
    best_prediction = max(probabilities)
    position = probabilities.index(best_prediction) + 1

    # Define a threshold to accept a prediction or not
    if best_prediction > DETECTION_THRESHOLD:
        print(position)
    else:
        print("not sure")

    # Press 'q' to quit. This also handles the delay in main loop
    if cv2.waitKey(1) == ord("q"):
        break

video.release()
cv2.destroyAllWindows()
