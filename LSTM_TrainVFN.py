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
    
    print('len all: '+str(len(names)))
    input('any: ')

    print('len Train: ', len(names))
    input('any: ')

    '''
        CHUAN BI TAP DU LIEU & NHAN (lable) DE TRAIN LSTM,
        - Mang LSTM duoc dinh nghia nhan vao 20 frame hinh,
        Moi hinh duoc cho qua VGG16 de lay mau ~ 4096
        - Vidu: 20 frame (224 x 224) ~ 20 * 4096 = [ [4096PhanTu],... [4096PhanTu] ]
    '''
    trainSet, labelSet = cf.fun_getTrainSet_LabelSet_SaveFile(pathVideoOrListFrame=cf.DIR_INPUT_TRAIN
                                                     , numItem=len(names), modelVGG16= modelVGG16, names= names, labels= labels)

    # Load File Saved of Data after throw VGG16 Model
    # trainSet, labelSet = cf.fun_getTrainSet_LabelSet_LoadFile(numItem= 400 * 17)

    print('total [train, vald, test]: ', len(trainSet))
    input('any: ')

    NUM_TESTS = int(len(trainSet) * cf.TEST_PERCENT)

    # Init Test Set
    testSet = trainSet[0:NUM_TESTS]
    testLabelSet = labelSet[0:NUM_TESTS]

    # Init Train Set
    trainSet = trainSet[NUM_TESTS:]
    labelSet = labelSet[NUM_TESTS:]

    '''
        LAY MODEL LSTM DUOC DINH NGHIA,
        - Chi tiet dinh nghia mang LSTM tai config file
    '''
    modelLSTM = cf.fun_getModelLSTM_5(num_classify= cf.NUM_CLASSIFY)
    modelLSTM.summary()

    '''
        BAT DAU HUAN LUYEN LSTM
    '''
    history = cf.fun_START_TRAINT_LSTM_PERCENT_K_Fold(modelLSTM= modelLSTM, trainSet= trainSet, labelSet= labelSet, testSet= testSet, testLabelSet= testLabelSet)

    '''
        SAVE MODEL LSTM VAO O DIA
    '''
    modelLSTM.save(cf.DIR_MODEL_LSTM)

    '''
        HIEN THI BIEU DO HOI TU
    '''
    cf.fun_showAnalysis(history= history)
    
    #-----------------------
    
    print('Len Test: ' + str(len(testSet)))
    input('any: ')
    
    '''
        DU DOAN % DO CHINH XAC,
        - Thu muc test tai: Data/Test/
    '''
    cf.fun_evaluate(modelLSTM=modelLSTM, testSet=testSet, testLabelSet=testLabelSet)
