from PySide6.QtCore import QThread
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QLabel
from ffpyplayer.player import MediaPlayer
import cv2, qimage2ndarray, numpy, time, constant as const

# class ReceiveStream(QThread):
class ReceiveStream():
    # def __init__(self, image_label : QLabel, url : str):
    #     super().__init__()
    #     self.image_label = image_label
    #     self.url = url

    def start_participant_stream(self, user_video_tile : QLabel, meeting_id : str, user_id : str):
        url = f'{const.RTMP_URL}/{meeting_id}_{user_id}'

        user_stream_player = MediaPlayer(url)

        while(True):
            frame, val = user_stream_player.get_frame()
            if val != "eof" and frame is not None:
                img, t = frame
                frame_data = numpy.frombuffer(img.to_bytearray()[0], dtype=numpy.uint8)
                frame_data = frame_data.reshape((const.FRAME_HEIGHT, const.FRAME_WIDTH, 3))
                frame_data = cv2.flip(frame_data, 1)
                image = qimage2ndarray.array2qimage(frame_data)
                pixmap = QPixmap.fromImage(image)
                user_video_tile.setPixmap(pixmap)
            elif frame is None:
                time.sleep(0.01)