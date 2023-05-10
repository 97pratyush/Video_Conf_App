from Meeting.meeting_page import MeetingPage
from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import Qt, QSize
from api_requests import end_meeting
from Streaming.send_and_display_video import SendandDisplayVideo
import constant as const
from app_state import state

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
        self.meeting_page.end_meeting_cta.clicked.connect(self.end_call)
        
        self.thread_send_stream = SendandDisplayVideo(self.meeting_page.self_video, self.meeting_id, self.user_id)
        
        try:
            self.thread_send_stream.start()
        except Exception as e:
            print("Exception occured while sending stream :", e)
        finally:
            self.thread_send_stream.stop()

        self.mainWindow.show()

    def end_call(self):
        state.in_meeting = False
        try:
            self.meeting_page.socket_client.close_socket()
            # Stop sending and displaying own video
            self.thread_send_stream.stop()
            self.meeting_page.thread_show_stream.stop()
            end_meeting(self.user_id, self.meeting_id)
            self.mainWindow.close()
            
            print("Ending call and closing streams")
        except Exception as e:
            print("Exception occured during end meeting :", e)
        finally:
            self.mainWindow.close()