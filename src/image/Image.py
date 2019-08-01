import cv2


def read_img(template_pic, flag=-1):
    if flag == -1:
        return cv2.imread(template_pic)
    else:
        return cv2.imread(template_pic, 0)


def get_img_opencv(screenshot_bytes, _width, _height, debug=False):
    import numpy
    im_opencv = numpy.frombuffer(screenshot_bytes, dtype='uint8')
    im_opencv.shape = (_height, _width, 4)
    if im_opencv.max() == 0 and im_opencv.min() == 0:
        raise Exception("截取屏幕失败")
    if debug:
        cv2.imshow('Detected', im_opencv)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    return im_opencv


def resize_by_zoom(zoom, image):
    if zoom != 1:
        height, width = image.shape[:2]
        return cv2.resize(image, (int(width * zoom), int(height * zoom)), interpolation=cv2.INTER_CUBIC)
    else:
        return image
