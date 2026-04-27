from collections import Counter


class SmartBarrier:
    """
    Chooses best barrier based on digit distribution
    """

    def __init__(self):
        pass

    def analyze_digits(self, digits):
        freq = Counter(digits)

        # normalize missing digits
        for i in range(10):
            if i not in freq:
                freq[i] = 0

        return freq

    def get_barrier(self, digits, signal):
        freq = self.analyze_digits(digits)

        # sort digits by frequency
        sorted_digits = sorted(freq.items(), key=lambda x: x[1])

        least_common = [d for d, _ in sorted_digits[:3]]
        most_common = [d for d, _ in sorted_digits[-3:]]

        # --------------------------
        # OVER LOGIC
        # --------------------------
        if signal == "OVER":
            # choose a lower barrier near weak digits
            barrier = min(least_common)

            # clamp to safe range
            return min(barrier, 6)

        # --------------------------
        # UNDER LOGIC
        # --------------------------
        if signal == "UNDER":
            # choose higher barrier near weak digits
            barrier = max(least_common)

            return max(barrier, 3)

        return 5  # fallback