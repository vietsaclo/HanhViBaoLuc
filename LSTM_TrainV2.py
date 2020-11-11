#----------------------- import --------------------------

from tensorflow.keras.applications import VGG16
from tensorflow.keras.models import Model, Sequential, load_model
import numpy as np
from random import shuffle
from tensorflow.keras.layers import LSTM, Dense, Activation
import matplotlib.pyplot as plt

#----------------------- CONST --------------------------

DIR_ROOT = ''
DIR_INPUT_TRAIN = DIR_ROOT + 'Train_30_10_2020_2'
DIR_MODEL_LSTM = DIR_ROOT + 'Models/LSTM_Train_30_10_2020_2.h5'
DIR_MODEL_CNN = DIR_ROOT + 'Models/VGG16_Model.h5'
SIZE = (224, 224)
NUM_FRAME_INPUT_LSTM = 20
TRANSFER_VALUE_SIZE = 4096
RNN_SIZE = 512
EPOCH = 300
BATCH_SIZE = 150

VIDEO_NAMES = [
  'da',
  'dn',
  'nt',
  'no'
]

VIDEO_NAMES_DETAIL = [
  'Đá',
  'Đánh, tát',
  'Nắm tóc',
  'Không có bạo lực'
]

VIDEO_LABELS = [
  [1, 0, 0, 0],
  [0, 1, 0, 0],
  [0, 0, 1, 0],
  [0, 0, 0, 1]
]

NUM_CLASSIFY = len(VIDEO_NAMES)

#----------------------- LIB --------------------------

import os
import cv2
import sys
import zipfile


def fun_print(name: str, value) -> None:
    print('@ Deep Learning> ', name)
    print(value)


def fun_getFileNames(path: str) -> list:
    return os.listdir(path)


def fun_showVideoPath(path: str, delay: int = 25) -> None:
    cap = cv2.VideoCapture(path)
    isContinue, frame = cap.read()
    while True:
        if not isContinue:
            break
        cv2.imshow('frame', frame)
        if cv2.waitKey(delay=delay) & 0xFF == ord('q'):
            break
        isContinue, frame = cap.read()

    cap.release()
    cv2.destroyAllWindows()


def fun_getFramesOfVideo(path: str, count: int = 20) -> list:
    cap = cv2.VideoCapture(path)
    isContinue, frame = cap.read()
    imgs = []
    while count > 0:
        if not isContinue:
            break
        imgs.append(frame)
        isContinue, frame = cap.read()
        count -= 1
    cap.release()
    cv2.destroyAllWindows()
    return imgs


def fun_getFramesOfVideo_ALL(path: str) -> list:
    cap = cv2.VideoCapture(path)
    isContinue, frame = cap.read()
    imgs = []
    while True:
        if not isContinue:
            break
        imgs.append(frame)
        isContinue, frame = cap.read()
    cap.release()
    cv2.destroyAllWindows()
    return imgs


def fun_showVideoFrames(frames: list, delay: int = 25) -> None:
    for frame in frames:
        cv2.imshow('frame', frame)
        if cv2.waitKey(delay=delay) & 0xFF == ord('q'):
            break


def fun_showVideo(source, delay: int = 25) -> None:
    if isinstance(source, str):
        fun_showVideoPath(path=source, delay=delay)
    else:
        fun_showVideoFrames(frames=source, delay=delay)


def fun_resizeFrames(frames: list, size: tuple = (224, 224)) -> list:
    imgs = []
    count = 0
    for frame in frames:
        try:
            fr = cv2.resize(frame, dsize=size)
            imgs.append(fr)
        except:
            print('\r!Error To Resize of {0}'.format(count))
        count += 1
    cv2.destroyAllWindows()
    return imgs


def fun_saveFramesToVideo(frames: list, path: str, fps: int = 25) -> bool:
    try:
        height, width, layer = frames[0].shape
        wr = cv2.VideoWriter(path, cv2.VideoWriter_fourcc(*'MJPG'), fps, (width, height))
        for frame in frames:
            wr.write(frame)
        wr.release()
        cv2.destroyAllWindows()
        return True

    except:
        fun_print(name='Write Video: ' + path, value='ERROR TO WRITE VIDEO')
        return False


