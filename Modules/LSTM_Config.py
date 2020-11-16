######################## config ##############################

from keras.applications import VGG16
from keras.models import Model
import numpy as np
from random import shuffle
from Modules import PublicModules as lib
from keras.models import Sequential
from keras.layers import LSTM, Dense, Activation
import matplotlib.pyplot as plt

DIR_ROOT = ''
DIR_INPUT_TRAIN = DIR_ROOT + 'Data/Train'
DIR_INPUT_TEST = DIR_ROOT + 'Data/Test'
DIR_INPUT_VALIDATION = DIR_ROOT + 'Data/Validation'
DIR_MODEL_LSTM = DIR_ROOT + 'Modules/LSTM_Train_16_11_2020.h5'
DIR_MODEL_CNN = DIR_ROOT + 'Modules/VGG16_Model.h5'
SIZE = (224, 224)
NUM_FRAME_INPUT_LSTM = 20
TRANSFER_VALUE_SIZE = 4096
RNN_SIZE = 512
EPOCH = 10
BATCH_SIZE = 150

VIDEO_NAMES = [
    'da',
    'dn',
    'om'
]

VIDEO_NAMES_DETAIL = [
    'Đá',
    'Đánh, tát',
    'Ôm, vật lộn'
]

VIDEO_LABELS = [
    [1, 0, 0],
    [0, 1, 0],
    [0, 0, 1],
]

NUM_CLASSIFY = len(VIDEO_NAMES)

######################## end config ##############################

# dinh nghia VGG16 Model
def fun_getVGG16Model():
    modelCNN = VGG16(include_top=True, weights='imagenet')
    modelCNN.summary()
    transferLayer = modelCNN.get_layer(name='fc2')
    imgModelTransfer = Model(inputs=modelCNN.input, outputs=transferLayer.output)
    return imgModelTransfer

# One hot
def fun_onesHotLabel(label: list):
  _ones = np.ones([NUM_FRAME_INPUT_LSTM, NUM_CLASSIFY])
  _onesHot = label * _ones
  return np.array(_onesHot)

# Danh nhan video
def fun_getVideoLabelNames_EachFolder(path: str):
    names = []
    labels = []

    for fol in VIDEO_NAMES:
        folder = path + '/' + fol
        fileNames = lib.fun_getFileNames(path=folder)
        index = VIDEO_NAMES.index(fol)
        for file in fileNames:
            names.append('/' + fol + '/' + file)
            labels.append(VIDEO_LABELS[index])

    c = list(zip(names, labels))
    shuffle(c)

    names, labels = zip(*c)
    return names, labels

# nem 20 frame hinh vao VGG16 Model
def fun_getTransferValue(pathVideoOrListFrame, modelVGG16):
    if isinstance(pathVideoOrListFrame, str):
        frames = lib.fun_getFramesOfVideo(path=pathVideoOrListFrame, count=NUM_FRAME_INPUT_LSTM)
    else:
        frames = pathVideoOrListFrame

    frames = lib.fun_resizeFrames(frames=frames, size=SIZE)

    frames = np.array(frames)
    frames = (frames / 255.).astype(np.float16)

    transfer = modelVGG16.predict(frames)
    return transfer

# chuan bi tap du lieu + nhan de train lstm
def fun_getTrainSet_LabelSet(numItem: int, modelVGG16, names, labels, mess: str= 'Train'):
    count = 0
    trainSet = []
    labelSet = []
    while count < numItem:
        itemTrain = fun_getTransferValue(pathVideoOrListFrame=DIR_INPUT_TRAIN + names[count], modelVGG16= modelVGG16)
        itemLable = fun_onesHotLabel(label=labels[count])

        trainSet.append(itemTrain)
        labelSet.append(itemLable[0])

        lib.fun_print_process(count=count, max=numItem, mess='Video frame throw into VGG16 Model Processing {0}: '.format(mess))

        count += 1

    return trainSet, labelSet

# Dinh nghia mang LSTM
def fun_getModelLSTM(rnn_size: int = 512, input_shape: tuple = (20, 4096), num_classify: int = 3):
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

# bat dau cong viec train lstm
def fun_START_TRAINT_LSTM(modelVGG16, modelLSTM, trainSet, labelSet):
    valName, valLabel = fun_getVideoLabelNames_EachFolder(path= DIR_INPUT_VALIDATION)
    valSet, valLabelSet = fun_getTrainSet_LabelSet(numItem= len(valName),
                                                   modelVGG16= modelVGG16,
                                                   names= valName, labels= valLabel,
                                                   mess= 'Validation')
    history = modelLSTM.fit(np.array(trainSet), np.array(labelSet), epochs=EPOCH,
                        validation_data=(np.array(valSet), np.array(valLabelSet)),
                        batch_size=BATCH_SIZE, verbose=2)
    lib.fun_print(name= 'LSTM Train', value= 'Train Finish!')
    return history

# Show bieu do hoi tu
def fun_showAnalysis(history):
    plt.plot(history.history['accuracy'])
    plt.plot(history.history['val_accuracy'])
    plt.title('model accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train', 'validation'], loc='upper left')
    plt.savefig('destination_path.eps', format='eps', dpi=1000)
    plt.show()
    # summarize history for loss
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'validation'], loc='upper left')
    plt.savefig('destination_path1.eps', format='eps', dpi=1000)
    plt.show()

def fun_loadModelLSTM():
    modelLSTM = fun_getModelLSTM(num_classify= NUM_CLASSIFY)
    modelLSTM.load_weights(filepath= DIR_MODEL_LSTM)
    return modelLSTM

def fun_evaluate(modelLSTM, testSet, testLabelSet):
    result = modelLSTM.evaluate(np.array(testSet), np.array(testLabelSet))
    for name, value in zip(modelLSTM.metrics_names, result):
        print(name, value)