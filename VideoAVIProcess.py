from models import PublicModules as lib
import os

DIR_INPUT = 'D:\\08DHTH1\\1.Luan An\\TaiLieu\\CNN_LSTM_Code\\Data\\Thay_17_10_2020\\DuLieu_Train_Thay_Ha\\Du lieu bao luc-20201017T152839Z-002\\PhanChia_ThanhVien_23_10_2020\\Train\\'

DIR_OUTPUT = 'C:\\Users\\VIETSACLO-PC\\Desktop\\out\\'

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

count1 = 0
count2 = 0

for fd in VIDEO_NAMES:
    folder = DIR_INPUT + fd
    fileNames = lib.fun_getFileNames(path= folder)
    max1 = len(VIDEO_NAMES)
    max2 = len(fileNames)
    for filename in fileNames:
        if str(filename).endswith('.avi'):
            continue
        pathSave = DIR_OUTPUT + fd
        if not os.path.exists(pathSave):
            os.makedirs(pathSave)
        pathSave = pathSave + '\\' + filename[0: len(filename) - 4] + '.avi'
        frames = lib.fun_getFramesOfVideo_ALL(path= folder + '\\' + filename)
        lib.fun_saveFramesToVideo(frames= frames, path= pathSave, fps= 30)
        count2 += 1

        lib.fun_print_process(count=count1, max=max1)
        lib.fun_print_process(count= count2, max= max2)

    count1 += 1