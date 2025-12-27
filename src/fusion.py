"""
Signal fusion logic for computing the final Stress Index.

This module defines explicit, interpretable logic that combines
physiological and behavioral signals into a single [0, 100] score.

No learning is performed here by design.
"""


"""
Signal fusion logic for Stress Index computation.
"""

import numpy as np


class StressFusion:
    def __init__(self, alpha=0.5):
        self.alpha = alpha
        self.stress = 0.0

    def normalize(self, x, min_val, max_val):
        return np.clip(
            (x - min_val) / (max_val - min_val + 1e-6),
            0.0,
            1.0
        )

    def update(self, hr_var, motion, blink_rate=None):
        # Guard against no-signal frames
        if hr_var == 0 and motion == 0 and blink_rate is None:
            return int(self.stress * 100)

        hr_score = self.normalize(hr_var, 0.01, 0.1)
        motion_score = self.normalize(motion, 0.0002, 0.005)

        blink_score = 0.0
        if blink_rate is not None:
            blink_score = self.normalize(blink_rate, 10.0, 40.0)

        raw = (
            0.3 * hr_score +
            0.4 * motion_score +
            0.3 * blink_score
        )

        self.stress = (
            self.alpha * raw +
            (1.0 - self.alpha) * self.stress
        )

        return int(self.stress * 100)



class StressFusion__:
    """
    Fuses normalized signals using weighted averaging and temporal smoothing.
    """

    def __init__(self, alpha=0.5):
        """
        Args:
            alpha (float): Exponential smoothing factor.
                           Higher = faster response, lower stability.
        """
        self.alpha = alpha
        self.stress = 0.0

    def normalize(self, x, min_val, max_val):
        """
        Normalize a raw signal into [0, 1].

        Bounds are empirically chosen and can be tuned per deployment.
        """
        return np.clip(
            (x - min_val) / (max_val - min_val + 1e-6),
            0.0,
            1.0
        )

    def update(self, hr_var, motion, blink_rate=None):
        """
        Update stress estimate using latest signals.

        Args:
            hr_var (float): rPPG-derived variability
            motion (float): Head motion energy
            blink_rate (float | None): Blinks per minute

        Returns:
            int: Stress Index in range [0, 100]
        """

        # Normalize physiological signal
        hr_score = self.normalize(hr_var, 0.01, 0.1)

        # Normalize behavioral motion signal
        motion_score = self.normalize(motion, 0.0002, 0.005)

        # Normalize blink rate if available
        blink_score = 0.0
        if blink_rate is not None:
            blink_score = self.normalize(blink_rate, 10.0, 40.0)

        # Weighted fusion (behavior emphasized for live demo)
        raw = (
            0.3 * hr_score +
            0.4 * motion_score +
            0.3 * blink_score
        )

        # Temporal smoothing to reduce jitter
        self.stress = (
            self.alpha * raw +
            (1.0 - self.alpha) * self.stress
        )

        return int(self.stress * 100)

