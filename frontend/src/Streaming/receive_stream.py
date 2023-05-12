from PySide6.QtCore import QThread, Signal
from PySide6.QtGui import QPixmap
from ffpyplayer.player import MediaPlayer
import cv2, qimage2ndarray, numpy, time, constant as const

class ReceiveStream(QThread):

    participant_frame_changed = Signal(object, str)

    def __init__(self, url, id):
        super().__init__()
        self.url = url
        self.id = id

    def run(self):
        try:
            self._running = True
            self.player = MediaPlayer(self.url)
            time.sleep(2)
            while(self._running):
                frame, val = self.player.get_frame()
                if val != "eof" and frame is not None:
                    img, t = frame
                    frame_data = numpy.frombuffer(img.to_bytearray()[0], dtype=numpy.uint8)
                    frame_data = frame_data.reshape((const.FRAME_HEIGHT, const.FRAME_WIDTH, 3))
                    frame_data = cv2.flip(frame_data, 1)
                    image = qimage2ndarray.array2qimage(frame_data)
                    pixmap = QPixmap.fromImage(image)
                    self.participant_frame_changed.emit(pixmap, self.id)
                elif frame is None:
                    time.sleep(0.01)
        except Exception as e:
            print("Exception occured while receiving stream of id :",self.id,".:", e)
        finally:
            self.player.close_player()


    def stop(self):
        self._running = False
        self.player.close_player()
        self.wait()