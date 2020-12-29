from Modules import PublicModules as lib
import os
import cv2

SO_LAN_CAT_VIDEO = '7'
ID_NGUOICAT = '1'

DIR_INPUT = 'D:/[KhoaLuan] Violence Detection/SuuTam/cqa_Lan2_001_out'
DIR_INPUT_LARGE = 'D:/[TMP]/DataViolence 2'
DIR_INPUT_VDGOC = 'D:\\[LuanAn_BaoLuc2]\\4_TMP\\NguyenVanHieuLan1\\video'

DIR_OUTPUT = 'D:/[TMP]/DataViolence 2_out'
DIR_OUTPUT_LARGE = 'F:/TongHopDataKhoaLuan/3_KetQuaChuanHoa/out_video_large'
DIR_OUTPUT_VDGOC = 'D:\\[LuanAn_BaoLuc2]\\3_KetQuaChuanHoa\\video_goc'

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

    return result


def fun_getVideoName(videoName: str):
    idStart = videoName.index('_')
    tmp = videoName[idStart + 1]
    result = ''
    while tmp != '.':
        result += tmp
        idStart += 1
        tmp = videoName[idStart + 1]
    return result


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
    fileNames = lib.fun_getFileNames(path=pathIn)
    max = len(fileNames)
    for fileName in fileNames:
        prefixName = fileName[0:2]
        fdOut = pathOut + '\\' + prefixName
        if not os.path.exists(fdOut):
            os.makedirs(fdOut)
        frames = lib.fun_getFramesOfVideo_ALL(path=pathIn + '\\' + fileName)
        lib.fun_saveFramesToVideo(frames=frames, path=fdOut + '\\' + fileName[0: len(fileName) - 4] + '.avi')
        lib.fun_print_process(count=count, max=max)
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


def fun_danhLaiIDChoVideo(DIR_INPUT: str, DIR_OUTPUT: str, DIR_OUTPUT_LARGE: str, IS_RESIZE: bool = True):
    # Validate
    if not os.path.exists(DIR_INPUT):
        os.makedirs(DIR_INPUT)
    if not os.path.exists(DIR_OUTPUT):
        os.makedirs(DIR_OUTPUT)
    if not os.path.exists(DIR_OUTPUT_LARGE):
        os.makedirs(DIR_OUTPUT_LARGE)

    # ID = START_ID
    filesName = lib.fun_getFileNames(path=DIR_INPUT)
    count = 1  # For calculator progress
    max = len(filesName)  # For calculator progress
    for file in filesName:
        HD = fun_getHanhDong(videoName=file)  # HD = Hanh Dong contain[da, dn, nt...]
        IDVID = fun_getID(videoName=file)
        TENVID = fun_getVideoName(file)
        nameVideoIn = DIR_INPUT + '\\' + file
        nameVideoOut = '{0}\\{1}{2}_{3}_{4}.avi'.format(DIR_OUTPUT, HD, IDVID, SO_LAN_CAT_VIDEO, TENVID)
        nameVideoOut_large = '{0}\\{1}{2}_{3}_{4}.avi'.format(DIR_OUTPUT_LARGE, HD, IDVID, SO_LAN_CAT_VIDEO, TENVID)
        # ID += 1

        frames = lib.fun_getFramesOfVideo_ALL(path=nameVideoIn)
        if IS_RESIZE:
            frames = lib.fun_resizeFrames(frames=frames, size=DEFAULT_SIZE_VIDEO)
        isSave = lib.fun_saveFramesToVideo(frames=frames, path=nameVideoOut, fps=30)
        if not isSave:
            lib.fun_print(name='Save video' + nameVideoIn, value='Error!')
        elif len(frames) >= 60:
            lib.fun_saveFramesToVideo(frames=frames, path=nameVideoOut_large, fps=30)

        lib.fun_print_process(count=count, max=max, mess='Progress Video Output ID: ')
        count += 1


