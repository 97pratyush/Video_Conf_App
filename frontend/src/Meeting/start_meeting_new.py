from Meeting.meeting_page import MeetingPage
from PySide6.QtWidgets import QMainWindow, QLabel
from PySide6.QtCore import Qt, QSize, QTimer
from PySide6.QtGui import QPixmap
from api_requests import end_meeting
from Streaming.send_and_display_video import SendandDisplayVideo
from Streaming.receive_stream import ReceiveStream
import threading, time, cv2, qimage2ndarray, numpy, constant as const
from ffpyplayer.player import MediaPlayer
from Meeting.socket_client import SocketClient
from app_state import state

user_stream_player : MediaPlayer = None

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

        self.send_stream = SendandDisplayVideo(self.meeting_page.self_video, self.meeting_id, self.user_id)
        
        try:
            # Send stream using ffmpeg and display it in UI
            thread_send_stream = threading.Thread(target=self.send_stream.send_stream_to_server, daemon=True)
            thread_send_stream.start()
        except Exception as e:
            print("Exception occured while sending stream :", e)
        finally:
            self.send_stream.stop_stream()

        self.mainWindow.show()
    
    # Need to be called for each participant
    def receive_video_of_participant(self):
        receive_stream = ReceiveStream()
        thread_show_stream = threading.Thread(target=receive_stream.start_participant_stream, args=(self.meeting_page.self_video, self.meeting_id, self.user_id), daemon=True)
        thread_show_stream.start()

    def end_call(self):
        state.in_meeting = False
        try:
            self.meeting_page.socket_client.close_socket()
            # Stop sending and displaying own video
            self.send_stream.stop_stream()
            end_meeting(self.user_id, self.meeting_id)
            self.mainWindow.close()
            
            print("Ending call and closing streams")
        except Exception as e:
            print("Exception occured during end meeting :", e)
        finally:
            self.mainWindow.close()

    def start_participant_stream(self, user_video_tile : QLabel, meeting_id : str, user_id : str):
        time.sleep(10)
        url = f'{const.RTMP_URL}/{meeting_id}_{user_id}'

        user_stream_player = MediaPlayer(url)
        val =''

        while(val != 'eof'):
            frame, val = user_stream_player.get_frame()
            if frame is not None:
                img, t = frame
                frame_data = numpy.frombuffer(img.to_bytearray()[0], dtype=numpy.uint8)
                frame_data = frame_data.reshape((const.FRAME_HEIGHT, const.FRAME_WIDTH, 3))
                frame_data = cv2.flip(frame_data, 1)
                image = qimage2ndarray.array2qimage(frame_data)
                pixmap = QPixmap.fromImage(image)
                user_video_tile.setPixmap(pixmap)
            elif frame is None:
                time.sleep(0.01)

        # def display_stream():
        #     frame, val = user_stream_player.get_frame()
        #     if val != "eof" and frame is not None:
        #         img, t = frame
        #         frame_data = numpy.frombuffer(img.to_bytearray()[0], dtype=numpy.uint8)
        #         frame_data = frame_data.reshape((const.FRAME_HEIGHT, const.FRAME_WIDTH, 3))
        #         frame_data = cv2.flip(frame_data, 1)
        #         image = qimage2ndarray.array2qimage(frame_data)
        #         pixmap = QPixmap.fromImage(image)
        #         user_video_tile.setPixmap(pixmap)
        #     elif frame is None:
        #         time.sleep(0.01)

        # self.timer = QTimer()
        # self.timer.timeout.connect(display_stream)
        # self.timer.start(30)