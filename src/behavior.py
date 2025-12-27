"""
Behavioral stress signal derived from facial landmarks.

We intentionally use simple kinematic features (head motion)
instead of complex facial expression analysis to ensure robustness
under real-world conditions (typing, partial occlusion, glasses).
"""

import numpy as np
from collections import deque


"""
Head motion–based behavioral stress signal.
"""

import numpy as np
from collections import deque


class HeadMotionAnalyzer:
    def __init__(self, window=30):
        self.positions = deque(maxlen=window)

    def update(self, landmarks):
        # Nose tip (more stable than index 1)
        nose = landmarks[4]
        self.positions.append(nose[:2])

    def motion_energy(self):
        if len(self.positions) < 5:
            return 0.0

        diffs = np.diff(np.array(self.positions), axis=0)
        return float(np.mean(np.linalg.norm(diffs, axis=1)))


class HeadMotionAnalyzer__:
    """
    Estimates head motion energy using landmark displacement.

    Higher short-term motion often correlates with agitation,
    cognitive load, or physical exertion.
    """

    def __init__(self, window=30):
        """
        Args:
            window (int): Number of frames to retain for motion analysis
        """
        self.positions = deque(maxlen=window)

    def update(self, landmarks):
        """
        Update motion buffer using a stable landmark (nose tip).

        Args:
            landmarks (np.ndarray): Face landmarks array
        """
        nose = landmarks[1]  # Chosen for stability across expressions
        self.positions.append(nose[:2])

    def motion_energy(self):
        """
        Compute average frame-to-frame displacement.

        Returns:
            float: Scalar motion energy
        """
        if len(self.positions) < 5:
            return 0.0

        diffs = np.diff(np.array(self.positions), axis=0)
        return np.mean(np.linalg.norm(diffs, axis=1))

