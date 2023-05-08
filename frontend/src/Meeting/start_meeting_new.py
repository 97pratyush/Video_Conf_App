from Meeting.meeting_page import MeetingPage
from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import Qt, QSize
from api_requests import end_meeting
from Streaming.send_and_display_video import SendandDisplayVideo
from Streaming.receive_stream import ReceiveStream
import threading, constant as const
from Meeting.socket_client import SocketClient

class StartMeeting:
    def __init__(self, user_details, meeting_id) -> None:

        self.video_size = QSize(const.FRAME_WIDTH, const.FRAME_HEIGHT, alignment = Qt.AlignCenter)
        self.user_details = user_details
        self.user_id = user_details['id']
        self.user_name = user_details['name']
        self.meeting_id = int(meeting_id)

        self.meeting_page = MeetingPage(self.user_details, self.meeting_id)
        self.mainWindow = QMainWindow()
        self.meeting_page.setupUi(self.mainWindow)
        self.meeting_page.end_meeting.clicked.connect(self.end_call)

        self.send_video = SendandDisplayVideo(self.meeting_page.self_video, self.meeting_id, self.user_id)

        # Send using ffmpeg wrapper
        thread_send_stream = threading.Thread(target=self.send_video.send_stream_to_server, daemon=True)
        # thread_send_stream.start()

        # Send using manual subprocess
        thread_send_stream_legacy = threading.Thread(target=self.send_video.send_stream_to_server_legacy, daemon=True)
        thread_send_stream_legacy.start()
        self.mainWindow.show()

    # Need to be called for each participant
    def receive_video_of_participant(self):
        receive_stream = ReceiveStream()
        thread_show_stream = threading.Thread(target=receive_stream.start_participant_stream, args=(self.meeting_page.self_video, self.meeting_id, self.user_id), daemon=True)
        thread_show_stream.start()

    def end_call(self):
        try:
            self.meeting_page.chat_page.socket_client.close_socket()
            end_meeting(self.user_id, self.meeting_id)
            self.mainWindow.close()
            print("Ending call and closing streams")

            # Stop sending and displaying own video
            self.send_video.stop_stream_legacy() # Or self.send_video.stop_stream()
        except:
            self.mainWindow.close()