import cv2
import numpy as np
from pyzbar import pyzbar

import extraction

#该代码仅针对全国大学英语四级答题卡page
class AnswerSheeteRcognizer(object):
    def __init__(self, page1Path=None, page2Path=None,page3Path=None, page4Path=None):
        self._page1Path = page1Path
        self._page2Path = page2Path
        self._page3Path = page3Path
        self._page4Path = page4Path
        self._imgPage1 = None
        self._imgPage2 = None
        self._imgPage3 = None
        self._imgPage4 = None
        #第一页区块坐标，只需要提取，不需要识别（学号和条形码待完成）
        self._page1BarCodept1 = (0.26938, 0.17563)
        self._page1BarCodept2 = (0.47805, 0.25151)
        self._imgPage1BarCode = None
        self._page1BarCodeInfo = None

        self._page1IDpt1 = (0.50416, 0.086826)
        self._page1IDpt2 = (0.90616, 0.283437)
        self._imgPage1ID = None

        self._page1Articalpt1 = (0.04444, 0.35429)
        self._page1Articalpt2 = (0.89861, 0.89520)
        self._imgPage1Artical = None

        #第二页区块坐标
        self._page2Articalpt1 = (0.09722, 0.12674)
        self._page2Articalpt2 = (0.95277, 0.47504)
        self._imgPage2Artical = None

        self._page2Choicept1 = (0.12083, 0.59680)
        self._page2Choicept2 = (0.87777, 0.83632)
        self._imgPage2Choice = None

        #第三页区块坐标
        self._page3IDpt1 = (0.5000, 0.13772)
        self._page3IDpt2 = (0.8986, 0.28742)
        self._imgPage3ID = None

        self._page3Choicept1 = (0.11388, 0.34331)
        self._page3Choicept2 = (0.85138, 0.89121)
        self._imgPage3Choice = None

        #第四页分块数据
        self._page4Transpt1 = (0.09861, 0.16167)
        self._page4Transpt2 = (0.96555, 0.90019)
        self._imgPage4Trans = None

        #规定大小
        self._imgSize = (2880, 4000)
        #客观题答案
        self._objAnswers = []  # 客观题答案
        self._objChoice = []  # 客观题选项
        self._objGrade = []  # 客观题评分
        self._objRect = []  # 客观题矩形框
        #读取图片
        self.readImg()
        #提取区块
        self.extract_page1()
        self.extract_page2()
        self.extract_page3()
        self.extract_page4()


    #读取图片
    def readImg(self):
        if self._page1Path is not None:
            self._imgPage1 = cv2.imread(self._page1Path)
            self._imgPage1 = cv2.resize(self._imgPage1, self._imgSize)
        if self._page2Path is not None:
            self._imgPage2 = cv2.imread(self._page2Path)
            self._imgPage2 = cv2.resize(self._imgPage2, self._imgSize)
        if self._page3Path is not None:
            self._imgPage3 = cv2.imread(self._page3Path)
            self._imgPage3 = cv2.resize(self._imgPage3, self._imgSize)
        if self._page4Path is not None:
            self._imgPage4 = cv2.imread(self._page4Path)
            self._imgPage4 = cv2.resize(self._imgPage4, self._imgSize)

    #获得客观题答案
    @property
    def get_objective_anwsers(self):
        return self._objAnswers
    #设置客观题答案
    def set_objective_anwsers(self, ans):
        self._objAnswers = ans
    #新增客观题答案
    def add_objective_anster(self, ans):
        self._objAnswers.append(ans)
    #从txt文件设置答案
    def set_answer_from_txt(self, filePath):
        self._objAnswers = np.loadtxt(filePath, dtype=np.str_).reshape(-1,1)


    #处理第一页
    def extract_page1(self):
        idPt1 = (int(self._imgPage1.shape[1]*self._page1IDpt1[0]),
                 int(self._imgPage1.shape[0]*self._page1IDpt1[1]))

        idPt2 = (int(self._imgPage1.shape[1]*self._page1IDpt2[0]),
                 int(self._imgPage1.shape[0]*self._page1IDpt2[1]))
        self._imgPage1ID = self._imgPage1[idPt1[1]:idPt2[1], idPt1[0]:idPt2[0]].copy()
        barcodePt1 = (int(self._imgPage1.shape[1]*self._page1BarCodept1[0]),
                      int(self._imgPage1.shape[0]*self._page1BarCodept1[1]))
        barcodePt2 = (int(self._imgPage1.shape[1]*self._page1BarCodept2[0]),
                      int(self._imgPage1.shape[0]*self._page1BarCodept2[1]))
        self._imgPage1BarCode = self._imgPage1[barcodePt1[1]:barcodePt2[1], barcodePt1[0]:barcodePt2[0]].copy()

        # 条形码识别（EAN13）：文本，类型，矩形框，四顶点
        self._page1BarCodeInfo = pyzbar.decode(self._imgPage1BarCode, symbols=[pyzbar.ZBarSymbol.EAN13])[0]
        for point in self._page1BarCodeInfo[3]:
            cv2.circle(self._imgPage1BarCode, point, 10, (100,255,0), -1)

        articalPt1 = (int(self._imgPage1.shape[1]*self._page1Articalpt1[0]),
                      int(self._imgPage1.shape[0]*self._page1Articalpt1[1]))
        articalPt2 = (int(self._imgPage1.shape[1]*self._page1Articalpt2[0]),
                      int(self._imgPage1.shape[0]*self._page1Articalpt2[1]))
        self._imgPage1Artical = self._imgPage1[articalPt1[1]:articalPt2[1], articalPt1[0]:articalPt2[0]].copy()

    def extract_page2(self):
        articalPt1 = (int(self._imgPage2.shape[1]*self._page2Articalpt1[0]),
                      int(self._imgPage2.shape[0]*self._page2Articalpt1[1]))
        articalPt2 = (int(self._imgPage2.shape[1]*self._page2Articalpt2[0]),
                      int(self._imgPage2.shape[0]*self._page2Articalpt2[1]))

        self._imgPage2Artical = self._imgPage2[articalPt1[1]:articalPt2[1], articalPt1[0]:articalPt2[0]].copy()
        choicePt1 = (int(self._imgPage2.shape[1]*self._page2Choicept1[0]),
                     int(self._imgPage2.shape[0]*self._page2Choicept1[1]))
        choicePt2 = (int(self._imgPage2.shape[1]*self._page2Choicept2[0]),
                     int(self._imgPage2.shape[0]*self._page2Choicept2[1]))
        self._imgPage2Choice = self._imgPage2[choicePt1[1]:choicePt2[1], choicePt1[0]:choicePt2[0]].copy()


    def extract_page3(self):
        idPt1 = (int(self._imgPage3.shape[1]*self._page3IDpt1[0]),
                 int(self._imgPage3.shape[0]*self._page3IDpt1[1]))

        idPt2 = (int(self._imgPage3.shape[1]*self._page3IDpt2[0]),
                 int(self._imgPage3.shape[0]*self._page3IDpt2[1]))
        self._imgPage3ID = self._imgPage3[idPt1[1]:idPt2[1], idPt1[0]:idPt2[0]].copy()
        choicePt1 = (int(self._imgPage3.shape[1]*self._page3Choicept1[0]),
                     int(self._imgPage3.shape[0]*self._page3Choicept1[1]))
        choicePt2 = (int(self._imgPage3.shape[1]*self._page3Choicept2[0]),
                     int(self._imgPage3.shape[0]*self._page3Choicept2[1]))
        self._imgPage3Choice = self._imgPage3[choicePt1[1]:choicePt2[1], choicePt1[0]:choicePt2[0]].copy()

    def extract_page4(self):

        transPt1 = (int(self._imgPage4.shape[1]*self._page4Transpt1[0]),
                    int(self._imgPage4.shape[0]*self._page4Transpt1[1]))
        tranPt2 = (int(self._imgPage4.shape[1]*self._page4Transpt2[0]),
                   int(self._imgPage4.shape[0]*self._page4Transpt2[1]))
        self._imgPage4Trans = self._imgPage4[transPt1[1]:tranPt2[1], transPt1[0]:tranPt2[0]].copy()

    #判断区域1的选择题
    def judgeChoice(self, betweenVerticalDis = 0.1, betweenHorizontalDis = 0.05, withinVerticalDis = 0.265, withinHorizontalDis = 0.1,
                     betweenEps = 0.3, withinEps=0.15, fillingConf=0.8, minChoiceSep = 5, maxChoiceSep = 200):
        '''
        :param betweenVerticalDis:   组间垂直距离（百分比形式）
        :param betweenHorizontalDis:   组间水平距离（百分比形式）
        :param withinVerticalDis:   组内垂直距离（百分比形式）
        :param withinHorizontalDis:   组内水平距离（百分比形式）
        :param betweenEps:   组间切分阈值（百分比形式）
        :param withinEps:   组内切分阈值（百分比形式）
        :param fillingConf:   认为涂色的面积占比阈值（涂色部分面积占矩形框面积的百分比）
        :param minChoiceSep:   选项框最小宽度（像素）
        :param maxChoiceSep:   选项框最大宽度（像素）
        :return: (得分列表，实际填涂列表，正确答案列表)
        '''
        extractionResult = extraction.process_img(self._imgPage2Choice, betweenVerticalDis, betweenHorizontalDis, withinVerticalDis,
                               withinHorizontalDis,
                               betweenEps, withinEps, fillingConf, minChoiceSep, maxChoiceSep)
        firstChoiceResult = extractionResult[0]
        self._objRect+=extractionResult[1]

        extractionResult = extraction.process_img(self._imgPage3Choice, betweenVerticalDis, betweenHorizontalDis, withinVerticalDis,
                               withinHorizontalDis,
                               betweenEps, withinEps, fillingConf, minChoiceSep, maxChoiceSep)
        secondChoiceResult = extractionResult[0]
        self._objRect+=extractionResult[1]
        self._objChoice = firstChoiceResult+secondChoiceResult
        for i in range(len(self._objAnswers)):
            # 多选了
            if len(self._objChoice[i])>1:
                self._objGrade.append(0)
            # 漏选了
            elif len(self._objChoice[i])==0:
                self._objGrade.append(0)
            # 选对了
            elif self._objChoice[i][0] == self._objAnswers[i][0]:
                self._objGrade.append(1)
            # 选错了
            elif self._objChoice[i][0] != self._objAnswers[i][0]:
                self._objGrade.append(0)
        return (self._objGrade,self._objChoice, self._objAnswers)


