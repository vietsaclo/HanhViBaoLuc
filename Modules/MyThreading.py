import time
import cv2
import threading
from PIL import Image
from PIL import ImageTk
from Modules import PublicModules as libs
from Modules import LSTM_Config as cf
import random

class MyThreadingVideo:
    def __init__(self, lbShow, lbFather, lbShowKetQua, vgg16_model, lstm_model, treeAction):
        self.vgg16_model = vgg16_model
        self.lstm_model = lstm_model
        self.treeAction = treeAction
        self.frames = None
        self.lbShow = lbShow
        self.lbShowKetQua = lbShowKetQua
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
        transfer = cf.fun_getTransferValue_EDIT(pathVideoOrListFrame= self.frames, modelVGG16= self.vgg16_model)
        pre, real = libs.fun_predict(modelLSTM= self.lstm_model, transferValue=transfer)
        conv = cf.VIDEO_NAMES_DETAIL[pre] if real > 0.7 else 'NO'
        text = 'Predict: {0} -> Real: [ {1} ]'.format(conv, real) if conv != 'NO' else ''

        if self.lbShow is not None:
            # Show thread video
            for frame in self.frames:
                image = libs.fun_cv2_imageArrayToImage(containerFather= self.lbFather, frame= frame.copy(), reSize= 0.8)
                self.lbShow.config(image= image)
                self.lbShow.image = image
                
        self.lbShowKetQua.config(text= text)
        self.treeAction.fun_saveVideoDetection(frames= self.frames, fol= cf.VIDEO_NAMES[pre])