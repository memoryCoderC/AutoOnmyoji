# coding=utf-8
from cv2 import imread, imshow, waitKey, destroyAllWindows, resize, INTER_CUBIC


def read_img(template_pic, flag=-1):
    if flag == -1:
        return imread(template_pic)
    else:
        return imread(template_pic, 0)


def get_img_opencv(screenshot_bytes, _width, _height, debug=False):
    import numpy
    im_opencv = numpy.frombuffer(screenshot_bytes, dtype='uint8')
    im_opencv.shape = (_height, _width, 4)
    if im_opencv.max() == 0 and im_opencv.min() == 0:
        raise Exception("截取屏幕失败")
    if debug:
        imshow('Detected', im_opencv)
        waitKey(0)
        destroyAllWindows()
    return im_opencv


def resize_by_zoom(zoom, image):
    if zoom != 1:
        height, width = image.shape[:2]
        return resize(image, (int(width * zoom), int(height * zoom)), interpolation=INTER_CUBIC)
    else:
        return image
