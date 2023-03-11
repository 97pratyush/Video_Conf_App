import cv2
import numpy
import subprocess
from PySide6 import QtCore, QtWidgets, QtGui

# Define the dimensions of the video frames
FRAME_WIDTH = 640
FRAME_HEIGHT = 480

# Define the IP address and port number of the server
SERVER_IP = 'localhost'
SERVER_PORT = 8080

class VideoStream(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Initialize the video capture object
        self.capture = cv2.VideoCapture(0)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

        # Initialize the network stream object
        self.stream = None

        # Create the GUI
        self.setup_ui()

        # Start the video stream
        self.start_stream()

    def setup_ui(self):
        # Create the widgets
        self.video_frame = QtWidgets.QLabel()
        self.stream_frame = QtWidgets.QLabel()
        self.quit_button = QtWidgets.QPushButton('Quit')

        # Create the layout
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.video_frame)
        layout.addWidget(self.stream_frame)

        # Set the layout
        self.setLayout(layout)

        # Connect the signals and slots
        self.quit_button.clicked.connect(self.close)

    def start_stream(self):
        # Start the network stream
        command = ['ffmpeg',
                   '-f', 'rawvideo',
                   '-pix_fmt', 'bgr24',
                   '-s', f"{FRAME_WIDTH}x{FRAME_HEIGHT}",
                   '-i', '-',
                   '-pix_fmt', 'yuv420p',
                   '-f', 'mpegts',
                   f"udp://{SERVER_IP}:{SERVER_PORT}"]
        self.stream = subprocess.Popen(command, stdin=subprocess.PIPE)

        # Start the video stream loop
        while True:
            # Read a frame from the video capture object
            ret, frame = self.capture.read()
            if not ret:
                break

            # Display the video frame in the GUI
            self.display_video_frame(frame)

            # Send the video frame to the network stream
            self.send_video_frame(frame)

        # Stop the network stream
        self.stream.stdin.close()
        self.stream.wait()

    def display_video_frame(self, frame):
        # Convert the frame from BGR to RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Create a QImage from the frame data
        image = QtGui.QImage(frame.data, frame.shape[1], frame.shape[0],
                             QtGui.QImage.Format_RGB888)

        # Create a QPixmap from the QImage
        pixmap = QtGui.QPixmap.fromImage(image)

        # Set the pixmap in the video frame label
        self.video_frame.setPixmap(pixmap)

    def send_video_frame(self, frame):
        # Write the frame to the network stream
        self.stream.stdin.write(frame.tobytes())
        self.stream.stdin.flush()

        # Receive the streamed frame from the server
        recv_command = ['ffmpeg',
                        '-i', f"udp://{SERVER_IP}:{SERVER_PORT}",
                        '-pix_fmt', 'rgb24',
                        '-f', 'rawvideo',
                        '-']
        recv_process = subprocess.Popen(recv_command, stdout=subprocess.PIPE)
        while True:
            # Read a frame from the network stream
            frame_data = recv_process.stdout.read(FRAME_WIDTH * FRAME_HEIGHT * 3)
            if not frame_data:
                break

            # Convert the frame data to a numpy array
            frame = numpy.frombuffer(frame_data, dtype=numpy.uint8)
            frame = frame.reshape((FRAME_HEIGHT, FRAME_WIDTH, 3))

            # Display the streamed frame in the GUI
            self.display_stream_frame(frame)

    def display_stream_frame(self, frame):
        # Convert the frame from BGR to RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Create a QImage from the frame data
        image = QtGui.QImage(frame.data, frame.shape[1], frame.shape[0],
                             QtGui.QImage.Format_RGB888)

        # Create a QPixmap from the QImage
        pixmap = QtGui.QPixmap.fromImage(image)

        # Set the pixmap in the stream frame label
        self.stream_frame.setPixmap(pixmap)

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = VideoStream()
    window.show()
    app.exec_()

