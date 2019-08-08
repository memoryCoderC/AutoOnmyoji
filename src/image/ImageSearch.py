# coding=utf-8
from cv2 import cvtColor, COLOR_BGR2GRAY, matchTemplate, TM_CCOEFF_NORMED, rectangle, imshow, waitKey, \
    destroyAllWindows, minMaxLoc, imwrite
from numpy import where
from src.util.log import logger

"""
sift算法匹配
"""


# def sift_kp(image):
#     gray_image = cvtColor(image, COLOR_BGR2GRAY)
#     sift = xfeatures2d_SIFT.create()
#     kp, des = sift.detectAndCompute(image, None)
#     kp_image = drawKeypoints(gray_image, kp, None)
#     return kp_image, kp, des


# def get_good_match(des1, des2):
#     bf = BFMatcher()
#     matches = bf.knnMatch(des1, des2, k=2)
#     good = []
#     for m, n in matches:
#         if m.distance < 0.75 * n.distance:
#             good.append(m)
#     return good


# def siftImageAlignment(img1, img2):
#     _, kp1, des1 = sift_kp(img1)
#     _, kp2, des2 = sift_kp(img2)
#     good_match = get_good_match(des1, des2)
#     if len(good_match) > 4:
#         pts_a = np.float32([kp1[m.queryIdx].pt for m in good_match]).reshape(-1, 1, 2)
#         pts_b = np.float32([kp2[m.trainIdx].pt for m in good_match]).reshape(-1, 1, 2)
#         ransac_reproj_threshold = 4
#         H, status = findHomography(pts_a, pts_b, RANSAC, ransac_reproj_threshold);
#         img_out = warpPerspective(img2, H, (img1.shape[1], img1.shape[0]),
#                                       flags=INTER_LINEAR + WARP_INVERSE_MAP)
#     return img_out, H, status


def get_len(pos1, pos2):
    x = pos1[0] - pos2[0]
    y = pos1[1] - pos2[1]
    from math import sqrt
    return sqrt((x ** 2) + (y ** 2))


def filter_close(list, distance):
    result = list.copy()
    for item in list:
        for j in range(list.index(item) + 1, len(list)):
            pos1 = item[0]
            pos2 = list[j][0]
            if get_len(pos1, pos2) < distance:
                result.remove(item)
                break
    return result


def mutl_match(search_pic, template_pic, threshold, distance=5, debug=False):
    """
    图像搜索，在目标图上找到相似的指定图片,多图像匹配
    :param distance:
    :param debug:
    :param search_pic:
    :param template_pic:
    :param threshold:
    :return:
    """
    list = []
    img_gray = cvtColor(search_pic, COLOR_BGR2GRAY)
    w, h = template_pic.shape[::-1]  # rows->h, cols->w
    # 相关系数匹配方法：TM_CCOEFF
    res = matchTemplate(img_gray, template_pic, TM_CCOEFF_NORMED)
    loc = where(res >= threshold)  # 匹配程度大于%80的坐标y,x
    pos = [-10, -10]
    for pt in zip(*loc[::-1]):  # *号表示可选参数
        if get_len(pos, pt) > distance:
            list.append([pt, (pt[0] + w, pt[1] + h)])
        if debug:
            rectangle(search_pic, pt, (pt[0] + w, pt[1] + h), (7, 249, 151), 2)
        pos = pt
    if debug:
        imshow('Detected', search_pic)
        waitKey(0)
        destroyAllWindows()
    return filter_close(list, distance)


def best_match(search_pic, template_pic, threshold, debug=False):
    """
    图像搜索，在目标图上找到相似的指定图片，匹配度最高的位置
    :param threshold:
    :param debug:
    :param search_pic:
    :param template_pic:
    :return: x,y的元组
    """
    # search_pic = imread(search_pic)
    # template_pic = imread(template_pic,0)
    img_gray = cvtColor(search_pic, COLOR_BGR2GRAY)
    w, h = template_pic.shape[::-1]  # rows->h, cols->w
    # 相关系数匹配方法：TM_CCOEFF

    # 平方差匹配CV_TM_SQDIFF：用两者的平方差来匹配，最好的匹配值为0
    # 归一化平方差匹配CV_TM_SQDIFF_NORMED
    # 相关匹配CV_TM_CCORR：用两者的乘积匹配，数值越大表明匹配程度越好
    # 归一化相关匹配CV_TM_CCORR_NORMED
    # 相关系数匹配CV_TM_CCOEFF：用两者的相关系数匹配，1
    # 表示完美的匹配，-1
    # 表示最差的匹配
    # 归一化相关系数匹配CV_TM_CCOEFF_NORMED
    res = matchTemplate(img_gray, template_pic, TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = minMaxLoc(res)
    left_top = max_loc  # 左上角
    if max_val > threshold:
        right_bottom = (left_top[0] + w, left_top[1] + h)  # 右下角
        if debug:
            rectangle(search_pic, left_top, right_bottom, 255, 2)  # 画出矩形位置
            imshow('Detected', search_pic)
            imwrite("Copy.jpg", search_pic)
            waitKey(0)
            destroyAllWindows()
        return [left_top, right_bottom]
    return None
