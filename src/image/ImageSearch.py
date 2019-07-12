import cv2
import numpy
import numpy as np


def mutl_match(search_pic, template_pic, threshold, debug=False):
    """
    图像搜索，在目标图上找到相似的指定图片,多图像匹配
    :param debug:
    :param search_pic:
    :param template_pic:
    :param threshold:
    :return:
    """
    img_rgb = cv2.imread(search_pic)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(template_pic, 0)
    w, h = template.shape[::-1]  # rows->h, cols->w
    # 相关系数匹配方法：cv2.TM_CCOEFF
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)  # 匹配程度大于%80的坐标y,x
    for pt in zip(*loc[::-1]):  # *号表示可选参数
        cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (7, 249, 151), 2)
    if debug:
        cv2.imshow('Detected', img_rgb)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    return


def best_match(search_pic, template_pic, threshold, debug=False):
    """
    图像搜索，在目标图上找到相似的指定图片，匹配度最高的位置
    :param threshold:
    :param debug:
    :param search_pic:
    :param template_pic:
    :return:
    """
    # search_pic = cv2.imread(search_pic)
    # template_pic = cv2.imread(template_pic,0)
    img_gray = cv2.cvtColor(search_pic, cv2.COLOR_BGR2GRAY)
    w, h = template_pic.shape[::-1]  # rows->h, cols->w
    # 相关系数匹配方法：cv2.TM_CCOEFF

    # 平方差匹配CV_TM_SQDIFF：用两者的平方差来匹配，最好的匹配值为0
    # 归一化平方差匹配CV_TM_SQDIFF_NORMED
    # 相关匹配CV_TM_CCORR：用两者的乘积匹配，数值越大表明匹配程度越好
    # 归一化相关匹配CV_TM_CCORR_NORMED
    # 相关系数匹配CV_TM_CCOEFF：用两者的相关系数匹配，1
    # 表示完美的匹配，-1
    # 表示最差的匹配
    # 归一化相关系数匹配CV_TM_CCOEFF_NORMED
    res = cv2.matchTemplate(img_gray, template_pic, cv2.TM_CCOEFF)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    left_top = max_loc  # 左上角
    right_bottom = (left_top[0] + w, left_top[1] + h)  # 右下角
    if debug:
        cv2.rectangle(search_pic, left_top, right_bottom, 255, 2)  # 画出矩形位置
        cv2.imshow('Detected', search_pic)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    return left_top, right_bottom


def get_img_opencv(screenshot_bytes, _width, _height):
    im_opencv = numpy.frombuffer(screenshot_bytes, dtype='uint8')
    im_opencv.shape = (_height, _width, 4)
    return im_opencv


def read_img(template_pic, flag=-1):
    if flag == -1:
        return cv2.imread(template_pic)
    else:
        return cv2.imread(template_pic, 0)


def lookup_pos(template_pic, search_pic):
    img_rgb = cv2.imread(search_pic)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    img = img_gray
    template = cv2.imread(template_pic, 0)
    w, h = template.shape[::-1]

    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.95
    loc = np.where(res >= threshold)
    num = 0
    left = 0
    top = 0

    pos_list = []
    for pt in zip(*loc[::-1]):
        cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
        left = pt[0]
        top = pt[1]
        pos_list.append(pt)
        num = num + 1

    res = res * 256
    # cv2.imwrite(r'.\tmp_output\out.png', img_rgb)
    # cv2.imwrite(r'.\tmp_output\res.png', res)
    cv2.cvtColor(res, cv2.COLOR_BGRA2RGB)
    cv2.imwrite("im_opencv.jpg", res, [int(cv2.IMWRITE_JPEG_QUALITY), 100])  # 保存
    cv2.namedWindow('im_opencv')  # 命名窗口
    cv2.imshow("im_opencv", res)  # 显示
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return num, w, h, pos_list


if __name__ == '__main__':
    best_match(read_img(u"../../resource/img/im_opencv.jpg"), read_img(u"../../resource/img/tansuo.png", 0))
