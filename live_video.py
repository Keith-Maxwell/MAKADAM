import cv2
import joblib
import numpy as np

from utils import (
    RGB2Gray2ShapeTransformer,  # needed when loading the pickled model
)

RESOLUTION = (1280, 720)
TOP_LEFT_CORNER = (1078, 574)  # top left corner
BOTTOM_RIGHT_CORNER = (1195, 676)  # bottom right corner
DETECTION_THRESHOLD = 0.75

video = cv2.VideoCapture(0, cv2.CAP_DSHOW)
# video = cv2.VideoCapture(".\\img\\vid\\2021051618455200_s.mp4", cv2.CAP_DSHOW)
video.set(3, RESOLUTION[0])
video.set(4, RESOLUTION[1])
video.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))

with open("trained_model.pkl", "rb") as f:
    model = joblib.load(f)

while True:
    ret, frame = video.read()
    # if not ret:
    #     print("video finished or error")
    #     break
    cv2.imshow("live", frame)

    # crop the image to focus on the position
    cropped_frame = frame[
        TOP_LEFT_CORNER[1] : BOTTOM_RIGHT_CORNER[1],
        TOP_LEFT_CORNER[0] : BOTTOM_RIGHT_CORNER[0],
    ]
    probabilities = list(model.predict_proba(np.array([cropped_frame]))[0])
    best_prediction = max(probabilities)
    position = probabilities.index(best_prediction) + 1
    if best_prediction < DETECTION_THRESHOLD:
        print("not sure")
    else:
        print(position)

    if cv2.waitKey(1) == ord("q"):
        break

video.release()
cv2.destroyAllWindows()
