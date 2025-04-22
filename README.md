# English-CET-4-6-Answer-Sheet-Recognition-Based-on-Projection-Segmentation
# 基于投影分割的全国大学英语四六级模板答题卡识别，客观题识别，主观题提取，条形码信息识别。

## 说明
仅针对全国大学英语四六级答题卡模板有效，图片要求清晰大小固定，无异常比例划痕等（投影分析客观题识别较为严格），图片比例和项目中.pdf文件比例一致（模板统一），最好使用截图，如果无截图使用相机拍照，务必进行图像增强。

## 参数说明（图片合规使用项目默认参数即可）
创建识别器实例时，使用4张图片作为参数创建实例<br/>
实例创建后，使用set_answer_from_txt方法设置答案（txt文件按顺序标明各个客观题答案，不用写序号）<br/>
进行条形码、客观题、主观题（仅提取）的提取和识别：<br/>
:param betweenVerticalDis:   组间垂直距离（百分比形式）<br/>
:param betweenHorizontalDis:   组间水平距离（百分比形式）<br/>
:param withinVerticalDis:   组内垂直距离（百分比形式）<br/>
:param withinHorizontalDis:   组内水平距离（百分比形式）<br/>
:param betweenEps:   组间切分阈值（百分比形式）<br/>
:param withinEps:   组内切分阈值（百分比形式）<br/>
:param fillingConf:   认为涂色的面积占比阈值（涂色部分面积占矩形框面积的百分比）<br/>
:param minChoiceSep:   选项框最小宽度（像素）<br/>
:param maxChoiceSep:   选项框最大宽度（像素）<br/>

