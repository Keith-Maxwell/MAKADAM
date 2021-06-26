import cv2
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin


class ShapeTransformer(BaseEstimator, TransformerMixin):
    """
    Convert an array of RGB images to grayscale and reshape the array to (n_samples, width * height)
    """

    def __init__(self):
        pass

    def fit(self, X, y=None):
        """returns itself"""
        return self

    def transform(self, X, y=None):
        """perform the transformation and return an array"""
        return X.reshape(X.shape[0], -1)


def image_preprocessing(image, tl_corner=None, br_corner=None):
    """Crop an image and apply a black and white mask

    Parameters
    ----------
    image : numpy array
        Image with 3 channels (BGR).
    tl_corner : Tuple
        Coordinates (x,y) of the top left corner of the rectangle to crop
    br_corner : Tuple
        Coordinates (x,y) of the bottom right corner of the rectangle to crop

    Returns
    -------
    numpy array
        binary image ready to be read by OCR
    """
    # Crop with slicing
    if tl_corner and br_corner:
        image = image[tl_corner[1] : br_corner[1], tl_corner[0] : br_corner[0]]

    # Convert to HSV channels
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # define lower and upper bounds of the filter
    lower = np.array([0, 0, 210])
    upper = np.array([255, 255, 255])
    # return the mask
    return cv2.inRange(hsv, lower, upper)


def apply_overlay(image, OCR_results):
    """Apply an overlay on the image with bounding boxes
    and the text recognized, along with the confidence level

    Parameters
    ----------
    image : numpy array
        image on which the overlay will be aplied (for better results, use BGR image)
    OCR_results : list[list]
        Detailed results given by the easyocr.Reader.readtext() function

    Returns
    -------
    numpy array
        image with the overlay of boxes and text recognized
    """
    image_with_overlay = image.copy()
    # loop over the results
    for (bbox, text, prob) in OCR_results:
        # display the OCR'd text and associated probability
        # print("[INFO] {:.4f}: {}".format(prob, text))

        # unpack the bounding box
        (tl, tr, br, bl) = bbox
        tl = (int(tl[0]), int(tl[1]))
        tr = (int(tr[0]), int(tr[1]))
        br = (int(br[0]), int(br[1]))
        bl = (int(bl[0]), int(bl[1]))

        # draw the box surrounding the text along
        # with the OCR'd text itself and the probability
        cv2.rectangle(image_with_overlay, tl, br, (0, 255, 0), 2)
        cv2.putText(
            image_with_overlay,
            text + " " + str(round(prob, 2)),
            (br[0] + 5, br[1]),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 0, 255),
            2,
        )
    return image_with_overlay


def returnCameraIndexes():
    """returns a list of availlable OpenCV camera indexes

    Returns
    -------
    list
        available camera indexes
    """
    # checks the first 10 indexes.
    index = 0
    arr = []
    i = 10
    while i > 0:
        cap = cv2.VideoCapture(index)
        if cap.read()[0]:
            arr.append(index)
            cap.release()
        index += 1
        i -= 1
    return arr


if __name__ == "__main__":
    pass
