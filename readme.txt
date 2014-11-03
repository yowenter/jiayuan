Hi,
I wrote them for some research on marriage match model. 


details:

jiayuan.py: a spider for http://www.jiayuan.com .
	At first the spider simulate logged in website then fetch the couples' ID on the website.
	Next it download the personal data on his home page.


parse.py :Extract user information from the retrieved webpages with the library BeautifulSoup4.3.2 .

transform.py: transform the users' data to nummeric ,according to a
dictionary that our group discussed for a long time ...

pdTransform.py: another program for transform data by using the library
pandas. 

patent.py:  fetch sources from china patent website for  a research on
comptition intelligence analysis.It's nothing to do with our marriage model
search.

ml.py: using some methods ,such as  SVM,Decision
Trees,then generate a model that predict if a enterprise were to go bankrupt.


If you're interested in data mining ,maybe we can have a talk. :)