if __name__ == '__main__':
    # 用四张答题卡图片初始化识别器
    rec = AnswerSheeteRcognizer(r'./card1/2/1.jpg', r'./card1/2/2.jpg',
                                 r'./card1/2/3.jpg', r'./card1/2/4.jpg')
    # 设置标准答案
    rec.set_answer_from_txt(r'C:\Users\LFK\OneDrive\Python_project\40例子\chap9答题卡识别\answers.txt')

    # 答题卡识别并返回检测客观题结果（会打印条形码信息和显示各个部分的图像）
    result = rec.judgeChoice(betweenVerticalDis = 0.1, betweenHorizontalDis = 0.05, withinVerticalDis = 0.3, withinHorizontalDis = 0.2,
                            betweenEps = 0.15, withinEps=0.12, fillingConf=0.7, minChoiceSep = 30, maxChoiceSep = 50)

    #======/================================展示处理结果=============================#
    print('题号 正误 选项 答案')
    for i in range(len(result[0])):
        print(i+1,": ", result[0][i], result[1][i], result[2][i])
    print('正确个数：', np.sum(result[0]))
    print('条形码信息：')
    for info in rec._page1BarCodeInfo:
        print(info)

    # ======================================附加内容=============================== #
    # 显示主观题部分
    cv2.namedWindow('sbj', cv2.WINDOW_NORMAL)
    sbjImg = [rec._imgPage1ID,rec._imgPage1BarCode, rec._imgPage1Artical, rec._imgPage2Artical, rec._imgPage4Trans]
    for img in sbjImg:
        cv2.imshow('sbj', img)
        cv2.waitKey(0)
    cv2.destroyAllWindows()
    # 显示客观题提取的部分
    cv2.namedWindow('obj', cv2.WINDOW_NORMAL)
    for img in rec._objRect:
        cv2.imshow('obj', img)
        cv2.waitKey(0)





