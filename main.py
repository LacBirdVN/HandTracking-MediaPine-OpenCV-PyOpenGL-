import sys
from PyQt5.QtWidgets import QApplication

from Tracker import Tracker
from ui import MainUI


if __name__ == "__main__":
    app = QApplication(sys.argv)

    tracker = Tracker()
    window = MainUI(tracker)

    window.setWindowTitle("Hand Tracking 2D + 3D")
    window.show()

    sys.exit(app.exec_())