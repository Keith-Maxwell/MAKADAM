import json
from time import time

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

is_computing = False
last_10_pos = []
while True:
    ret, frame = video.read()
    if ret == 0:
        print("video finished or error")
        break

    # Display a red circle when not doing anything and a green circle when computing
    cv2.circle(
        frame,  # image
        (RESOLUTION[0] // 2, RESOLUTION[1] // 10),  # center
        40,  # radius
        (0, 255, 0) if is_computing else (0, 0, 255),  # color
        -1,  # thickness (-1 means filled)
    )

    if is_computing:
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

            # Save the last 5 position to smooth the recordings
            last_10_pos.append(position)
            if len(last_10_pos) > 10:
                last_10_pos.pop(0)

            print(last_10_pos)

            if all([x == position for x in last_10_pos]):
                records[time() - start_time] = position

            # simple display on the video
            cv2.putText(
                frame,
                str(position),
                TOP_LEFT_CORNER,
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 255, 255),
                3,
            )
        else:
            cv2.putText(
                frame, "???", TOP_LEFT_CORNER, cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 3
            )

    cv2.imshow("live", frame)

    # wait 1 milisecond for a key press
    key = cv2.waitKey(1)
    # Press 'q' to quit.
    if key == ord("q"):
        break
    # Press 'Space' to toggle the position computing
    if key == ord(" "):
        # Toggle from recording to not recording
        if is_computing == True:
            # save results
            with open("records.json", "w+") as f:
                json.dump(records, f)
            is_computing = False  # toggle
        # toggle from not recording to recording
        elif is_computing == False:
            records = {}  # reset the records
            start_time = time()  # reset the time
            is_computing = True  # toggle

video.release()
cv2.destroyAllWindows()
