Ttitle: Marriage model research .
Group Member: Jawen,Swimmi,Czo,Wenter .



details:

jiayuan.py: a spider for http://www.jiayuan.com .
	At first the spider simulate logged in website then fetch the couples' ID on the website.
	Next it download the personal data on his home page.


parse.py :Extract user information from the retrieved webpages with the library BeautifulSoup4.3.2 .

transform.py: transform the users' data to nummeric ,according to a
dictionary which costs our group discussed  a long time ...

pdTransform.py: another program for transform data by using the library
pandas. 

marriageModel.py: Reduce dimisions by PCA,Factor Analysis .Then fit data to KMeans Model and DecisionTree Model.





'''Author:Wenter.Woo
Email:airywent@gmail.com
Org:ECNU '''
