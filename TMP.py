from Modules import PublicModules as libs

frames1 = libs.fun_getFramesOfVideo(path= 'FileOutput/out.avi')

frames2 = libs.fun_getFramesOfVideo(path= 'FileOutput/out2.avi')

res = []
for x in frames1:
    res.append(x)

for x in frames2:
    res.append(x)

libs.fun_saveFramesToVideo(res, 'FileOutput/kq.avi')
print('fn')