def fun_getSizeOfFrame(frame) -> tuple:
    height, width, layer = frame.shape
    return (width, height)


# version 1
def fun_outListVideoWithNumFrame(pathVideoLoad: str, dirToSave: str, preFixName: str, videoNameIndex: int = None,
                                 countFrame: int = 40, fps: int = 25, isShowCalculating: bool = False) -> int:
    if videoNameIndex is None:
        fun_print('fun_outListVideoWithNumFrame', 'Please input para: videoNameIndex')
        return 0

    all = 0
    countWriten = 0
    if isShowCalculating:
        fun_print('Calculator Video Out Frame', 'calculating...')
        all = fun_getFramesOfVideo_ALL(pathVideoLoad)
        all = len(all) // countFrame

    cap = cv2.VideoCapture(pathVideoLoad)
    isContinue, frame = cap.read()
    count = videoNameIndex
    while True:
        if not isContinue:
            break
        nameFile = dirToSave + preFixName + '_out_' + str(count) + '.avi'
        cFrame = countFrame
        frames = []

        # get list frame
        while cFrame > 0:
            frames.append(frame)
            isContinue, frame = cap.read()
            if not isContinue:
                break
            cFrame -= 1

        # check video enough frameCount frame ?
        if len(frames) != countFrame:
            break

        # write list frame
        res = fun_saveFramesToVideo(frames=frames, path=nameFile, fps=fps)
        countWriten += 1
        if res:
            if isShowCalculating:
                percent = countWriten / all
                mess = '\r - Writen: {0} -> Complete: {1:.1%}'.format(nameFile, percent)
                sys.stdout.write(mess)
                sys.stdout.flush()
            else:
                mess = '\r - Writen: {0} -> Complete'.format(nameFile)
                sys.stdout.write(mess)
                sys.stdout.flush()

        # done
        count += 1

    cap.release()
    cv2.destroyAllWindows()
    return count


def fun_extractZipFile(pathFileZip: str, pathToSave: str) -> None:
    if not os.path.exists(pathToSave):
        os.makedirs(pathToSave)
    fun_print(name='Extract All ' + pathFileZip, value='Extracting...')
    if (pathFileZip.endswith('.zip')):
        zipfile.ZipFile(file=pathFileZip, mode='r').extractall(path=pathToSave)
        print('Extract Done')
    else:
        print('Please Input zip file')


def fun_print_process(count: int, max: int, mess: str = 'Processing: ') -> None:
    process = count / max
    mess = '\r - ' + mess + ' [{0:.1%}]'.format(process)
    sys.stdout.write(mess)
    sys.stdout.flush()


def getModelLSTM(rnn_size: int = 512, input_shape: tuple = (20, 4096), num_classify: int = 3):
    modelLSTM = Sequential()
    modelLSTM.add(LSTM(rnn_size, input_shape=input_shape))
    modelLSTM.add(Dense(1024))
    modelLSTM.add(Activation('relu'))
    modelLSTM.add(Dense(50))
    modelLSTM.add(Activation('sigmoid'))
    modelLSTM.add(Dense(num_classify))
    modelLSTM.add(Activation('softmax'))
    modelLSTM.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])
    return modelLSTM


def fun_predict(modelLSTM, transferValue, isPrint: bool = True):
    arrPre = []
    arrPre.append(transferValue)
    Real = modelLSTM.predict(np.array(arrPre))
    pre = np.argmax(Real)

    if isPrint:
        print(Real, pre)
        print('\r')
    return pre, Real[0][pre]

def fun_mergeVideo(dirInput: str, videoNames: list, pathSave, fps: int = 25):
    count = 0
    max = len(videoNames)
    sizeVideoOut = (int(1280 * 0.7), int(720 * 0.7))
    wr = cv2.VideoWriter(pathSave, cv2.VideoWriter_fourcc(*'MJPG'), fps, sizeVideoOut)
    for name in videoNames:
        frames = fun_getFramesOfVideo_ALL(path=dirInput + name)
        frames = fun_resizeFrames(frames=frames, size=sizeVideoOut)
        for frame in frames:
            wr.write(frame)
        fun_print_process(count=count, max=max, mess='Merge video processing: ')
        count += 1
    wr.release()
    cv2.destroyAllWindows()

