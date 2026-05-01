import cv2

from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap

from draw import draw_hand
from draw3D import Hand3DWidget
from config import CAMERA_ID


class MainUI(QWidget):
    def __init__(self, tracker):
        super().__init__()

        self.tracker = tracker

        # UI
        self.viewer3D = Hand3DWidget()
        self.viewer3D.setMinimumSize(600, 600)

        self.viewer2D = QLabel()
        self.viewer2D.setMinimumSize(600, 600)

        layout = QHBoxLayout()
        layout.addWidget(self.viewer2D)
        layout.addWidget(self.viewer3D)
        self.setLayout(layout)

        # Camera
        self.cap = cv2.VideoCapture(CAMERA_ID)

        # Timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(16)

    def update_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Tracking
        result = self.tracker.process(frame_rgb)

        if result and result.hand_landmarks:
            for hand_landmarks in result.hand_landmarks:
                draw_hand(frame, hand_landmarks)
                self.viewer3D.set_hand(hand_landmarks)

        # Convert sang Qt image
        h, w, ch = frame.shape
        bytes_per_line = ch * w

        qt_image = QImage(
            frame.data,
            w,
            h,
            bytes_per_line,
            QImage.Format_BGR888
        )

        self.viewer2D.setPixmap(QPixmap.fromImage(qt_image))

    def closeEvent(self, event):
        self.cap.release()
        self.tracker.close()
        event.accept()