def fun_danhLaiIDChoVideoGoc(DIR_INPUT, DIR_OUTPUT):
    # Validate
    if not os.path.exists(DIR_INPUT):
        print('Folder VideoGoc is not existing!!')
    if not os.path.exists(DIR_OUTPUT):
        print('Folder OUT VideoGoc is not existing!!')

    filesName = lib.fun_getFileNames(path=DIR_INPUT)
    count = 0  # For calculator progress
    max = len(filesName)  # For calculator progress

    for file in filesName:
        nameVideoIn = DIR_INPUT + '\\' + file
        nameVideoOut = '{0}\\{1}_{2}_{3}.avi'.format(DIR_OUTPUT, ID_NGUOICAT, SO_LAN_CAT_VIDEO, file[0:len(file) - 4])

        frames = lib.fun_getFramesOfVideo_ALL(path=nameVideoIn)
        lib.fun_saveFramesToVideo(frames=frames, path=nameVideoOut, fps=30)

        lib.fun_print_process(count=count, max=max, mess='Processing VideoGOC ID: ')
        count += 1


def fun_read_START_ID(path: str) -> int:
    try:
        file = open(path, mode='r')
        id = int(file.read())
        file.close()
        return id
    except:
        lib.fun_print(name='read file: ' + path, value='Error To Read FileInput from path!')
        return -1


def fun_write_START_ID(path: str, START_ID) -> bool:
    try:
        file = open(path, mode='w+')
        file.write(str(START_ID))
        file.close()
        return True
    except:
        lib.fun_print(name='Write file: ' + path, value='Error To Write FileInput from path!')
        return False


def fun_resizeVideos(pathLoad: str, dirSave: str, size: tuple = (224, 224)):
    count = 1000
    max = 1832
    filenames = lib.fun_getFileNames(path=pathLoad)
    for file in filenames:
        frames = lib.fun_getFramesOfVideo_ALL(path=pathLoad + '/' + file)

        frames = lib.fun_resizeFrames(frames=frames, size=size)
        fileSave = '{0}.avi'.format(count)
        isSave = lib.fun_saveFramesToVideo(frames=frames, path=dirSave + '/' + fileSave)
        if isSave:
            count += 1
        lib.fun_print_process(count=count, max=max, mess='Resize Video Processing: ')


def fun_renameFiles(pathLoad: str):
    count = 1000
    max = 1832
    filenames = lib.fun_getFileNames(path=pathLoad)
    for file in filenames:
        fileSave = '{0}.avi'.format(count)
        os.renames(old=pathLoad + '/' + file, new=pathLoad + '/' + fileSave)
        count += 1
        lib.fun_print_process(count=count, max=max, mess='Rename Video Processing: ')


def fun_getVideoNameOriganal(nameVideoOut: str):
    start = nameVideoOut.find('_')
    end = nameVideoOut.rfind('_')
    return nameVideoOut[start + 1:end]


def fun_mapTimeToFrameIndex(time: str):
    times = time.split(':')
    index = int(times[1]) * 1800 + int(times[2]) * 30 + int(times[3])
    return index


def autoCutVideo(dirInput: str ,pathSave: str, fps: int = 30):
    file = open(file='FileInput/input.txt', mode='r')
    incree = 1
    recored = file.readlines()
    max = len(recored)
    old = ''
    frames = []
    for line in recored:
        if line is None:
            break
        full = line.split(';')
        name = full[0]
        time = full[1]
        nameOriganal = fun_getVideoNameOriganal(nameVideoOut=name)
        index = fun_mapTimeToFrameIndex(time=time)
        path = '{0}/{1}.avi'.format(dirInput, nameOriganal)
        if old != nameOriganal:
            old = nameOriganal
            frames = lib.fun_getFramesOfVideo_ALL(path=path)
        isSave = lib.fun_saveFramesToVideo(frames= frames[index:index+30],path='{0}/{1}.avi'.format(pathSave, name), fps= 30)
        if not isSave:
            lib.fun_print('save video: {0}'.format(name), value= 'Error')
        lib.fun_print_process(count= incree, max= max, mess= 'Video Auto Cut Processing: ')
        incree += 1

    file.close()

