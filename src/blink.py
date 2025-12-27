"""
Blink rate estimation using Eye Aspect Ratio (EAR).
"""

import numpy as np
from collections import deque


class BlinkRateEstimator:
    def __init__(self, ear_thresh=0.21, window_sec=10):
        self.ear_thresh = ear_thresh
        self.window_sec = window_sec
        self.blinks = deque()
        self.eye_closed = False

    def compute_ear(self, eye):
        A = np.linalg.norm(eye[1] - eye[5])
        B = np.linalg.norm(eye[2] - eye[4])
        C = np.linalg.norm(eye[0] - eye[3])
        return (A + B) / (2.0 * C + 1e-6)

    def update(self, landmarks, ts):
        left_eye = landmarks[[33, 160, 158, 133, 153, 144]]
        right_eye = landmarks[[362, 385, 387, 263, 373, 380]]

        ear = (
            self.compute_ear(left_eye) +
            self.compute_ear(right_eye)
        ) / 2.0

        if ear < self.ear_thresh and not self.eye_closed:
            self.blinks.append(ts)
            self.eye_closed = True
        elif ear >= self.ear_thresh:
            self.eye_closed = False

        while self.blinks and ts - self.blinks[0] > self.window_sec:
            self.blinks.popleft()

        return ear

    def blink_rate(self):
        return len(self.blinks) / self.window_sec * 60.0


"""
Blink rate estimation using eye aspect ratio (EAR).

Higher blink frequency often correlates with stress,
fatigue, or cognitive load.
"""

"""
import numpy as np
from collections import deque
import time

class BlinkRateEstimator:
    def __init__(self, ear_thresh=0.21, window_sec=10):
        self.ear_thresh = ear_thresh
        self.blinks = deque()
        self.window_sec = window_sec

    def compute_ear(self, eye):
        # eye: array of 6 landmarks
        A = np.linalg.norm(eye[1] - eye[5])
        B = np.linalg.norm(eye[2] - eye[4])
        C = np.linalg.norm(eye[0] - eye[3])
        return (A + B) / (2.0 * C + 1e-6)

    def update(self, landmarks, ts):
        # MediaPipe eye landmark indices
        left_eye = landmarks[[33, 160, 158, 133, 153, 144]]
        right_eye = landmarks[[362, 385, 387, 263, 373, 380]]

        ear = (self.compute_ear(left_eye) + self.compute_ear(right_eye)) / 2

        if ear < self.ear_thresh:
            self.blinks.append(ts)

        # Remove old blinks
        while self.blinks and ts - self.blinks[0] > self.window_sec:
            self.blinks.popleft()

        return ear

    def blink_rate(self):
        return len(self.blinks) / self.window_sec * 60  # blinks/min
"""
