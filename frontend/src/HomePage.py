from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
import sys, cv2, qimage2ndarray
import ffmpeg

class VideoConferencingHomePage(QLabel):
    def __init__(self):
        super().__init__()

        self.title = QLabel("<font color=#fc1803 size=40>Video Conferencing App</font>", alignment=Qt.AlignHCenter)
        self.show_opencv_video_button = QPushButton("Show Video from OpenCV")
        self.join_meeting_button = QPushButton("Join Meeting")
        self.create_meeting_button = QPushButton("Create Meeting")
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.show_opencv_video_button)
        self.layout.addWidget(self.join_meeting_button)
        self.layout.addWidget(self.create_meeting_button)

        self.show_opencv_video_button.clicked.connect(self.show_opencv_video_action)
        self.join_meeting_button.clicked.connect(self.join_meeting_action)
        self.create_meeting_button.clicked.connect(self.create_meeting_action)

    Slot()
    def join_meeting_action(self):
        self.join_meeting_button.setText("Join Button Clicked")
        
    Slot()
    def create_meeting_action(self):
        self.create_meeting_button.setText("Create Button Clicked")


# OPEN CV Implementation
    Slot()
    def show_opencv_video_action(self):
        self.show_opencv_video_button.setText("Video needs to be shown")
        self.video_size = QSize(640, 480, alignment = Qt.AlignCenter)
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

        # Setting up process to send frame to a server
        video_format = "h264"
        server_url = "http://127.0.0.1:8080" # Server link
        self.streaming_process = (
            ffmpeg
            .input('pipe:', format='rawvideo',codec="rawvideo", pix_fmt='bgr24', s='{}x{}'.format(self.video_size.width(), self.video_size.height()))
            .output(
                server_url + '/stream',
                #codec = "copy", # use same codecs of the original video
                listen=1, # enables HTTP server
                pix_fmt="yuv420p",
                preset="ultrafast",
                f=video_format
            )
            .overwrite_output()
            .run_async(pipe_stdin=True)
        )

        self.timer = QTimer()
        self.timer.timeout.connect(self.display_video_stream)
        self.timer.start(30)

    def display_video_stream(self):
    #     """Read frame from camera and repaint QLabel widget.
    # """
    #     ret, frame = self.capture.read()
    #     if ret:
    #         frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    #         frame = cv2.flip(frame, 1)
    #         image = qimage2ndarray.array2qimage(frame)
    #         self.image_label.setPixmap(QPixmap.fromImage(image))

    #         #To send opencv stream via ffmpeg to server
    #         streaming_process = self.send_video_ffmpeg()
    #         streaming_process.stdin.write(frame.tobytes())
    #         streaming_process.stdin.close()
    #         streaming_process.wait()
    #         self.capture.release()

        ret, frame = self.capture.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.flip(frame, 1)
            image = qimage2ndarray.array2qimage(frame)
            self.image_label.setPixmap(QPixmap.fromImage(image))
            self.streaming_process.stdin.write(frame.tobytes())
        else:
            self.streaming_process.stdin.close()
            self.streaming_process.wait()
            self.capture.release()

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
