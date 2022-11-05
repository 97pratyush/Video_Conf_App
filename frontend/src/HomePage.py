from ctypes import alignment
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
import sys, cv2, qimage2ndarray
from ffmpeg_streaming import Formats, Bitrate, Representation, Size, input

class VideoConferencingHomePage(QLabel):
    def __init__(self):
        super().__init__()

        self.title = QLabel("<font color=#fc1803 size=40>Video Conferencing App</font>", alignment=Qt.AlignHCenter)
        self.show_video_button = QPushButton("Show your Video")
        self.show_local_video_button = QPushButton("Show Local Video")
        self.join_meeting_button = QPushButton("Join Meeting")
        self.create_meeting_button = QPushButton("Create Meeting")
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.show_video_button)
        self.layout.addWidget(self.show_local_video_button)
        self.layout.addWidget(self.join_meeting_button)
        self.layout.addWidget(self.create_meeting_button)

        self.show_video_button.clicked.connect(self.show_video_action)
        self.show_local_video_button.clicked.connect(self.show_local_video_action)
        self.join_meeting_button.clicked.connect(self.join_meeting_action)
        self.create_meeting_button.clicked.connect(self.create_meeting_action)

    Slot()
    def show_local_video_action(self):
        # input = ffmpeg.input('')
        # audio = input.audio.filter("aecho", 0.8, 0.9, 1000, 0.3)
        # video = input.video.hflip()
        # out = ffmpeg.output(audio, video, 'out.mp4')
        video = input("0:0", capture=True)

        dash = video.dash(Formats.h264())
        _480p  = Representation(Size(854, 480), Bitrate(750 * 1024, 192 * 1024))
        _720p  = Representation(Size(1280, 720), Bitrate(2048 * 1024, 320 * 1024))
        dash.representations(_480p, _720p)
        dash.output('../output/dash.mpd')

    Slot()
    def join_meeting_action(self):
        self.join_meeting_button.setText("Join Button Clicked")
        
    Slot()
    def create_meeting_action(self):
        self.create_meeting_button.setText("Create Button Clicked")

    Slot()
    def show_video_action(self):
        self.show_video_button.setText("Video needs to be shown")
        self.video_size = QSize(320, 240, alignment = Qt.AlignCenter)
        self.setup_ui()
        self.setup_camera()
    
    def setup_ui(self):
        """Initialize widgets.
        """
        self.image_label = QLabel()
        self.image_label.setFixedSize(self.video_size)

        self.quit_button = QPushButton("Quit")
        self.quit_button.clicked.connect(self.close)
        
        ## Clear current layout
        for i in reversed(range(self.layout.count())): 
            self.layout.itemAt(i).widget().deleteLater()

        self.layout.addWidget(self.image_label)
        self.layout.addWidget(self.quit_button)

        self.setLayout(self.layout)

    def setup_camera(self):
        """Initialize camera.
        """
        self.capture = cv2.VideoCapture(0)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.video_size.width())
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.video_size.height())

        self.timer = QTimer()
        self.timer.timeout.connect(self.display_video_stream)
        self.timer.start(30)

    def display_video_stream(self):
        """Read frame from camera and repaint QLabel widget.
    """
        _, frame = self.capture.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.flip(frame, 1)
        image = qimage2ndarray.array2qimage(frame)
        self.image_label.setPixmap(QPixmap.fromImage(image))

if __name__ == "__main__":
    app = QApplication([])

    homepage = VideoConferencingHomePage()
    homepage.resize(800, 600)
    homepage.setAutoFillBackground(True)
    p = QPalette()
    gradient = QLinearGradient(0, 0, 0, 400)
    gradient.setColorAt(0.0, QColor(240, 240, 240))
    gradient.setColorAt(1.0, QColor(240, 160, 160))
    p.setBrush(QPalette.Window, QBrush(gradient))
    homepage.setPalette(p)
    homepage.show()

    sys.exit(app.exec())
