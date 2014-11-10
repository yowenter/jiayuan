信息源 --> 数据采集 --> 数据结构化 --> 数据清洗 -->数据转换 --> 模型训练　--> 发现知识

step1,信息源:http://www.jiayuan.com/。

step2,网站层级结构分析。

step3,根据结构,编写爬虫。 [jiayuan.py]

step4,解析网页,提取数据,并结构化。[parseHtml.py]

step5,制定规则,转换数据。[pdTransform.py]

step6,采用合适的算法模型进行训练,得到婚恋匹配模型。[marryModel.py]


details:

jiayuan.py:
网站一级结构：佳缘网晒幸福主页【包含情侣主页空间的 -->loversHomePage】　
	二级结构：情侣主页 【包含情侣两个人的ID --> personalHomePage】
		三级结构：个人主页 【个人信息展示页】



parseHtml.py:

按照网站结构依次解析对应网页。【结构同上】

最后个人信息保留字段：
	header=['id','gender','age','where','height','edu',\
               'marriage','salary','nation','job',\
                'car','house','look','body','face',\
                'hair','weight','place','smoke','drink',\
                'personality','child','parent']


pdTransform.py:

引用一种二维数组的结构(numpy.ndarray)
引用一种类似于表格的数据结构(pandas.DataFrame)
从而进行清晰易懂的行，列操作。


marryModel.py:

由于数据维度太多，为避免维灾难，故采取PCA(主成分分析)降维。
降维的思想：
计算各变量之间的相关性，得到协方差矩阵。
计算对应的特征值和特征向量。
在矩阵运算中，特征值意味着对该矩阵根据特征向量组合的拉伸变换。
所以，特征值愈大，则意味这该列向量信息量大。
所以，将计算得到的特征向量按照特征值大小排列。采取前面ｎ(即主成分)列。
然后将得到的向量把原数据进行转换成ｎ维数据。从而达到降维的目的。


毫无疑问的，一开始应该进行无监督学习的聚类算法。
得到分类后，才能进行监督学习的决策树算法，或贝叶斯算法。
降维之后，对女生进行聚类分析，得到ｍ个类。将类别对应到男生。
对男生进行决策树算法。训练，测试。
