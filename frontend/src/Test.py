import ffmpeg, constant as const, sys, subprocess, time, numpy, cv2, qimage2ndarray, pyaudio
from PySide6.QtCore import Qt, QThread, Signal, Slot
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtWidgets import QApplication, QLabel
from pydub import AudioSegment
from pydub.playback import play
from io import BytesIO

class VideoThread(QThread):

    def __init__(self, image_label : QLabel, url : str):
        super().__init__()
        self.image_label = image_label
        self.url = url

    def run(self):
        try: 
            process : subprocess.Popen = (
                ffmpeg
                .input(self.url)
                .output('pipe:', format='rawvideo', pix_fmt='bgr24')
                .run_async(pipe_stdout=True)
            )
            time.sleep(10)
            print("Made ffmpeg process")
            frame_received = False
            self.close_called = False
        
            start_time = time.time()

            while(True):
                if self.close_called == True:
                    print("Video receiving stopped : ", self.url)
                    break
                
                # Wait until frame is received or maximum of 10 seconds
                if ((time.time() - start_time) >= const.MAX_WAIT_TIME_FOR_SERVER and frame_received == False): # Wait a maximum of wait time defined
                    print("No frame receieved even after", const.MAX_WAIT_TIME_FOR_SERVER, "seconds.")
                    break
                
                frame_data = process.stdout.read(const.FRAME_WIDTH * const.FRAME_HEIGHT * 3)

                if frame_data:
                    frame_received = True
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
                    self.image_label.setPixmap(pixmap)
                    process.stdout.flush()
                else:
                    process.stdout.flush()
                    time.sleep(0.1)
                    continue

        except Exception as e:
            print("Exception occured while receiving frames : ", e)
        finally:
            print("Closing Receive stream")
            if process != None:
                if process.stdout:
                    process.stdout.close()
                process.terminate()
    
    def stop(self):
        self._stop_requested = True

class AudioStream():
    def __init__(self, url : str):
        super().__init__()
        self.url = url

    def audio_play(self):
        try:
            audio = ffmpeg.input(self.url)
            time.sleep(5)
            process : subprocess.Popen = audio.output('pipe:', format='adts', ac=1, ar='44100').run_async(pipe_stdout=True)
            while True:
                in_bytes = process.stdout.read(320*240*2)
                if not in_bytes:
                    break
                audio_data = AudioSegment.from_file(BytesIO(in_bytes))
                play(audio_data)
                process.stdout.flush()
        except Exception as e:
            print("Exception occured while receiving audio : ", e)
        finally:
            print("Closing Receive audio stream")
            if process != None:
                if process.stdout:
                    process.stdout.close()
                process.terminate()

    def pyaudio_play(self):
        
        try:
            self.p = pyaudio.PyAudio()
            self.audio_stream = self.p.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=44100,
                output=True,
                frames_per_buffer=1024
            )

            audio = ffmpeg.input(self.url)
            time.sleep(5)
            process : subprocess.Popen = audio.output('pipe:', format='adts', ac=1, ar='44100').run_async(pipe_stdout=True)
            while True:
                in_bytes = process.stdout.read(1024)
                if not in_bytes:
                    break
                self.audio_stream.write(in_bytes)
                process.stdout.flush()
        except Exception as e:
            print("Exception occured while receiving audio : ",)
        finally:
            print("Closing Receive audio stream")
            if self.audio_stream != None:
                    self.audio_stream.stop_stream()
                    self.audio_stream.close()
            if self.p != None:
                self.p.terminate()
            if process != None:
                if process.stdout:
                    process.stdout.close()
                process.terminate()