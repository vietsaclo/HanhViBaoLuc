from keras.layers import TimeDistributed, Dense, Dropout
from keras.layers import Conv2D, BatchNormalization, MaxPool2D, GlobalMaxPool2D, LSTM
import keras
from Modules import PublicModules as libs
import numpy as np
import cv2
import tensorflow as tf
from keras.preprocessing import image

VIDEO_NAMESs = [
    'bc',
    'cq',
    'da',
]

NUM_CLASSIFY = len(VIDEO_NAMESs)

def build_convnet(shape=(112, 112, 3)):
    momentum = .9
    model = keras.Sequential()
    model.add(Conv2D(64, (3,3), input_shape=shape,
        padding='same', activation='relu'))
    model.add(Conv2D(64, (3,3), padding='same', activation='relu'))
    model.add(BatchNormalization(momentum=momentum))
    
    model.add(MaxPool2D())
    
    model.add(Conv2D(128, (3,3), padding='same', activation='relu'))
    model.add(Conv2D(128, (3,3), padding='same', activation='relu'))
    model.add(BatchNormalization(momentum=momentum))
    
    model.add(MaxPool2D())
    
    model.add(Conv2D(256, (3,3), padding='same', activation='relu'))
    model.add(Conv2D(256, (3,3), padding='same', activation='relu'))
    model.add(BatchNormalization(momentum=momentum))
    
    model.add(MaxPool2D())
    
    model.add(Conv2D(512, (3,3), padding='same', activation='relu'))
    model.add(Conv2D(512, (3,3), padding='same', activation='relu'))
    model.add(BatchNormalization(momentum=momentum))
    
    # flatten...
    model.add(GlobalMaxPool2D())
    return model

def action_model(shape=(20, 112, 112, 3), nbout= NUM_CLASSIFY):
    # Create our convnet with (112, 112, 3) input shape
    convnet = build_convnet(shape[1:])
    
    # then create our final model
    model = keras.Sequential()
    # add the convnet with (5, 112, 112, 3) shape
    model.add(TimeDistributed(convnet, input_shape=shape))
    # here, you can also use GRU or LSTM
    model.add(LSTM(64))
    # and finally, we make a decision network
    model.add(Dense(1024, activation='relu'))
    model.add(Dropout(.5))
    model.add(Dense(512, activation='relu'))
    model.add(Dropout(.5))
    model.add(Dense(128, activation='relu'))
    model.add(Dropout(.5))
    model.add(Dense(64, activation='relu'))
    model.add(Dense(nbout, activation='softmax'))
    return model

model = action_model()
model.load_weights('Modules/GRU_TIME_DES.h5')

modelCNN = build_convnet()
modelCNN.summary()

frames = libs.fun_getFramesOfVideo(path= 'E:/TongHopDataKhoaLuan/[DATA SUA LAI]/[HopLe]/cq/003_[out_large_15].avi', count= 20)
frames = libs.fun_resizeFrames(frames= frames, size= (112, 112))
imgs = []
for f in frames:
    img = image.array_to_img(f)
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)

    images = np.vstack([x])
    imgs.append(images)

imgs = np.array(imgs)
print(imgs.shape)

# print(type(frames[0]))

# frames = libs.fun_resizeFrames(frames= frames, size= (112, 112))

# imgs = []
# for f in frames:
#     RGB_img = cv2.cvtColor(f, cv2.COLOR_BGR2RGB)
#     res = cv2.resize(RGB_img, dsize=(112, 112),
#                         interpolation=cv2.INTER_CUBIC)
#     imgs.append(res)

# resul = np.array(imgs)
# # resul = (resul / 255.).astype(np.float32)
# print(resul.shape)
# print(model.layers[0].input_shape)

# arrs = []
# arrs.append(resul)
# arrs = np.array(arrs)
# print(arrs.shape)

# # imgs = []
# # for f in arr:
# #     RGB_img = cv2.cvtColor(f, cv2.COLOR_BGR2RGB)
# #     res = cv2.resize(RGB_img, dsize=(112, 112),
# #                         interpolation=cv2.INTER_CUBIC)
# #     imgs.append(res)

# # arrs = []
# # arrs.append(imgs)
# # arrs = np.array(arrs)
# # print(arrs.shape)

real = model.predict(imgs)
pre = np.argmax(real)

# print(b.shape)
print(real)
print(pre)