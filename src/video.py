"""
Video input abstraction.

This module isolates all video capture logic so that the rest of the
pipeline remains agnostic to the video source (webcam, video file, stream).

Keeping this separate makes it easy to swap in prerecorded datasets
(e.g., UBFC-Phys) or different camera backends.
"""

import cv2
import time

"""
Video input abstraction.

Handles frame capture and timestamping.
Fails loudly if camera cannot be opened (important for demos).
"""


class VideoStream:
    def __init__(self, src=0, width=640, height=480):
        self.cap = cv2.VideoCapture(src)
        if not self.cap.isOpened():
            raise RuntimeError(f"Unable to open video source {src}")

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    def read(self):
        ret, frame = self.cap.read()
        if not ret:
            return None, None
        return frame, time.time()

    def release(self):
        self.cap.release()


class VideoStream__:
    """
    Lightweight wrapper around OpenCV VideoCapture.

    Responsibilities:
    - Frame acquisition
    - Timestamping for synchronization with MediaPipe Tasks API
    """

    def __init__(self, src=0, width=640, height=480):
        """
        Args:
            src (int or str): Camera index or video file path
            width (int): Desired capture width
            height (int): Desired capture height
        """
        self.cap = cv2.VideoCapture(src)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    def read(self):
        """
        Reads a single frame and returns it with a timestamp.

        Returns:
            frame (np.ndarray): BGR image
            timestamp (float): Wall-clock time in seconds
        """
        ret, frame = self.cap.read()
        if not ret:
            return None, None

        # Timestamp is required for MediaPipe VIDEO running mode
        return frame, time.time()

    def release(self):
        """Release camera resources."""
        self.cap.release()

