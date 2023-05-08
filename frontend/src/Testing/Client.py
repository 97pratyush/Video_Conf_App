from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtMultimedia import *
from PySide6.QtMultimediaWidgets import *
from Test import VideoThread, AudioStream
from Streaming.send_and_display_video import SendandDisplayVideo
from Streaming.receive_stream import ReceiveStream
import constant as const
import sys, cv2, qimage2ndarray, numpy, subprocess, threading, pyaudio, vlc, time
from ffpyplayer.player import MediaPlayer

MEETING_ID = 'test'
USER_ID = 'test'

class VideoConferencingHomePage(QWidget):
    def __init__(self):
        super().__init__()

        self.send_default_audio_video_command = ['ffmpeg', 
                    '-f', 'v4l2',
                    '-s', f'{const.FRAME_WIDTH}x{const.FRAME_HEIGHT}', 
                    '-thread_queue_size', '1024',
                    '-i', '/dev/video0',
                    '-f', 'alsa',
                    '-thread_queue_size', '1024',
                    '-i', 'default',
                    '-c:v', 'libx264',
                    '-preset', 'ultrafast',
                    '-tune', 'zerolatency',
                    '-b:v', '100k',
                    '-c:a', 'aac', 
                    '-ar', '44100',
                    '-ac', '1',
                    '-af', 'afftdn',
                    '-maxrate', '3000k',
                    '-bufsize', '300k',
                    '-f', f'{const.VIDEO_CODEC}',
                    f'{const.RTMP_URL}/{MEETING_ID}_{USER_ID}'
        ]
        # self.stream = subprocess.Popen(self.send_default_audio_video_command, stdin=subprocess.PIPE, stderr=subprocess.PIPE)

        #Audio only command
        # self.recv_command = [
        #             'ffmpeg',
        #             '-re',
        #             '-i', f'{RTMP_URL}',
        #             '-vn',
        #             '-f', 'adts',
        #             '-'
        #         ]

        # self.stream = None
        self.receive_video_from_server_process = None
        self.close_called = False
        self.receive_process_invoked = False
        self.capture = None
        self.audio_stream = None
        self.send_video = None

        # self.title = QLabel("<font color=#fc1803 size=40>Video Conferencing App</font>", alignment=Qt.AlignHCenter)
        # self.send_video_to_server_button = QPushButton("Send Video to Server")
        # self.receive_video_from_server_button = QPushButton("Receive Video from Server")
        # self.layout = QVBoxLayout(self)
        # self.layout.addWidget(self.title)
        # self.layout.addWidget(self.send_video_to_server_button)
        # self.layout.addWidget(self.receive_video_from_server_button)

        # self.send_video_to_server_button.clicked.connect(self.send_video_to_server)
        # self.receive_video_from_server_button.clicked.connect(self.start_stream_thread)

    def closeEvent(self, event):
        print("Quitting Application")

        self.close_called = True

        # if self.stream != None:
        #     self.stream.terminate() 

        if self.capture != None:
            self.capture.release()

        if self.receive_process_invoked == True and self.receive_video_from_server_process != None:
            self.receive_video_from_server_process.stdout.close()
            self.receive_video_from_server_process.terminate()

        if self.audio_stream != None:
            self.audio_stream.stop_stream()
            self.audio_stream.close()
            self.p.terminate()

        if self.send_video:
            self.send_video.stop_stream()

        super().closeEvent(event)

    # OpenCV Implementation
    Slot()
    def send_video_to_server(self):
        self.setup_ui()
        self.test_stream()
        # thread_opencv = threading.Thread(target=self.display_video_frame_using_opencv, args=(self.image_label, RTMP_URL))
        # thread_opencv.start()
    
    def setup_ui(self):
        """Initialize widgets.
        """
        self.video_size = QSize(const.FRAME_WIDTH, const.FRAME_HEIGHT, alignment = Qt.AlignCenter)
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

        self.layout.addWidget(self.image_label)
        self.layout.addWidget(self.stream_label)
        self.layout.addWidget(self.display_frame_button)
        self.layout.addWidget(self.quit_button)

        self.setLayout(self.layout)

    def test_stream(self):
        
        # Send and display Video 
        self.send_video = SendandDisplayVideo(self.image_label, 'test', 'test')

        # Send using manual subprocess
        thread_ffmpeg_send = threading.Thread(target=self.send_video.send_stream_to_server_legacy, daemon=True)
        thread_ffmpeg_send.start()
        
        thread_send_stream = threading.Thread(target=self.send_video.send_stream_to_server, daemon=True)
        # thread_send_stream.start()

        # global player
        # player = MediaPlayer(url)
        receive_stream = ReceiveStream()
        thread_show_stream = threading.Thread(target=receive_stream.start_participant_stream, args=(self.stream_label, 'test', 'test'), daemon=True)
        thread_show_stream.start()

        # print("HEHEHEH")
        # self.test_audio()

        def handle_quit():
            print()

        app.aboutToQuit.connect(handle_quit)


    def test_audio(self):
        global player, player2
        player = MediaPlayer('rtmp://10.0.0.248/live/stream1')
        player2 = MediaPlayer('rtmp://10.0.0.248/live/stream')

    def display_video_frame_using_opencv(self, label : QLabel, meeting_id : str, user_id : str):
        # URL in the form of rtmp://server/meeting_user
        url = f'{const.RTMP_URL}/{meeting_id}_{user_id}'

        opencv_video_stream = cv2.VideoCapture(url, cv2.CAP_FFMPEG)

        start_time = time.time()
        self.frame_received = False

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
                        self.frame_received = True
                        frame = cv2.resize(frame, (const.FRAME_WIDTH, const.FRAME_HEIGHT))

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
                        if ((time.time() - start_time) >= const.MAX_WAIT_TIME_FOR_SERVER and self.frame_received == False): # Wait a maximum of wait time defined
                            print("No frame receieved even after", const.MAX_WAIT_TIME_FOR_SERVER, "seconds.")
                            return

                except Exception as e:
                    print("Failed : ", e)
                
        except Exception as e:
            print("Exception in displaying : ", e)
        finally:
            opencv_video_stream.release()

    def display_video_frame_using_ffmpeg_subprocess(self, image_label : QLabel, meeting_id : str, user_id : str):
        
        url = f'{const.RTMP_URL}/{meeting_id}_{user_id}'
        self.receive_video_from_server_command = ['ffmpeg',
                #    '-fflags', 'nobuffer',
                   '-an',
                   '-i', f'{url}',
                   '-f', 'rawvideo',
                   '-pix_fmt', 'bgr24',
                   '-bufsize', '300k',
                   '-'
        ]

        # Start process first
        self.receive_video_from_server_process = subprocess.Popen(self.receive_video_from_server_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=10**8)
        self.receive_process_invoked = True
        self.frame_received = False

        start_time = time.time()

        try: 
            while(True):
                if self.close_called == True:
                    print("Video receiving stopped : ", url)
                    break
                
                # Wait until frame is received or maximum of 10 seconds
                if ((time.time() - start_time) >= const.MAX_WAIT_TIME_FOR_SERVER and self.frame_received == False): # Wait a maximum of wait time defined
                    print("No frame receieved even after", const.MAX_WAIT_TIME_FOR_SERVER, "seconds.")
                    return
                
                frame_data = self.receive_video_from_server_process.stdout.read(const.FRAME_WIDTH * const.FRAME_HEIGHT * 3)

                if frame_data:
                    self.frame_received = True
                    # Convert the frame data to a numpy array
                    frame = numpy.frombuffer(frame_data, dtype=numpy.uint8)
                    frame = frame.reshape((const.FRAME_HEIGHT, const.FRAME_WIDTH, 3))
                    # Convert the frame from BGR to RGB
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    frame = cv2.flip(frame, 1)
                    # Create a QImage from the frame data
                    image = qimage2ndarray.array2qimage(frame)
                    # Create a QPixmap from the QImage
                    pixmap = QPixmap.fromImage(image)
                    # Set the pixmap in the stream frame label
                    image_label.setPixmap(pixmap)
                    self.receive_video_from_server_process.stdout.flush()
                else:
                    self.receive_video_from_server_process.stdout.flush()
                    time.sleep(0.1)
                    continue

        except Exception as e:
            print("Exception occured while receiving frames : ", e)
        finally:
            print("Closing Receive stream")
            if self.receive_video_from_server_process != None:
                if self.receive_video_from_server_process.stdout:
                    self.receive_video_from_server_process.stdout.close()
                self.receive_video_from_server_process.terminate()

    Slot()
    def start_stream_thread(self):
        """
            Mark this as true to close necessary operations when program ends.
        """
        self.receive_process_invoked = True
        self.setup_ui()

        """ 
            Display frame directly using OpenCV. 
            Call this after ffmpeg starts sending frames from the client, calling it before any data is published on rtmp will lead to failure.
        """
        thread_opencv_display = threading.Thread(target=self.display_video_frame_using_opencv, args=(self.image_label, 'test', 'test'))
        thread_opencv_display.start()

        """
            Display frame by capturing piped output.
            Can be initiated anytime.
        """
        #Display it in a new thread
        # thread_ffmpeg_display = threading.Thread(target=self.display_video_frame_using_ffmpeg_subprocess, args=(self.image_label, 'test', 'test'), daemon=True)
        # thread_ffmpeg_display.start()
        

        """Audio tests"""
        # thread_stream_audio = threading.Thread(target=self.stream_audio_play)
        # thread_stream_audio.start()

        """Works but a lot of delay"""
        # thread_stream_audio = threading.Thread(target=self.test_play)
        # thread_stream_audio.start()

    def thread_finished(self):
        print("Thread closed")

    # def test_play(self):
    #     vlc_instance = vlc.Instance()
    #     media_player = vlc_instance.media_player_new()
    #     Media = vlc_instance.media_new(const.RTMP_URL)
    #     Media.get_mrl()
    #     media_player.set_media(Media)
    #     media_player.play()

    # def stream_audio_play(self):
    #     print("Reading audio from server")

    #     self.p = pyaudio.PyAudio()
    #     self.audio_stream = self.p.open(
    #         format=pyaudio.paInt16,
    #         channels=1,
    #         rate=44100,
    #         output=True,
    #         frames_per_buffer=1024
    #     )
        
    #     while(True):
    #         try:
    #             # Play audio from stdout
    #             if self.close_called == True:
    #                 break
    #             data = self.receive_video_from_server_process.stdout.read(const.FRAME_HEIGHT * const.FRAME_WIDTH * 2)
    #             self.audio_stream.write(data)
    #         except Exception as e:
    #             # print("Exception occured during audio receive : ", e)
    #             continue
    #         finally:
    #             if self.audio_stream != None:
    #                 self.audio_stream.stop_stream()
    #                 self.audio_stream.close()
    #             if self.p != None:
    #                 self.p.terminate()
    #             self.receive_video_from_server_process.stdout.flush()
    #             self.receive_video_from_server_process.terminate()
    #             self.receive_video_from_server_process.wait()
        
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