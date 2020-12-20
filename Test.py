from Modules import PublicModules as libs
from Modules import LSTM_Config as cf

PATH = 'E:/TongHopDataKhoaLuan/[TrainQuaCacLan]'

names, labels = cf.fun_getVideoLabelNames_EachFolder(path= PATH)

incree = 1
max = len(names)
for name in names:
  cf.fun_FilterVideoFitFrameCount(fileName= PATH + name)
  libs.fun_print_process(count= incree, max= max, mess= 'Filter Process: ')
  incree += 1
