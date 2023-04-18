from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtMultimedia import *
from PySide6.QtMultimediaWidgets import QVideoWidget
import sys, cv2, qimage2ndarray
import numpy, subprocess, threading

# Define the dimensions of the video frames
FRAME_WIDTH = 320
FRAME_HEIGHT = 240

# Define the IP address and port number of the server
SERVER_IP = 'localhost'
SERVER_PORT = 1235
BROADCAST_PORT = 4000

# Video Codec
VIDEO_CODEC = 'h264'

class VideoConferencingHomePage(QLabel):
    def __init__(self):
        super().__init__()

        self.title = QLabel("<font color=#fc1803 size=40>Video Conferencing App</font>", alignment=Qt.AlignHCenter)
        self.receive_video_button = QPushButton("Receive Video from Host")

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.receive_video_button)


        self.receive_video_button.clicked.connect(self.receive_video_action)


        # self.broadcast_command = ['ffmpeg', 
        #             '-f', 'rawvideo', 
        #             '-pix_fmt', 'bgr24',
        #             '-video_size', f'{FRAME_WIDTH}x{FRAME_HEIGHT}', 
        #             '-i', f'udp://{SERVER_IP}:{SERVER_PORT}/stream',
        #             '-c:v', 'libx264',
        #             '-preset', 'ultrafast',
        #             '-tune', 'zerolatency',
        #             '-f', 'h264',
        #             f'udp://{SERVER_IP}:{BROADCAST_PORT}/stream'
        # ]
        # self.stream = subprocess.Popen(broadcast_command, stderr=subprocess.PIPE)

        self.recv_command = ['ffmpeg',
                   '-i', f'udp://{SERVER_IP}:{SERVER_PORT}/stream',
                #    '-pix_fmt', 'bgr24',
                   '-bufsize', '10M',
                   '-c:v', 'libx264',
                    '-preset', 'ultrafast',
                    '-tune', 'zerolatency',
                    '-f', 'h264',
                   f'udp://{SERVER_IP}:{BROADCAST_PORT}/stream']
        # self.recv_process = subprocess.Popen(recv_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # OpenCV Implementation
    Slot()
    def receive_video_action(self):
        self.video_size = QSize(320, 240, alignment = Qt.AlignCenter)
        self.setup_ui()
        self.start_stream_thread()
    
    def setup_ui(self):
        """Initialize widgets.
        """
        self.stream_label = QLabel()
        self.stream_label.setFixedSize(self.video_size)


        self.quit_button = QPushButton("Quit")
        self.quit_button.clicked.connect(self.close)
        
        ## Clear current layout
        for i in reversed(range(self.layout.count())): 
            self.layout.itemAt(i).widget().deleteLater()


        self.layout.addWidget(self.stream_label)
        self.layout.addWidget(self.quit_button)

        self.setLayout(self.layout)



    def send_video_frame(self):
        # print("Sending Frame to Server")

        # Write the frame to the network stream
        print("Forwarding Video")
        subprocess.run(self.recv_command)




    def start_stream_thread(self):
        # thread_display_stream_frame = threading.Thread(target=self.display_stream_frame, daemon=True)
        # thread_display_stream_frame.start()
        thread_send_video_frame = threading.Thread(target=self.send_video_frame)
        thread_send_video_frame.start()

    def display_stream_frame(self):
        print("Reading Frame from Server")

        limit = 0

        try:
            while(True):
                # Read a frame from the network stream
                frame_data = self.recv_process.stdout.read(FRAME_WIDTH * FRAME_HEIGHT * 3)
                
                if len(frame_data) != FRAME_WIDTH * FRAME_HEIGHT * 3:
                    print("Incorrect Frame Data : " + frame_data.decode("utf-8"))
                    return

                if frame_data:
                    print("Received a frame from server")
                    # Convert the frame data to a numpy array
                    frame = numpy.frombuffer(frame_data, dtype=numpy.uint8)
                    frame = frame.reshape((FRAME_HEIGHT, FRAME_WIDTH, 3))

                    # Convert the frame from BGR to RGB
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    frame = cv2.flip(frame, 1)

                    # Create a QImage from the frame data
                    # image = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
                    image = qimage2ndarray.array2qimage(frame)
                    
                    # Create a QPixmap from the QImage
                    pixmap = QPixmap.fromImage(image)

                    # Set the pixmap in the stream frame label
                    self.stream_label.setPixmap(pixmap)
                else:
                    limit += 1

                if(limit >= 5):
                    print("Not receiving any frame from the server. Closing read operation.")
                    self.recv_process.stdin.close()
                    self.recv_process.wait()
                    return
        except:
            self.recv_process.stdin.close()
            self.recv_process.wait()

if __name__ == "__main__":
    app = QApplication([])

    homepage = VideoConferencingHomePage()
    homepage.resize(800, 600)
    homepage.setAutoFillBackground(True)
    palette = QPalette()
    gradient = QLinearGradient(0, 0, 0, 400)
    gradient.setColorAt(0.0, QColor('darkBlue'))
    gradient.setColorAt(1.0, QColor('darkMagenta'))
    palette.setBrush(QPalette.Window, QBrush(gradient))
    homepage.setPalette(palette)
    homepage.show()

    sys.exit(app.exec())
