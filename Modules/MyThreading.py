import time
import cv2
import threading
from PIL import Image
from PIL import ImageTk

class MyThreadingVideo:
    def __init__(self, lbShow, lbFather):
        self.frames = None
        self.lbShow = lbShow
        self.lbFather = lbFather
        self.myThread = threading.Thread(target=self.VideoThread)
        self.myThread.setDaemon(True)

    def setFrames(self, frames: list):
        self.frames = frames

    def isBusy(self):
        return self.myThread.isAlive()

    def startShowVideo(self):
        self.myThread = threading.Thread(target=self.VideoThread)
        self.myThread.setDaemon(True)
        self.myThread.start()

    def VideoThread(self):
        # Predict cho moi 20Frames Anh tai day

        for frame in self.frames:
            winWidth = int(self.lbFather.winfo_width() * 0.8)
            winHeight = int(self.lbFather.winfo_height() * 0.8)
            frame = cv2.resize(frame, (winWidth, winHeight))
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(image)
            image = ImageTk.PhotoImage(image)
            self.lbShow.config(image= image)
            self.lbShow.image = image
            # time.sleep(0.02)
