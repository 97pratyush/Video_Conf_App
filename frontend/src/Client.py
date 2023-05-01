from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtMultimedia import *
from PySide6.QtMultimediaWidgets import *
from PySide6.QtNetwork import *
import sys, cv2, qimage2ndarray, numpy, subprocess, threading, pyaudio

# Define the dimensions of the video frames
FRAME_WIDTH = 320
FRAME_HEIGHT = 240

# Define the IP address and port number of the server
SERVER_IP = '10.0.0.248'
SERVER_PORT = 4000

# Video Codec
VIDEO_CODEC = 'flv'

RTMP_URL = 'rtmp://10.0.0.248/live/test_test'

class VideoConferencingHomePage(QWidget):
    def __init__(self):
        super().__init__()

        self.send_command = ['ffmpeg', 
                    # '-f', 'rawvideo', 
                    '-f', 'v4l2',
                    '-s', f'{FRAME_WIDTH}x{FRAME_HEIGHT}', 
                    '-i', '/dev/video0',
                    '-f', 'alsa',
                    '-i', 'default',
                    '-c:v', 'libx264',
                    '-preset', 'veryfast',
                    '-tune', 'zerolatency',
                    '-b:v', '100k',
                    '-c:a', 'aac', 
                    '-ar', '44100',
                    '-ac', '1',
                    '-af', 'afftdn',
                    '-maxrate', '3000k',
                    '-bufsize', '300k',
                    '-f', f'{VIDEO_CODEC}',
                    f'{RTMP_URL}'
        ]

        self.stream = subprocess.Popen(self.send_command, stdin=subprocess.PIPE, stderr=subprocess.PIPE)

        # self.recv_command = ['ffmpeg',
        #            '-i', f'{RTMP_URL}',
        #            '-f', 'rawvideo',
        #         #    '-fflags', 'nobuffer',
        #            '-pix_fmt', 'bgr24',
        #         #    '-bufsize', '100k',
        #            '-'
        # ]

        self.recv_command = [
                    'ffmpeg',
                    '-vn',
                    '-i', f'{RTMP_URL}',
                    '-f', 'adts',
                    '-'
                ]

        # self.stream = None
        self.recv_process = None
        self.close_called = False
        self.receive_process_invoked = False
        self.capture = None
        self.audio_stream = None

        self.title = QLabel("<font color=#fc1803 size=40>Video Conferencing App</font>", alignment=Qt.AlignHCenter)
        self.send_video_to_server_button = QPushButton("Send Video to Server")
        self.receive_video_from_server_button = QPushButton("Receive Video from Server")
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.send_video_to_server_button)
        self.layout.addWidget(self.receive_video_from_server_button)

        self.send_video_to_server_button.clicked.connect(self.send_video_to_server)
        self.receive_video_from_server_button.clicked.connect(self.start_stream_thread)

    def closeEvent(self, event):
        print("Quitting Application")

        self.close_called = True

        if self.stream != None:
            self.stream.terminate() 
            self.stream.wait()

        if self.capture != None:
            self.capture.release()

        if self.receive_process_invoked == True and self.recv_process != None:
            self.recv_process.terminate()
            self.recv_process.wait()

        if self.audio_stream != None:
            self.audio_stream.stop_stream()
            self.audio_stream.close()
            self.p.terminate()

        super().closeEvent(event)

    # OpenCV Implementation
    Slot()
    def send_video_to_server(self):
        self.setup_ui()
        # thread_opencv = threading.Thread(target=self.display_video_frame_using_opencv, args=(self.image_label, RTMP_URL))
        # thread_opencv.start()
    
    def setup_ui(self):
        """Initialize widgets.
        """
        self.video_size = QSize(FRAME_WIDTH, FRAME_HEIGHT, alignment = Qt.AlignCenter)
        self.image_label = QLabel()
        self.image_label.setFixedSize(self.video_size)

        self.stream_label = QLabel()
        self.stream_label.setFixedSize(self.video_size)

        self.second_label = QLabel()
        self.second_label.setFixedSize(self.video_size)

        self.third_label = QLabel()
        self.third_label.setFixedSize(self.video_size)

        self.display_frame_button = QPushButton("Display from Server")
        self.display_frame_button.clicked.connect(self.start_stream_thread)

        self.quit_button = QPushButton("Quit")
        self.quit_button.clicked.connect(self.close)
        
        ## Clear current layout
        for i in reversed(range(self.layout.count())): 
            self.layout.itemAt(i).widget().deleteLater()

        # self.layout.addWidget(self.image_label)
        self.layout.addWidget(self.stream_label)
        self.layout.addWidget(self.display_frame_button)
        self.layout.addWidget(self.quit_button)

        self.setLayout(self.layout)
        

    def display_video_frame_using_opencv(self, label : QLabel, url : str):
        opencv_video_stream = cv2.VideoCapture(url, cv2.CAP_FFMPEG)

        try:
            while True:
                try:
                    # Read the input live stream
                    ret, frame = opencv_video_stream.read()
                    # print("Return type : ", type(ret), ". Return value : ", ret)
                    # print("Frame type : ", type(frame), ". Frane value : ", frame)
                    if self.close_called == True:
                        print("Video Capture stopped : ", url)
                        break

                    if ret:
                        frame = cv2.resize(frame, (FRAME_WIDTH, FRAME_HEIGHT))

                        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        frame = cv2.flip(frame, 1)

                        # Create a QImage from the frame data
                        # image = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
                        image = qimage2ndarray.array2qimage(frame)
                        
                        # Create a QPixmap from the QImage
                        pixmap = QPixmap.fromImage(image)

                        # Set the pixmap in the stream frame label
                        label.setPixmap(pixmap)
                    else:
                        print("No frame received in opencv stream")

                except Exception as e:
                    print("Failed : ", e)
                
        except Exception as e:
            print("Exception in displaying : ", e)
        finally:
            opencv_video_stream.release()

    Slot()
    def start_stream_thread(self):
        self.setup_ui()
        # self.layout.addWidget(self.stream_label)
        # self.layout.addWidget(self.second_label)
        # self.layout.addWidget(self.third_label)

        thread_opencv_second = threading.Thread(target=self.display_video_frame_using_opencv, args=(self.stream_label, RTMP_URL))
        thread_opencv_second.start()
        
        # self.receive_process_invoked = True

        # self.recv_process = subprocess.Popen(self.recv_command, stdout=subprocess.PIPE)

        # thread_stream_audio = threading.Thread(target=self.stream_audio_play)
        # thread_stream_audio.start()

    def stream_audio_play(self):
        print("Reading audio from server")

        self.p = pyaudio.PyAudio()
        self.audio_stream = self.p.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=44100,
            output=True
        )

        data = self.recv_process.stdout.read(FRAME_HEIGHT * FRAME_WIDTH * 2)
        while(len(data)>0):
            try:
                # Play audio from stdout
                if self.close_called == True:
                    break
                self.audio_stream.write(data)
                data = self.recv_process.stdout.read(FRAME_HEIGHT * FRAME_WIDTH * 2)
                # self.recv_process.stdout.flush()
            except Exception as e:
                print("Exception occured during audio receive : ", e)
            finally:
                if self.audio_stream != None:
                    self.audio_stream.stop_stream()
                    self.audio_stream.close()
                if self.p != None:
                    self.p.terminate()
                self.recv_process.stdout.flush()
                self.recv_process.terminate()
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



#Read a frame from the network stream
# audio_video_data = self.recv_process.stdout.read(FRAME_WIDTH * FRAME_HEIGHT * 2)
# print("Frame Data : " + audio_video_data.decode("utf-8"))

# if len(audio_video_data) != FRAME_WIDTH * FRAME_HEIGHT * 3:
#     print("Incorrect data received from server")

# if 1 == 1:
    # print("Received a frame from server")
    # Convert the frame data to a numpy array
    # frame = numpy.frombuffer(audio_video_data, dtype=numpy.uint8)
    # frame = frame.reshape((FRAME_HEIGHT, FRAME_WIDTH, 3))

    # # Convert the frame from BGR to RGB
    # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # frame = cv2.flip(frame, 1)

    # # Create a QImage from the frame data
    # # image = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
    # image = qimage2ndarray.array2qimage(frame)
    
    # # Create a QPixmap from the QImage
    # pixmap = QPixmap.fromImage(image)

    # # Set the pixmap in the stream frame label
    # self.stream_label.setPixmap(pixmap)

    # self.recv_process.stdout.flush()