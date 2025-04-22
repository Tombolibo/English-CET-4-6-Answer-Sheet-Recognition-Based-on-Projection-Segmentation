import cv2
import numpy as np

#投影分割，返回shape为(组、起点、终点）的array, minSep，组间最小间隔（连续0达到就视为下一组）， eps视为空的最小值
def extract_projection_coordinates(projection, minSep = 50, eps = 0, endBias = 0, minLength=0, maxLength = 5000)->np.array:
    maxVal = np.max(projection)
    start = None
    end = None
    AllPoints = []
    cnt0 = 0
    for i,projectioni in enumerate(projection):
        if projectioni<=eps*maxVal or i==len(projection)-1:
            cnt0+=1
            #如果0个个数达到阈值
            if start is not None and end is not None and (end-start>=minLength) and (cnt0>=minSep or i==len(projection)-1 or (end-start)>=maxLength):
                AllPoints.append([start, end+endBias])
                cnt0 = 0
                start = None
                end = None
        else:
            cnt0 = 0
            if start is None:
                start = i
            end = i
    return np.array(AllPoints, dtype = np.int32)


#处理一个选择题区块（5个题+-）
def process_block(img, withinVerticalDis = 0.26, withinHorizontalDis = 0.1, eps = 0.15, fillingConf=0.75, minChoiceSep = 5, maxChoiceSep = 200):
    imgShow = img.copy()
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    t, img = cv2.threshold(img, -1,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)  # 自动阈值，留下ABCD
    # t, img = cv2.threshold(img, 50 ,255,cv2.THRESH_BINARY_INV)  # 手动阈值

    k = np.ones((3,3), dtype=np.uint8)
    img = cv2.morphologyEx(img, cv2.MORPH_CLOSE,k,None, (-1,-1), 1)
    # cv2.imshow('thresh result', img)
    # cv2.waitKey(0)
    answers = []
    mask = np.zeros(img.shape, dtype=np.uint8)
    horizontalHistData = np.sum(img, axis = 1)
    verticalHistData = np.sum(img, axis = 0)
    horizontalGroups = extract_projection_coordinates(horizontalHistData, withinHorizontalDis*img.shape[0]/5, 0.15)
    verticalGroups = extract_projection_coordinates(verticalHistData, withinVerticalDis*img.shape[0]/5, eps,0, minChoiceSep, maxChoiceSep)
    #对于每一道题
    for i,hori in enumerate(horizontalGroups):
        #每一个选项
        answer = []
        for j,verj in enumerate(verticalGroups):
            if j==0:
                continue
            mask=mask*0
            pt1 = (verj[0],hori[0])
            pt2 = (verj[1],hori[1])
            cv2.rectangle(mask, pt1, pt2, 255, -1)

            cv2.rectangle(imgShow, pt1, pt2, (255,0,0), 3)
            #计算白色与矩形面积比
            pro = cv2.countNonZero(cv2.bitwise_and(img,mask ))/((verj[1]-verj[0])*(hori[1]-hori[0]))
            if pro>fillingConf:
                answer.append(chr(j-1+65))
        answers.append(answer)
    # cv2.imshow('Recognition result  ', imgShow)
    # cv2.waitKey(0)
    return answers, imgShow

def process_img(img, betweenVerticalDis = 0.1, betweenHorizontalDis = 0.05, withinVerticalDis = 0.265, withinHorizontalDis = 0.1, betweenEps = 0.3, withinEps=0.15, fillingConf=0.8, minChoiceSep = 5, maxChoiceSep = 200):
    choices = []
    objRects = []
    imgsrc = img.copy()
    #图像预处理
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.GaussianBlur(img, (5,5), 0)
    #imgThresh作为后续投影分组的基础
    t, imgThresh = cv2.threshold(img, -1, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    # 形态学封闭小孔
    k = np.ones((3,3), np.uint8)
    imgThresh = cv2.morphologyEx(imgThresh, cv2.MORPH_DILATE, k, None, (-1,-1), 1)

    #计算水平投影数据
    horizontalHistData = np.sum(imgThresh, axis = 1)
    #根据水平投影数据提取水平分组数据
    horizontalGroups = extract_projection_coordinates(horizontalHistData, betweenHorizontalDis*imgThresh.shape[0], betweenEps)
    #对于每一个水平分组计算垂直投影，并提取当前水平组下的垂直分组
    for i,horidatai in enumerate(horizontalGroups):
        verticalHistData = np.sum(imgThresh[horidatai[0]:horidatai[1], :], axis = 0)
        verticalGroups = extract_projection_coordinates(verticalHistData, betweenVerticalDis*imgThresh.shape[1],betweenEps)
        #对于每一个垂直和水平的交叉（一组）获取其两个矩形点
        for j,verdatai in enumerate(verticalGroups):
            blockResult = process_block(imgsrc[horidatai[0]:horidatai[1], verdatai[0]:verdatai[1]], withinVerticalDis,
                                        withinHorizontalDis, withinEps, fillingConf, minChoiceSep, maxChoiceSep)
            choices = choices+blockResult[0]
            objRects.append(blockResult[1])
    return choices,objRects
