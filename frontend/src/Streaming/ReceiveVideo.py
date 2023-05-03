from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QLabel
import cv2, qimage2ndarray, numpy, subprocess, time, constant as const

class ReceiveVideo():
    def receive_video_frames_using_ffmpeg(self, image_label : QLabel, meeting_id : str, user_id : str):
        url = f'{const.RTMP_URL}/{meeting_id}_{user_id}'
        receive_video_from_server_command = ['ffmpeg',
                #    '-fflags', 'nobuffer',
                   '-an',
                   '-i', f'{url}',
                   '-f', 'rawvideo',
                   '-pix_fmt', 'bgr24',
                   '-bufsize', '300k',
                   '-'
        ]

        time.sleep(10)
        self.receive_video_from_server_process = subprocess.Popen(receive_video_from_server_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=10**8)
        frame_received = False
        self.close_called = False
    
        start_time = time.time()

        try: 
            while(True):
                if self.close_called == True:
                    print("Video receiving stopped : ", url)
                    break
                
                # Wait until frame is received or maximum of 10 seconds
                if ((time.time() - start_time) >= const.MAX_WAIT_TIME_FOR_SERVER and frame_received == False): # Wait a maximum of wait time defined
                    print("No frame receieved even after", const.MAX_WAIT_TIME_FOR_SERVER, "seconds.")
                    break
                
                frame_data = self.receive_video_from_server_process.stdout.read(const.FRAME_WIDTH * const.FRAME_HEIGHT * 3)

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

    def stop_receiving_frames(self):
        self.close_called = True
        if self.receive_video_from_server_process != None:
            if self.receive_video_from_server_process.stdout:
                self.receive_video_from_server_process.stdout.flush()
                self.receive_video_from_server_process.stdout.close()
            self.receive_video_from_server_process.terminate()