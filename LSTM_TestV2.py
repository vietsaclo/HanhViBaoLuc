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
    names, labels = cf.fun_getVideoLabelNames_EachFolder(path=cf.DIR_INPUT_TEST)

    '''
        CHUAN BI TAP DU LIEU & NHAN DE TEST,
        - Mang LSTM duoc dinh nghia nhan vao 20 frame hinh,
        Moi hinh duoc cho qua VGG16 de lay mau ~ 4096
        - Vidu: 20 frame (224 x 224) ~ 20 * 4096 = [ [4096PhanTu],... [4096PhanTu] ]
    '''
    testSet, labelSet = cf.fun_getTrainSet_LabelSet(numItem=len(names), modelVGG16= modelVGG16, names= names, labels= labels)

    '''
        LOAD LSTM MODEL,
        - Hien tai minh load trong thu muc DIR_MODEL_LSTM config file
    '''
    modelLSTM = cf.fun_loadModelLSTM()

    '''
        DU DOAN % DO CHINH XAC,
        - Thu muc test tai: Data/Test/
    '''
    cf.fun_evaluate(modelLSTM= modelLSTM, testSet= testSet, testLabelSet= labelSet)