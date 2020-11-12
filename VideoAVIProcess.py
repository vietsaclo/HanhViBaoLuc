from Modules import PublicModules as lib
import os
from time import sleep

SO_LAN_CAT_VIDEO = 'L01'

DIR_INPUT = 'D:\\[VIET-SACLO]\\TongHopDataKhoaLuan\\4_TMP\\out_video'

PATH_INPUT_START_ID = 'D:\\[VIET-SACLO]\\TongHopDataKhoaLuan\\0_Important\\START_ID.TXT'

DIR_OUTPUT = 'D:\\[VIET-SACLO]\\TongHopDataKhoaLuan\\3_KetQuaChuanHoa\\out_video'

DIR_OUTPUT_LARGE = 'D:\\[VIET-SACLO]\\TongHopDataKhoaLuan\\3_KetQuaChuanHoa\\out_video_large'

DEFAULT_SIZE_VIDEO = (224, 224)

VIDEO_NAMES = [
    'bc',
    'cq',
    'da',
    'dn',
    'kc',
    'lg',
    'lk',
    'na',
    'nc',
    'ne',
    'nt',
    'om',
    'tc',
    'vd',
    'vk',
    'xd',
    'xt'
]

def fun_getHanhDong(videoName: str):
    return videoName[0:2]

def fun_getID(videoName: str):
    vid = videoName[2:]
    idStart = 0
    result = ''
    tmp = vid[idStart]
    while tmp != '_':
        result += tmp
        idStart += 1
        tmp = vid[idStart]

    return 'ID'+result

def fun_getVideoName(videoName: str):
    idStart = videoName.index('_')
    idStart += 1
    tmp = videoName[idStart]
    result = ''
    while tmp != '_':
        result += tmp
        idStart += 1
        tmp = videoName[idStart]
    return 'T'+result

def chuanHoaToanBoVideoTrongTungThuMuc():
    count1 = 0
    count2 = 0

    for fd in VIDEO_NAMES:
        folder = DIR_INPUT + fd
        fileNames = lib.fun_getFileNames(path=folder)
        max1 = len(VIDEO_NAMES)
        max2 = len(fileNames)
        for filename in fileNames:
            if str(filename).endswith('.avi'):
                continue
            pathSave = DIR_OUTPUT + fd
            if not os.path.exists(pathSave):
                os.makedirs(pathSave)
            pathSave = pathSave + '\\' + filename[0: len(filename) - 4] + '.avi'
            frames = lib.fun_getFramesOfVideo_ALL(path=folder + '\\' + filename)
            lib.fun_saveFramesToVideo(frames=frames, path=pathSave, fps=30)
            count2 += 1

            lib.fun_print_process(count=count1, max=max1)
            lib.fun_print_process(count=count2, max=max2)

        count1 += 1

def xuatVideoVaoTungThuMuc(pathIn: str, pathOut: str):
    count = 0
    fileNames = lib.fun_getFileNames(path= pathIn)
    max = len(fileNames)
    for fileName in fileNames:
        prefixName = fileName[0:2]
        fdOut = pathOut + '\\' + prefixName
        if not os.path.exists(fdOut):
            os.makedirs(fdOut)
        frames = lib.fun_getFramesOfVideo_ALL(path= pathIn + '\\' + fileName)
        lib.fun_saveFramesToVideo(frames= frames, path= fdOut + '\\' + fileName[0: len(fileName) - 4] + '.avi')
        lib.fun_print_process(count= count, max= max)
        count += 1

'''
    Dinh nghia mot ham:
    input: list video
    output: list video duoc danh lai id theo so thu thu 1...n
    @:param: DIR_INPUT: str: path list video input
    @:param: DIR_INPUT_START_ID: path to read and save start id. video id identity
    @:param: DIR_OUTPUT: str: path list video duoc danh lai so id tu 1...n
    @:param: DIR_OUTPUT_LARGE: path list video duoc save lai khi nhung video >= 60 frames
    @:param: START_ID: int: ID bat dau danh. vi du: START_ID = 1, list video out se duoc danh tu 1...n
    @:param: IS_RESIZE: bool: co muon resize ve dang 224 X 224 default = true
'''
def fun_danhLaiIDChoVideo(DIR_INPUT: str,PATH_INPUT_START_ID: str, DIR_OUTPUT: str, DIR_OUTPUT_LARGE: str, START_ID: int, IS_RESIZE: bool= True):
    # Validate
    if not os.path.exists(DIR_INPUT):
        os.makedirs(DIR_INPUT)
    if not os.path.exists(DIR_OUTPUT):
        os.makedirs(DIR_OUTPUT)
    if not os.path.exists(DIR_OUTPUT_LARGE):
        os.makedirs(DIR_OUTPUT_LARGE)

    ID = START_ID
    filesName = lib.fun_getFileNames(path= DIR_INPUT)
    count = 0 # For calculator progress
    max = len(filesName) # For calculator progress
    for file in filesName:
        HD = fun_getHanhDong(videoName= file) # HD = Hanh Dong contain[da, dn, nt...]
        IDVID = fun_getID(videoName= file)
        TENVID = fun_getVideoName(file)
        nameVideoIn = DIR_INPUT + '\\' + file
        nameVideoOut = '{0}\\{1}_{2}_{3}_{4}_{5}.avi'.format(DIR_OUTPUT, HD, IDVID, SO_LAN_CAT_VIDEO, TENVID, ID)
        nameVideoOut_large = '{0}\\{1}_{2}_{3}_{4}_{5}.avi'.format(DIR_OUTPUT_LARGE, HD, IDVID, SO_LAN_CAT_VIDEO, TENVID, ID)
        ID += 1

        frames = lib.fun_getFramesOfVideo_ALL(path= nameVideoIn)
        if IS_RESIZE:
            frames = lib.fun_resizeFrames(frames= frames, size= DEFAULT_SIZE_VIDEO)
        isSave = lib.fun_saveFramesToVideo(frames= frames, path= nameVideoOut, fps= 30)
        if not isSave:
            lib.fun_print(name= 'Save video' + nameVideoIn, value= 'Error!')
        elif len(frames) >= 60:
            lib.fun_saveFramesToVideo(frames= frames, path= nameVideoOut_large, fps= 30)

        lib.fun_print_process(count= count, max= max, mess= 'Progress Video Output ID: ')
        count += 1

    fun_write_START_ID(path= PATH_INPUT_START_ID, START_ID= ID)
    print('\rMax ID: ', ID)

def fun_read_START_ID(path: str) -> int:
    try:
        file = open(path, mode='r')
        id = int(file.read())
        file.close()
        return id
    except:
        lib.fun_print(name= 'read file: '+path, value='Error To Read File from path!')
        return -1

def fun_write_START_ID(path: str, START_ID) -> bool:
    try:
        file = open(path, mode='w+')
        file.write(str(START_ID))
        file.close()
        return True
    except:
        lib.fun_print(name='Write file: '+path, value='Error To Write File from path!')
        return False

import tensorflow as tf

if __name__ == '__main__':
    #------------------- START ID VERY IMPORTANT--------------------
    START_ID = fun_read_START_ID(path= PATH_INPUT_START_ID)
    #---------------------------------------------------------------
    if START_ID != -1:
        fun_danhLaiIDChoVideo(DIR_INPUT= DIR_INPUT, PATH_INPUT_START_ID= PATH_INPUT_START_ID, DIR_OUTPUT= DIR_OUTPUT, DIR_OUTPUT_LARGE= DIR_OUTPUT_LARGE, START_ID= START_ID, IS_RESIZE= True)