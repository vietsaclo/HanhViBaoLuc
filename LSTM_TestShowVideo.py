from Modules import PublicModules as lib
from Modules import LSTM_Config as cf
import numpy as np
import cv2

def fun_predict(modelLSTM, transferValue, isPrint: bool= False):
    arrPre = []
    arrPre.append(transferValue)
    Real = modelLSTM.predict(np.array(arrPre))
    pre = np.argmax(Real)

    if isPrint:
      print(Real, pre)
      print('\r')
    return pre, Real[0][pre]

def fun_showEachVideoInFolder(pathLoad: str):
    fileNames = lib.fun_getFileNames(path= pathLoad)
    for fileName in fileNames:
        cap = lib.fun_getFramesOfVideo(path= pathLoad + '/' + fileName)
        lib.fun_showVideo(source= cap, delay= 30)

def fun_showEachVideoInFolderPredic(pathLoad: str):
    VGG16_model = cf.fun_getVGG16Model()
    LSTM_model = cf.fun_loadModelLSTM()
    fileNames = lib.fun_getFileNames(path= pathLoad)
    countFrame = 0

    for fileName in fileNames:
        frames = lib.fun_getFramesOfVideo(path= pathLoad + '/' + fileName)
        transfer = cf.fun_getTransferValue(pathVideoOrListFrame= frames, modelVGG16= VGG16_model)
        pre, real = fun_predict(modelLSTM=LSTM_model, transferValue=transfer)

        color = (100, 200, 255)
        conv = cf.VIDEO_NAMES_DETAIL[pre]

        text = 'Predict: {0} -> Real: [ {1} ]'.format(conv, real)

        for ff in frames:
            countFrame += 1
            resized = cv2.resize(ff, (int(1280 * 0.6), int(720 * 0.6)), interpolation=cv2.INTER_AREA)
            # putText
            cv2.putText(img=resized,
                        text=text,
                        org=(50, 100),
                        fontScale=1,
                        fontFace=cv2.FONT_HERSHEY_COMPLEX_SMALL,
                        thickness=1,
                        color=color)

            cv2.putText(img=resized,
                        text='Frame Count: {0}'.format(countFrame),
                        org=(50, 150),
                        fontScale=1,
                        fontFace=cv2.FONT_HERSHEY_COMPLEX_SMALL,
                        thickness=1,
                        color=color)

            cv2.imshow('ff', resized)

            if cv2.waitKey(30) == ord('a'):
                print('a')

def fun_showEachVideoInFolderPredicCam(pathLoad):
    VGG16_model = cf.fun_getVGG16Model()
    LSTM_model = cf.fun_loadModelLSTM()
    cap = cv2.VideoCapture('http://192.168.137.99:8080/video')
    isContinue, frame = cap.read()
    countFrame = 0

    while True:
        if not isContinue:
            break
        frames = []
        mumInput = 0
        while mumInput < cf.NUM_FRAME_INPUT_LSTM:
            isContinue, frame = cap.read()
            if not isContinue:
                break
            frames.append(frame)
            mumInput += 1

        transfer = cf.fun_getTransferValue(pathVideoOrListFrame= frames, modelVGG16= VGG16_model)
        pre, real = fun_predict(modelLSTM=LSTM_model, transferValue=transfer)

        color = (100, 200, 255)
        conv = cf.VIDEO_NAMES_DETAIL[pre]

        text = 'Predict: {0} -> Real: [ {1} ]'.format(conv, real)

        for ff in frames:
            countFrame += 1
            resized = cv2.resize(ff, (int(1280 * 0.6), int(720 * 0.6)), interpolation=cv2.INTER_AREA)
            # putText
            cv2.putText(img=resized,
                        text=text,
                        org=(50, 100),
                        fontScale=1,
                        fontFace=cv2.FONT_HERSHEY_COMPLEX_SMALL,
                        thickness=1,
                        color=color)

            cv2.putText(img=resized,
                        text='Frame Count: {0}'.format(countFrame),
                        org=(50, 150),
                        fontScale=1,
                        fontFace=cv2.FONT_HERSHEY_COMPLEX_SMALL,
                        thickness=1,
                        color=color)

            cv2.imshow('ff', resized)

            if cv2.waitKey(30) == ord('a'):
                print('a')


def fun_showEachVideoInFolderPredicMerge(pathLoad: str):
    VGG16_model = cf.fun_getVGG16Model()
    LSTM_model = cf.fun_loadModelLSTM()
    fileNames = lib.fun_getFileNames(path=pathLoad)
    countFrame = 0

    frameMerge = []

    progressInt = 0
    max = len(fileNames)
    for fileName in fileNames:
        frames = lib.fun_getFramesOfVideo(path=pathLoad + '/' + fileName)
        transfer = cf.fun_getTransferValue(pathVideoOrListFrame=frames, modelVGG16=VGG16_model)
        pre, real = fun_predict(modelLSTM=LSTM_model, transferValue=transfer)

        color = (100, 200, 255)
        conv = cf.VIDEO_NAMES_DETAIL[pre]

        text = 'Predict: {0} -> Real: [ {1} ]'.format(conv, real)

        progressInt += 1
        for ff in frames:
            countFrame += 1
            resized = cv2.resize(ff, (int(1280 * 0.6), int(720 * 0.6)), interpolation=cv2.INTER_AREA)
            # putText
            cv2.putText(img=resized,
                        text=text,
                        org=(50, 100),
                        fontScale=1,
                        fontFace=cv2.FONT_HERSHEY_COMPLEX_SMALL,
                        thickness=1,
                        color=color)

            cv2.putText(img=resized,
                        text='Frame Count: {0}'.format(countFrame),
                        org=(50, 150),
                        fontScale=1,
                        fontFace=cv2.FONT_HERSHEY_COMPLEX_SMALL,
                        thickness=1,
                        color=color)

            frameMerge.append(resized)

        lib.fun_print_process(count= progressInt, max= max, mess= 'Video Merge Processing: ')

    lib.fun_showVideo(source= frameMerge, delay= 30)

if __name__ == '__main__':
    fun_showEachVideoInFolderPredicCam(pathLoad= 'http://192.168.137.99:8080')