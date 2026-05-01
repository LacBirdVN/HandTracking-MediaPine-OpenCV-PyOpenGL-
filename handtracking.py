import mediapipe as mp
import time
import math
from config import MODEL_PATH, NUM_HANDS, SMOOTHING, THRESHOLD

# Khởi tạo MediaPipe
BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

def distance(a, b):
    return math.sqrt(
        (a.x - b.x) ** 2 +
        (a.y - b.y) ** 2 +
        (a.z - b.z) ** 2
    )


class HandTracking:
    def __init__(self):
        self.result = None
        self.prev_landmarks = None
        
        # Tạo Model 
        options = HandLandmarkerOptions(
            base_options=BaseOptions(model_asset_path=MODEL_PATH),
            running_mode=VisionRunningMode.LIVE_STREAM,
            result_callback=self.callback,
            num_hands=NUM_HANDS
        )

        # Khởi đông Model 
        self.landmarker = HandLandmarker.create_from_options(options)

    # Nhận kết quả từ Mediapine và xử lý smoothing
    def callback(self, result, output_image, timestamp_ms):
        if result and result.hand_landmarks:
            if self.prev_landmarks is None:
                self.prev_landmarks = result.hand_landmarks
            else:
                for i in range(len(result.hand_landmarks)):
                    for j in range(len(result.hand_landmarks[i])):
                        prev = self.prev_landmarks[i][j]
                        curr = result.hand_landmarks[i][j]

                        dist = distance(prev, curr)

                        if dist < THRESHOLD:
                            # Di chuyển nhỏ -> bỏ qua
                            curr.x, curr.y, curr.z = prev.x, prev.y, prev.z
                        else:
                            # Di chuyển lớn → smoothing
                            curr.x = SMOOTHING * prev.x + (1 - SMOOTHING) * curr.x
                            curr.y = SMOOTHING * prev.y + (1 - SMOOTHING) * curr.y
                            curr.z = SMOOTHING * prev.z + (1 - SMOOTHING) * curr.z

                self.prev_landmarks = result.hand_landmarks

        self.result = result

    def detect(self, frame_rgb):
 
        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=frame_rgb
        )
        timestamp = int(time.time() * 1000)
        self.landmarker.detect_async(mp_image, timestamp)

    def get_result(self):
        return self.result

    def close(self):
        self.landmarker.close()