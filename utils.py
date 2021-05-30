import cv2
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin


class RGB2Gray2ShapeTransformer(BaseEstimator, TransformerMixin):
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
        return np.array([cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) for img in X]).reshape(
            X.shape[0], -1
        )
