from PySide6.QtCore import Qt, QSize
from Meeting.meeting import MeetingPage
from PySide6.QtWidgets import QMainWindow
from PySide6.QtGui import QPixmap
from api_requests import end_meeting
from Streaming.send_and_display_video import SendandDisplayVideo
from Streaming.receive_stream import ReceiveStream
from ffpyplayer.player import MediaPlayer
import threading, qimage2ndarray, numpy, time, cv2, constant as const

class StartMeeting(QMainWindow):
    def __init__(self, user_details, meeting_id, parent=None):
        super(StartMeeting, self).__init__(parent)

        self.meeting_streams = {}
        self.video_size = QSize(const.FRAME_WIDTH, const.FRAME_HEIGHT, alignment = Qt.AlignCenter)
        self.user_id = user_details['id']
        self.user_name = user_details['name']
        self.meeting_id = int(meeting_id)
        self.meeting_page = MeetingPage()
        self.meeting_page.end_call_button.clicked.connect(self.end_call)
        
        self.setCentralWidget(self.meeting_page)
        self.setWindowTitle(f"{self.user_name} - {self.meeting_id}")
        self.resize(700, 500)
        self.setAutoFillBackground(True)
        self.setStyleSheet("QMainWindow" "{" "background : #313a46;" "}")
        
        # Send and display own video
        self.send_video = SendandDisplayVideo(self.meeting_page.labels[0], self.meeting_id, self.user_id)

        # Send using manual subprocess
        thread_send_stream = threading.Thread(target=self.send_video.send_stream_to_server, daemon=True)
        thread_send_stream.start()

        time.sleep(2)

        thread_show_stream = threading.Thread(target=self.receive_video_of_participant, daemon=True)
        thread_show_stream.start()


    # Need to be called for each participant
    def receive_video_of_participant(self):
        url = f'{const.RTMP_URL}/{self.meeting_id}_{self.user_id}'
        print(url)

        user_stream_player = MediaPlayer(url)

        self.meeting_streams[self.user_id] = user_stream_player
        try:
            while(True):
                frame, val = user_stream_player.get_frame()
                if val != "eof" and frame is not None:
                    img, t = frame
                    frame_data = numpy.frombuffer(img.to_bytearray()[0], dtype=numpy.uint8)
                    frame_data = frame_data.reshape((const.FRAME_HEIGHT, const.FRAME_WIDTH, 3))
                    frame_data = cv2.flip(frame_data, 1)
                    image = qimage2ndarray.array2qimage(frame_data)
                    pixmap = QPixmap.fromImage(image)
                    self.meeting_page.labels[0].setPixmap(pixmap)
                elif frame is None:
                    time.sleep(0.01)
        except Exception as e:
            print("Exception occured during receiving stream from url", url, ":", e)
        

    def end_call(self):
        try:
            end_meeting(self.user_id, self.meeting_id)
            self.close()
            print("Ending call and closing streams")

            # Stop sending and displaying own video
            self.send_video.stop_stream() # Or self.send_video.stop_stream()
        except:
            self.close()