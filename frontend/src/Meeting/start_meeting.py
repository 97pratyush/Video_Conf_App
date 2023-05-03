from PySide6.QtCore import Qt, QSize
from Meeting.meeting import MeetingPage
from PySide6.QtWidgets import QMainWindow
from api_requests import end_meeting
from Streaming.send_and_display_video import SendandDisplayVideo
from Streaming.receive_video import ReceiveVideo
import threading, constant as const

class StartMeeting(QMainWindow):
    def __init__(self, user_details, meeting_id, parent=None):
        super(StartMeeting, self).__init__(parent)

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
        thread_ffmpeg_send = threading.Thread(target=self.send_video.send_video_using_opencv_pipe, daemon=True)
        thread_ffmpeg_send.start()

    def receive_video_of_participant(self):
        self.receive_video = ReceiveVideo()
        thread_ffmpeg_send = threading.Thread(target=self.receive_video.receive_video_frames_using_ffmpeg, args=(self.meeting_page.labels[0], 'meeting_id', 'user_id'), daemon=True)
        thread_ffmpeg_send.start()

    def end_call(self):
        try:
            end_meeting(self.user_id, self.meeting_id)
            self.close()
            print("Ending call and closing streams")
            # Stop sending and displaying own video
            self.send_video.stop_sending_video_opencv()
            # Stop receiving process of each participant
            # self.receive_video.stop_receiving_frames()
        except:
            self.close()