def fun_renameVideoOut(pathLoad: str):
    incree = 1
    filenames = lib.fun_getFileNames(path=pathLoad)
    max = len(filenames)
    for file in filenames:
        HD = fun_getHanhDong(videoName= file)
        ID = fun_getID(videoName= file)
        TENVID = fun_getVideoName(videoName= file)
        replace = '{0}_{1}_{2}_{3}.avi'.format(HD, ID, SO_LAN_CAT_VIDEO, TENVID)
        os.replace(src= pathLoad + '\\' + file, dst= pathLoad + '\\' + replace)
        lib.fun_print_process(count=incree, max=max, mess='Rename Video Processing: ')
        incree += 1

def fun_TMP_Rename(dirInput: str):
    fileNames = lib.fun_getFileNames(path= dirInput)
    for file in fileNames:
        hd = file[0:2]
        name = file[2:]
        name = hd + '8_7_' + name
        os.renames(old= dirInput + '/' + file, new= dirInput + '/' + name)

def fun_saveVideoToImages(dirVideo: str, pathSave: str):
    fileNames = lib.fun_getFileNames(dirVideo)
    incree = 1
    max = len(fileNames)
    print(max)
    for file in fileNames:
        countImage = 0
        prefix = file[0:len(file) - 4]
        frames = lib.fun_getFramesOfVideo(path= dirVideo + '/' + file)
        for frame in frames:
            cv2.imwrite(pathSave + '/' + prefix + '_'+str(countImage) + '.jpg', frame)
            countImage += 1
        lib.fun_print_process(count= incree, max= max,)
        incree += 1

if __name__ == '__main__':
    # fun_danhLaiIDChoVideoGoc(DIR_INPUT=DIR_INPUT_VDGOC, DIR_OUTPUT=DIR_OUTPUT_VDGOC)
    # fun_danhLaiIDChoVideo(DIR_INPUT=DIR_INPUT, DIR_OUTPUT=DIR_OUTPUT, DIR_OUTPUT_LARGE=DIR_OUTPUT_LARGE, IS_RESIZE=True)

    # filesLarge = lib.fun_getFileNames(path= DIR_INPUT_LARGE)
    # max = len(filesLarge)
    # count = 1
    # for file in filesLarge:
    #     lib.fun_outListVideoWithNumFrame(
    #         dirInput=DIR_INPUT_LARGE,
    #         fileName=file,
    #         dirToSave=DIR_OUTPUT,
    #         isShowCalculating=True,
    #         isResize= True
    #     )
    #     count += 1
    #     lib.fun_print_process(count= count, max= max, mess= 'ALL PROCESS: ')

    # fun_resizeVideos(pathLoad= 'D:/[KhoaLuan] Violence Detection/SuuTam/QuayClipLanCuoi', dirSave= 'D:/[KhoaLuan] Violence Detection/SuuTam/QuayClipLanCuoi_Resize')
    # fun_renameFiles(pathLoad= 'D:/[KhoaLuan] Violence Detection/SuuTam/QuayClipLanCuoi_Resize')
    # autoCutVideo(dirInput= 'F:/TongHopDataKhoaLuan/1_ThuCong/Lan7/NguyenCongTanLan7/video',
    # pathSave= 'F:/TongHopDataKhoaLuan/1_ThuCong/Lan7/NguyenCongTanLan7/out_tmp')

    # fun_renameVideoOut(pathLoad= DIR_INPUT)

    # fun_TMP_Rename(dirInput= 'F:/TongHopDataKhoaLuan/1_ThuCong/Lan6/NgoHuyThangLan6-001/video_out')
    fun_saveVideoToImages(dirVideo= 'F:/tmp', pathSave= 'F:/imgs')