#-----------------------------
modelCNN = VGG16(include_top= True, weights= 'imagenet')
modelCNN.summary()

frames = fun_getFramesOfVideo(path= DIR_INPUT_TRAIN + '/da/da1_111_001.avi', count=20)

fun_print('count frame: ', value=len(frames))

transferLayer = modelCNN.get_layer(name='fc2')

imgModelTransfer = Model(inputs= modelCNN.input, outputs= transferLayer.output)

frames = fun_resizeFrames(frames= frames, size=SIZE)

frames = np.array(frames)
frames = (frames / 255.).astype(np.float16)

transfer = imgModelTransfer.predict(frames)
print(transfer)

def onesHotLabel(label: list):
  _ones = np.ones([NUM_FRAME_INPUT_LSTM, NUM_CLASSIFY])
  _onesHot = label * _ones
  return np.array(_onesHot)

_oneHot = onesHotLabel([1, 0, 0, 0])
fun_print(name='oneHost', value= _oneHot)


def getVideoLabelNames_EachFolder(path: str):
    names = []
    labels = []

    for fol in VIDEO_NAMES:
        folder = path + '/' + fol
        fileNames = fun_getFileNames(path=folder)
        index = VIDEO_NAMES.index(fol)
        for file in fileNames:
            names.append('/' + fol + '/' + file)
            labels.append(VIDEO_LABELS[index])

    c = list(zip(names, labels))
    shuffle(c)

    names, labels = zip(*c)
    return names, labels


def getTransferValue(pathVideoOrListFrame):
    if isinstance(pathVideoOrListFrame, str):
        frames = fun_getFramesOfVideo(path=pathVideoOrListFrame, count=NUM_FRAME_INPUT_LSTM)
    else:
        frames = pathVideoOrListFrame

    frames = fun_resizeFrames(frames=frames, size=SIZE)

    frames = np.array(frames)
    frames = (frames / 255.).astype(np.float16)

    transfer = imgModelTransfer.predict(frames)
    return transfer

names, labels = getVideoLabelNames_EachFolder(path= DIR_INPUT_TRAIN)

fun_print(name= 'Size of List video', value= len(names))
fun_print(name= 'Size of List labels', value= len(labels))

print('= '*50)

print(names[0:5])
print(labels[0:5])

print('= '*50)

print(getTransferValue(DIR_INPUT_TRAIN + names[0]))
print(onesHotLabel(labels[0]))


def getTrainSet_LabelSet(numItem: int):
    count = 0
    trainSet = []
    labelSet = []
    while count < numItem:
        itemTrain = getTransferValue(pathVideoOrListFrame=DIR_INPUT_TRAIN + names[count])
        itemLable = onesHotLabel(label=labels[count])

        trainSet.append(itemTrain)
        labelSet.append(itemLable[0])

        fun_print_process(count=count, max=numItem, mess='Video frame throw into VGG16 Model Processing: ')

        count += 1

    return trainSet, labelSet


trainSet, labelSet = getTrainSet_LabelSet(numItem= len(names))
fun_print(name= 'Get transfer value', value= 'Finish')

print(len(trainSet))
print(len(trainSet[0]))
print(len(trainSet[0][0]))

print(len(labelSet))
print(labelSet[0])
print(labelSet[0][0])

model = getModelLSTM(num_classify= NUM_CLASSIFY)
model.summary()

history = model.fit(np.array(trainSet[0:750]), np.array(labelSet[0:750]), epochs=EPOCH,
                    validation_data=(np.array(trainSet[750:]), np.array(labelSet[750:])),
                    batch_size=BATCH_SIZE, verbose=2)
model.save(DIR_MODEL_LSTM)
fun_print(name= 'LSTM Train', value= 'Finish')

