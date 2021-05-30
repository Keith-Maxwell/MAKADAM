import gc
import os

import cv2
import h5py
import numpy as np
from tqdm import tqdm

RESOLUTION = (1280, 720)
tl_corner = (1078, 574)  # top left corner
br_corner = (1195, 676)  # bottom right corner

data = []
labels = []

for position in tqdm(range(1, 13)):
    n = 1
    for file in os.listdir(os.path.join("img", "ML_dataset", str(position))):
        # iterates over every file and checks if it's a video
        if file.endswith(".mp4"):
            # Open the video file with openCV
            cap = cv2.VideoCapture(f"img\\ML_dataset\\{position}\\{file}")
            cap.set(3, RESOLUTION[0])
            cap.set(4, RESOLUTION[1])
            while True:
                # read each frame
                ret, img = cap.read()

                if not ret:  # checks if the read was successful
                    n += 1
                    break

                else:
                    # crop the image to focus on the position
                    img = img[tl_corner[1] : br_corner[1], tl_corner[0] : br_corner[0]]
                    # cv2.imshow("img", img)

                    # save one image out of 5 to not overload memory
                    if n % 5 == 0:
                        cv2.imwrite(
                            f"img\\ML_dataset\\{position}\\{position}_" + str(n) + ".jpg", img
                        )
                        # append the data and label to the dataset list
                        data.append(img)
                        labels.append(position)

                    n += 1  # allows the naming of each file differently

                    if cv2.waitKey(1) == ord("q"):
                        break

            cap.release()  # close the video file
            cv2.destroyAllWindows()  # close all windows
            gc.collect()  # try to clean the memory, to avoid memory issues


h5_file = h5py.File(os.path.join("img", "ML_dataset", "dataset.h5"), "w")
h5_file.create_dataset("dataset", data=np.array(data))
h5_file.create_dataset("labels", data=np.array(labels))
h5_file.close()
