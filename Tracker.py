from handtracking import HandTracking


class Tracker:
    def __init__(self):
        self.tracker = HandTracking()
        self.frame_count = 0

    def process(self, frame_rgb):
        self.tracker.detect(frame_rgb)
        result = self.tracker.get_result()

        if result and result.hand_landmarks:
            self.frame_count += 1

            for hand_landmarks in result.hand_landmarks:
                # In mỗi 5 frame cho đỡ spam
                if self.frame_count % 5 == 0:
                    self.print_landmarks(hand_landmarks)

        return result

    def print_landmarks(self, hand_landmarks):
        print(f"\n==== Frame {self.frame_count} ====")
        for i, lm in enumerate(hand_landmarks):
            print(f"Point {i:02d}: norm=({lm.x:.3f},{lm.y:.3f},{lm.z:.3f})")

    def close(self):
        self.tracker.close()