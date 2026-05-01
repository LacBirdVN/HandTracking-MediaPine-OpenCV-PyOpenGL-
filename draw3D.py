import sys
from PyQt5.QtWidgets import QApplication, QOpenGLWidget
from PyQt5.QtCore import QTimer
from OpenGL.GL import *
from OpenGL.GLU import *
import math

HAND_CONNECTIONS = [
    (0,1),(1,2),(2,3),(3,4),
    (0,5),(5,6),(6,7),(7,8),
    (5,9),(9,10),(10,11),(11,12),
    (9,13),(13,14),(14,15),(15,16),
    (13,17),(17,18),(18,19),(19,20),
    (0,17)
]

class Hand3DWidget(QOpenGLWidget):
    def __init__(self):
        super().__init__()
        self.hand_landmarks = None

        self.rot_x = 0
        self.rot_y = 0
        self.last_pos = None

        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(16)  # ~60 FPS

    def set_hand(self, landmarks):
        self.hand_landmarks = landmarks

    def initializeGL(self):
        glEnable(GL_DEPTH_TEST)

    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        # Cài đặt camera
        gluPerspective(45, w / h if h != 0 else 1, 0.1, 50.0)
        glMatrixMode(GL_MODELVIEW)

    def paintGL(self):
        # Xóa frame cũ, thêm frame mới 
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        # Vị trí Camera
        glTranslatef(0, 0, -2.5)

        # Xoay chuột
        glRotatef(self.rot_x, 1, 0, 0)
        glRotatef(self.rot_y, 0, 1, 0)

        # Vẽ x(đỏ), y(xanh lá), z(xanh dương)
        self.draw_axes()

        if not self.hand_landmarks:
            return

        xs = [lm.x for lm in self.hand_landmarks]
        ys = [lm.y for lm in self.hand_landmarks]
        zs = [lm.z * 2 for lm in self.hand_landmarks]

        # Center (Lấy cổ tay làm gốc (0,0,0))
        cx, cy, cz = xs[0], ys[0], zs[0]
        xs = [x - cx for x in xs]
        ys = [y - cy for y in ys]
        zs = [z - cz for z in zs]

        # Đảo trục (do MediaPipe và OpenGL trục ngược nhau)
        ys = [-y for y in ys]
        zs = [-z for z in zs]

        # scale (Tay không bị zoom theo camera)
        def dist(a, b):
            return math.sqrt(
                (a.x - b.x)**2 +
                (a.y - b.y)**2 +
                (a.z - b.z)**2
            )

        hand_size = dist(self.hand_landmarks[0], self.hand_landmarks[9])
        scale = 0.4 / (hand_size + 1e-6)

        xs = [x * scale for x in xs]
        ys = [y * scale for y in ys]
        zs = [z * scale for z in zs]

        # Vẽ điểm 
        glPointSize(8)
        glBegin(GL_POINTS)
        glColor3f(0, 1, 0)
        for x, y, z in zip(xs, ys, zs):
            glVertex3f(x, y, z)
        glEnd()

        # Vẽ đường 
        glLineWidth(2)
        glBegin(GL_LINES)
        glColor3f(1, 0, 0)
        for s, e in HAND_CONNECTIONS:
            glVertex3f(xs[s], ys[s], zs[s])
            glVertex3f(xs[e], ys[e], zs[e])
        glEnd()

    # Điều khiển chuột 
    def mousePressEvent(self, event):
        self.last_pos = event.pos()

    def mouseMoveEvent(self, event):
        if self.last_pos:
            dx = event.x() - self.last_pos.x()
            dy = event.y() - self.last_pos.y()

            self.rot_x += dy
            self.rot_y += dx

            self.last_pos = event.pos()

    def draw_axes(self):
        glLineWidth(3)
        glBegin(GL_LINES)

        # X - đỏ
        glColor3f(1, 0, 0)
        glVertex3f(0, 0, 0)
        glVertex3f(0.5, 0, 0)

        # Y - xanh lá
        glColor3f(0, 1, 0)
        glVertex3f(0, 0, 0)
        glVertex3f(0, 0.5, 0)

        # Z - xanh dương
        glColor3f(0, 0, 1)
        glVertex3f(0, 0, 0)
        glVertex3f(0, 0, 0.5)

        glEnd()