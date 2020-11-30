import os
import cv2
import sys
import zipfile

def fun_print(name: str, value) -> None:
    print('@ Deep Learning> ', name)
    print(value)


def fun_getFileNames(path: str) -> list:
    return os.listdir(path)


def fun_showVideoPath(path: str, delay: int = 25) -> None:
    cap = cv2.VideoCapture(path)
    isContinue, frame = cap.read()
    while True:
        if not isContinue:
            break
        cv2.imshow('frame', frame)
        if cv2.waitKey(delay=delay) & 0xFF == ord('q'):
            break
        isContinue, frame = cap.read()

    cap.release()
    cv2.destroyAllWindows()


def fun_getFramesOfVideo(path: str, count: int = 20) -> list:
    cap = cv2.VideoCapture(path)
    isContinue, frame = cap.read()
    imgs = []
    while count > 0:
        if not isContinue:
            break
        imgs.append(frame)
        isContinue, frame = cap.read()
        count -= 1
    cap.release()
    cv2.destroyAllWindows()
    return imgs

def fun_getFramesOfVideo_ALL(path: str) -> list:
    cap = cv2.VideoCapture(path)
    isContinue, frame = cap.read()
    imgs = []
    while True:
        if not isContinue:
            break
        imgs.append(frame)
        isContinue, frame = cap.read()
    cap.release()
    cv2.destroyAllWindows()
    return imgs


def fun_showVideoFrames(frames: list, delay: int = 25) -> None:
    for frame in frames:
        cv2.imshow('frame', frame)
        if cv2.waitKey(delay=delay) & 0xFF == ord('q'):
            break


def fun_showVideo(source, delay: int = 25) -> None:
    if isinstance(source, str):
        fun_showVideoPath(path=source, delay=delay)
    else:
        fun_showVideoFrames(frames=source, delay=delay)


def fun_resizeFrames(frames: list, size: tuple = (224, 224)) -> list:
    imgs = []
    count = 0
    for frame in frames:
        try:
          fr = cv2.resize(frame, dsize=size)
          imgs.append(fr)
        except:
          print('\r!Error To Resize of {0}'.format(count))
        count += 1
    cv2.destroyAllWindows()
    return imgs


def fun_saveFramesToVideo(frames: list, path: str, fps: int = 30) -> bool:
    try:
        height, width, layer = frames[0].shape
        wr = cv2.VideoWriter(path, cv2.VideoWriter_fourcc(*'MJPG'), fps, (width, height))
        for frame in frames:
            wr.write(frame)
        wr.release()
        cv2.destroyAllWindows()
        return True

    except:
        fun_print(name='Write Video: '+path, value='ERROR TO WRITE VIDEO')
        return False

def fun_getSizeOfFrame(frame) -> tuple:
    height, width, layer = frame.shape
    return (width, height)

# version 1
def fun_outListVideoWithNumFrame(
        pathLoad: str,
        pathSave: str,
        countFrame: int,
        fps: int= 30
):


def fun_extractZipFile(pathFileZip: str, pathToSave: str) -> None:
    if not os.path.exists(pathToSave):
        os.makedirs(pathToSave)
    fun_print(name='Extract All ' + pathFileZip, value='Extracting...')
    if (pathFileZip.endswith('.zip')):
        zipfile.ZipFile(file=pathFileZip, mode='r').extractall(path=pathToSave)
        print('Extract Done')
    else:
        print('Please Input zip file')

def fun_print_process(count: int, max: int, mess: str = 'Processing: ') -> None:
  process = count / max
  mess = '\r - ' +  mess + ' [{0:.1%}]'.format(process)
  sys.stdout.write(mess)
  sys.stdout.flush()

def fun_makeCenter(win):
    """
        centers a tkinter window
        :param win: the main window or Toplevel window to center
        """
    win.update_idletasks()
    width = win.winfo_width()
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width = width + 2 * frm_width
    height = win.winfo_height()
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = win.winfo_screenwidth() // 2 - win_width // 2
    y = win.winfo_screenheight() // 2 - win_height // 2
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    win.deiconify()