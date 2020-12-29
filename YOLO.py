
import time
import cv2
import argparse
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument('-i', '--image', required=True,
                help='path to input image')
ap.add_argument('-c', '--config', required=True,
                help='path to yolo config file')
ap.add_argument('-w', '--weights', required=True,
                help='path to yolo pre-trained weights')
ap.add_argument('-cl', '--classes', required=True,
                help='path to text file containing class names')
args = ap.parse_args()


def get_output_layers(net):
    layer_names = net.getLayerNames()

    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    return output_layers


def draw_prediction(img, class_id, confidence, x, y, x_plus_w, y_plus_h):
    label = str(classes[class_id])

    color = COLORS[class_id]

    cv2.rectangle(img, (x, y), (x_plus_w, y_plus_h), color, 2)

    cv2.putText(img, label, (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)


image = cv2.imread(args.image)
#image = cv2.imread('cam3.jpeg')

Width = image.shape[1]
Height = image.shape[0]
scale = 0.00392

classes = None

with open(args.classes, 'r') as f:
    classes = [line.strip() for line in f.readlines()]

COLORS = np.random.uniform(0, 255, size=(len(classes), 3))

net = cv2.dnn.readNet(args.weights, args.config)

blob = cv2.dnn.blobFromImage(image, scale, (416, 416), (0, 0, 0), True, crop=False)

net.setInput(blob)

outs = net.forward(get_output_layers(net))

class_ids = []
confidences = []
boxes = []
conf_threshold = 0.5
nms_threshold = 0.4

# Thực hiện xác định bằng HOG và SVM
start = time.time()

for out in outs:
    for detection in out:
        scores = detection[5:]
        class_id = np.argmax(scores)
        confidence = scores[class_id]
        if confidence > 0.5:
            center_x = int(detection[0] * Width)
            center_y = int(detection[1] * Height)
            w = int(detection[2] * Width)
            h = int(detection[3] * Height)
            x = center_x - w / 2
            y = center_y - h / 2
            class_ids.append(class_id)
            confidences.append(float(confidence))
            boxes.append([x, y, w, h])

indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)

index = 0
imgOriganal = image.copy()
imgsGet = []
for i in indices:
    i = i[0]
    box = boxes[i]
    x = box[0]
    y = box[1]
    w = box[2]
    h = box[3]
    draw_prediction(image, class_ids[i], confidences[i], round(x), round(y), round(x + w), round(y + h))
    if class_ids[i] == 0:
        y = int(y)
        yh = int(y + h)
        x = int(x)
        xw = int(x + w)
        img = imgOriganal[y:yh, x:xw]
        imgsGet.append([img, [y, yh, x, xw]])
    index+=1

# cv2.imshow("object detection", image)

image = image * 0
# cv2.imshow('adf', image)

def fun_sumWidthHeight(img):
    width, height, _ = img.shape
    return width + height

def fun_sort_desc(imgs):
    for i in range(0, len(imgs) -1):
        for j in range(i + 1, len(imgs)):
            sI = fun_sumWidthHeight(imgs[i][0])
            sJ = fun_sumWidthHeight(imgs[j][0])
            if sJ > sI:
                tmp = imgs[i]
                imgs[i] = imgs[j]
                imgs[j] = tmp

def fun_getY_YH_X_XW(yx):
    return yx[0], yx[1], yx[2], yx[3]

def fun_getTowImageLarge(imgs):
    fun_sort_desc(imgs)
    s1 = fun_sumWidthHeight(imgs[0][0])
    s2 = fun_sumWidthHeight(imgs[1][0])
    res = []
    res.append(imgs[0][0])
    if s1 - s2 < 40:
        res.append(imgs[1][0])

    for i in range(0, len(res)):
        y, yh, x, xw = fun_getY_YH_X_XW(imgs[i][1])
        image[y:yh, x:xw] = imgs[i][0]

def fun_blankFrame(imgs):
    for i in range(0, len(imgs)):
        y, yh, x, xw = fun_getY_YH_X_XW(imgs[i][1])
        image[y:yh, x:xw] = imgs[i][0]
        

# fun_getTowImageLarge(imgsGet)
fun_blankFrame(imgsGet)

cv2.imshow('final', image)


end = time.time()
print("YOLO Execution time: " + str(end-start))


cv2.waitKey()

cv2.imwrite("object-detection.jpg", image)
cv2.destroyAllWindows()
