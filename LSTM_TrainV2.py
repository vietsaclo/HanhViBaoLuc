from Modules import LSTM_Config as cf

if __name__ == '__main__':
    '''
        LOAD VGG16 MODEL,
        - Hien tai minh dung VGG16 model cua keras trong so = imagenet
    '''
    modelVGG16 = cf.fun_getVGG16Model()

    '''
        LAY TOAN BO VIDEO VA NHAN CUA TUNG VIDEO,
        - Truy cap vao thu muc DIR_INPUT_TRAIN lay toan bo file video va nhan bo vao mang.
        - Vidu: names[da1_1_111_001.avi,nt2_1_222_002.avi] ~ labels[ [1,0,0], [0,1,0] ]
    '''
    names, labels = cf.fun_getVideoLabelNames_EachFolder(path=cf.DIR_INPUT_TRAIN)

    print('len Train: ', len(names))
    input('any: ')

    '''
        CHUAN BI TAP DU LIEU & NHAN DE TRAIN LSTM,
        - Mang LSTM duoc dinh nghia nhan vao 20 frame hinh,
        Moi hinh duoc cho qua VGG16 de lay mau ~ 4096
        - Vidu: 20 frame (224 x 224) ~ 20 * 4096 = [ [4096PhanTu],... [4096PhanTu] ]
    '''
    trainSet, labelSet = cf.fun_getTrainSet_LabelSet(pathVideoOrListFrame=cf.DIR_INPUT_TRAIN
                                                     , numItem=len(names), modelVGG16= modelVGG16, names= names, labels= labels)

    '''
        LAY MODEL LSTM DUOC DINH NGHIA,
        - Chi tiet dinh nghia mang LSTM tai config file
    '''
    modelLSTM = cf.fun_getModelLSTM(num_classify= cf.NUM_CLASSIFY)
    modelLSTM.summary()

    '''
        BAT DAU HUAN LUYEN LSTM
    '''
    history = cf.fun_START_TRAINT_LSTM(modelVGG16= modelVGG16 ,modelLSTM= modelLSTM, trainSet= trainSet, labelSet= labelSet)

    '''
        SAVE MODEL LSTM VAO O DIA
    '''
    modelLSTM.save(cf.DIR_MODEL_LSTM)

    '''
        HIEN THI BIEU DO HOI TU
    '''
    cf.fun_showAnalysis(history= history)