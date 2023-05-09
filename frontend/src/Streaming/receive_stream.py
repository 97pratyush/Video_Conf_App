from PySide6.QtCore import QThread, Signal
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QLabel
from ffpyplayer.player import MediaPlayer
import cv2, qimage2ndarray, numpy, time, constant as const

class ReceiveStream(QThread):

    participant_frame_changed = Signal(object)

    def __init__(self, url):
        super().__init__()
        self.url = url

    def run(self):
        self._running = True
        player = MediaPlayer(self.url)

        while(self._running):
            frame, val = player.get_frame()
            if val != "eof" and frame is not None:
                img, t = frame
                frame_data = numpy.frombuffer(img.to_bytearray()[0], dtype=numpy.uint8)
                frame_data = frame_data.reshape((const.FRAME_HEIGHT, const.FRAME_WIDTH, 3))
                frame_data = cv2.flip(frame_data, 1)
                image = qimage2ndarray.array2qimage(frame_data)
                pixmap = QPixmap.fromImage(image)
                self.participant_frame_changed.emit(pixmap)
            elif frame is None:
                time.sleep(0.01)


    def stop(self):
        self._running = False
        self.wait()