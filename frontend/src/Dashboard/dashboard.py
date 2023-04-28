from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QPushButton,   
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QSize
from style import primary_cta_style, secondary_cta_style
from Dashboard.join_meeting_dialog import JoinMeeting
from Meeting.meeting import MeetingPage

import sys, cv2, qimage2ndarray, numpy, subprocess, threading, time


class Dashboard(QWidget):
    def __init__(self, parent=None):
        super(Dashboard, self).__init__(parent)
        self.welcome_label = QLabel(
            "<font size=40>Welcome, User</font>", alignment=Qt.AlignCenter
        )

        self.create_meeting = QPushButton("Create a meeting")
        self.create_meeting.setStyleSheet(primary_cta_style)
        self.create_meeting.clicked.connect(self.start_meeting)

        self.join_meeting_cta = QPushButton("Join Meeting")
        self.join_meeting_cta.setStyleSheet(secondary_cta_style)
        self.join_meeting_cta.clicked.connect(self.join_meeting)

        self.layout = QVBoxLayout()
        self.widgets = [
            self.welcome_label,
            self.create_meeting,
            self.join_meeting_cta,
        ]
        for self.widget in self.widgets:
            self.layout.addWidget(self.widget)

        self.setLayout(self.layout)

        # Define the dimensions of the video frames
        self.FRAME_WIDTH = 640
        self.FRAME_HEIGHT = 480

        # Define the IP address and port number of the server
        SERVER_IP = '10.0.0.248'
        SERVER_PORT = 4000

        # Video Codec
        VIDEO_CODEC = 'flv'

        self.send_command = ['ffmpeg', 
                    '-f', 'rawvideo', 
                    '-pix_fmt', 'bgr24',
                    '-s', f'{self.FRAME_WIDTH}x{self.FRAME_HEIGHT}', 
                    '-i', '-',
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
                    '-bufsize', '100k',
                    '-f', f'{VIDEO_CODEC}',
                    f'rtmp://{SERVER_IP}/live/stream'
        ]

        self.recv_command = ['ffmpeg',
                   '-i', f'rtmp://{SERVER_IP}/live/test_test',
                   '-f', 'rawvideo',
                #    '-fflags', 'nobuffer',
                   '-pix_fmt', 'bgr24',
                   '-bufsize', '100k',
                   '-'
        ]

        self.video_size = QSize(self.FRAME_WIDTH, self.FRAME_HEIGHT, alignment = Qt.AlignCenter)

    def start_meeting(self):    
        self.meeting_page = MeetingPage()
        self.meeting_page.end_call_button.clicked.connect(self.end_call)
        self.meeting_page.show()

        # Send Video
        self.stream = subprocess.Popen(self.send_command, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        self.thread_send_video_frame = threading.Thread(target=self.setup_camera)
        self.thread_send_video_frame.start()

        # Recieve Video
        thread_display_stream_frame = threading.Thread(target=self.display_stream_frame, daemon=True)
        thread_display_stream_frame.start()

    def setup_camera(self):
        
        self.capture = cv2.VideoCapture(0)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.video_size.width())
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.video_size.height())

        # thread_display_video_frame = threading.Thread(target=self.display_video_frame, args=(self.frame))
        # thread_display_video_frame.start()

        _, frame = self.capture.read()

        # self.timer = QTimer()
        # self.timer.timeout.connect(self.start_capturing)
        # self.timer.start(30)

        while(True):
            _, frame = self.capture.read()
            self.send_video_frame(frame)
            self.display_video_frame(frame)
        
    def send_video_frame(self, frame):
        # print("Sending Frame to Server")

        # Write the frame to the network stream
        self.stream.stdin.write(frame.tobytes())

        # Throw away data to pipe buffer
        self.stream.stdin.flush()
        

    def display_video_frame(self, frame):
        # print("Displaying Local Frame")
        # Convert the frame from BGR to RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.flip(frame, 1)

        # Create a QImage from the frame data
        # image = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
        image = qimage2ndarray.array2qimage(frame)

        # Create a QPixmap from the QImage
        pixmap = QPixmap.fromImage(image)

        # Set the pixmap in the video frame label
        self.meeting_page.labels[0].setPixmap(pixmap)
        self.meeting_page.labels[0].setFixedSize(self.video_size)

    def end_call(self):
        self.close()
        print("Stopping ffmpeg sending command")
        self.stream.terminate()
        self.stream.kill()
        self.stream.wait()

    def display_stream_frame(self):
        print("Reading Frame from Server")

        self.recv_process = subprocess.Popen(self.recv_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        limit = 0

        try:
            while(True):
                # Read a frame from the network stream
                frame_data = self.recv_process.stdout.read(self.FRAME_WIDTH * self.FRAME_HEIGHT * 3)

                if len(frame_data) != self.FRAME_WIDTH * self.FRAME_HEIGHT * 3:
                    print("Incorrect Frame Data : " + frame_data.decode("utf-8"))
                    return

                if frame_data:
                    print("Received a frame from server")
                    # Convert the frame data to a numpy array
                    frame = numpy.frombuffer(frame_data, dtype=numpy.uint8)
                    frame = frame.reshape((self.FRAME_HEIGHT, self.FRAME_WIDTH, 3))

                    # Convert the frame from BGR to RGB
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    frame = cv2.flip(frame, 1)

                    # Create a QImage from the frame data
                    # image = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
                    image = qimage2ndarray.array2qimage(frame)
                    
                    # Create a QPixmap from the QImage
                    pixmap = QPixmap.fromImage(image)

                    # Set the pixmap in the stream frame label
                    self.meeting_page.labels[1].setPixmap(pixmap)
                    self.meeting_page.labels[1].setFixedSize(self.video_size)
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

    def join_meeting(self):
        self.join_meeting_dialog = JoinMeeting()
        self.join_meeting_dialog.show()
