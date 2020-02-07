#coding=utf-8
import re
import os,os.path
import shutil
import random
import string
import time

BOUNDARY = u"==========\n" #分隔符
intab = "\/:*?\"<>|"
outtab = "  ： ？“《》 "     #用于替换特殊字符
#trantab = maketrans(intab, outtab)

HTML_HEAD = '''<!DOCTYPE html>
<html>
	<head>
	<meta charset="utf-8" />
	<title> Kindle 读书笔记 </title>
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<link href="../style/css/bootstrap.min.css" rel="stylesheet" type="text/css" />
	<link href="../style/css/bootstrap-theme.min.css" rel="stylesheet" type="text/css" />
	<link href="../style/css/custom.css" rel="stylesheet" type="text/css" />
</head>
<body>
'''

INDEX_TITLE = '''
	<div class="container">
		<header class="header col-md-12">
			<div class="page-header">
				<h1><small><span class="glyphicon glyphicon-book" aria-hidden="true"></span> Kindle 读书笔记 </small> <span class="badge">更新于 UPDATE </span> <span class="badge"> 共 BOOKS_SUM 本书，SENTENCE_SUM 条笔记</span></h1>
			</div>
		</header>
	<div class="col-md-12">
        <div class="list-group">

'''

BOOK_TITLE = '''
	<div class="container">
		<header class="header col-md-12">
			<div class="page-header">
				<h1><small><span class="glyphicon glyphicon-book" aria-hidden="true"></span>BookName</small> <span class="badge"></span></h1>
			</div>
		</header>

        <div class="col-md-2">
			<ul class="nav nav-pills nav-stacked">
				<li role="presentation" class="active text-center">
					<a href="../index.html"><span class="glyphicon glyphicon-chevron-left" aria-hidden="true"></span> 返回目录</a>
				</li>
			</ul>
		</div>
'''

SENTENCE_CONTENT = '''
    	<div class="col-md-12">
			<article>
				<div class="panel panel-default">
					<div class="panel-body mk88"><p>SENTENCE_TXT
                    </p></div>
					<div class="panel-footer text-right">
						<span class="label label-primary"><span class="glyphicon glyphicon-tag" aria-hidden="true"></span> 标注</span>
						<span class="label label-default"><span class="glyphicon glyphicon-bookmark" aria-hidden="true"></span>SENTENCE_ADDR</span>
						<span class="label label-default"><span class="glyphicon glyphicon-time" aria-hidden="true"></span>SENTENCE_TIME</span>
					</div>
				</div>
			</article>
        </div>
'''

ITEM_CONTENT = '''          <a href="HTML_URL" class="list-group-item"><span class="glyphicon glyphicon-book" aria-hidden="true"></span>HTML_FILE_NAME<span class="glyphicon glyphicon-tag" aria-hidden="true">SENTENCE_COUNT</span></a>
'''

FOOTER_CONTENT = '''
        </div>
    </div>
</body>
</html>
'''

# 替换不能用作文件名的字符
def changechar(s):
    return s.translate(str.maketrans(intab,outtab))

# 获取标注位置
def getAddr(s):
    g = s.split(" | ")[0]
    return g

# 获取添加时间
def getTime(s):
    g = s.split(" | ")[1]
    return g.split("\n\n")[0]

# 获取标注内容
def getMark(s):
    g = s.split(" | ")[1]
    try:
        return g.split("\n\n")[1]
    except IndexError:
        #print("list index out of range due to empty content")
        return "empty content"

# 分割函数实现利用关键词进行简单的分割成列表
# 结果为每一条单独的笔记，包含书名，时间，位置和内容
f = open("source.txt", "r", encoding='utf-8')

# 读取标注文件全部内容
content = f.read()

# 替换书名前的空格
content = content.replace(u'\ufeff', u'')
clips = content.split(BOUNDARY)

# 获取列表的个数
print("列表个数：",clips.__len__())
sum = clips.__len__()

# 获取书名存储为列表books，获取除书名外的内容为sentence
both = []  #完整内容。格式为[['',''],['','']……]
books = [] #书名列表
sentence = []  #标注内容
for i in range(0,sum):
    book = clips[i].split("\n-")
    both.append(book)
    #print(book)
    if (book != ['']): # 如果书名非空
        books.append(changechar(book[0])) #添加书名，替换特殊字符，以便创建文件
        sentence.append(book[1])          #添加笔记
print('笔记总数：',sentence.__len__())

# 去除书名列表中的重复元素
nameOfBooks = list(set(books))
nameOfBooks.sort(key=books.index)
print('书籍总数：',nameOfBooks.__len__())

# 根据不同书名建立网页文件
stceOfBookCnt = {}   # 记录每本书有几条标注的字典
# print(os.listdir())
if os.path.exists('books'):
    shutil.rmtree('books')
os.mkdir('books') #创建一个books目录，用于存放书名网页文件
# print(os.listdir())
os.chdir('books') #更改工作目录
for j in range(0,nameOfBooks.__len__()):

# 网页文件的字符长度不能太长，以免无法在linux下创建
    if nameOfBooks[j].__len__() > 80:
        #print(nameOfBooks[j],"_len:",nameOfBooks[j].__len__())
        #print(nameOfBooks[j][0:90]+".html")
        nameOfBooks[j] = nameOfBooks[j][0:80]  # 截取字符串

    f = open(nameOfBooks[j]+".html",'w',encoding='utf-8') # 创建网页文件
    f.write(HTML_HEAD)   # 写入html头文件
    #s = nameOfBooks[j]
    f.write(BOOK_TITLE.replace('BookName',nameOfBooks[j]))

    f.close()
    stceOfBookCnt.__setitem__(nameOfBooks[j],0)  # 清零每本书的标注数量

# 向文件添加标注内容
stce_succ_cnt = 0  # 向html文件添加笔记成功次数
stce_fail_cnt = 0  # 向html文件添加笔记失败次数
# print("html name:",os.listdir())
file_list = os.listdir(".") # 获取当前目录文件名，存放于file_list
for j in range(0,sentence.__len__()):
    temp = both[j]
    filename = changechar(temp[0][0:80])
    if (filename+".html" in file_list ): # 检索字典
        s1 = getAddr(temp[1])  # 获取标注位置
        s2 = getTime(temp[1])  # 获取标注时间
        s3 = getMark(temp[1])  # 获取标注内容
        f = open(filename+".html",'a',encoding='utf-8') # 打开对应的文件
        if (s3 != '\n'):       # 如果文本内容非空
            stce_succ_cnt += 1
            cnt_temp = stceOfBookCnt[filename]
            stceOfBookCnt[filename] = cnt_temp+1
            f.write(SENTENCE_CONTENT.replace("SENTENCE_TXT",s3)
                                    .replace("SENTENCE_TIME",s2)
                                    .replace("SENTENCE_ADDR",s1))
        else:
            stce_fail_cnt += 1
        f.close()

# 向文件添加脚标
file_list = os.listdir(".") #获取当前目录文件名，存放于file_list
html_count = file_list.__len__()
for i in range(0,file_list.__len__()):
    f = open(file_list[i],'a',encoding='utf-8')
    f.write(FOOTER_CONTENT)
    f.close()

# 处理index.html
os.chdir("../")
f=open("index.html",'w',encoding='utf-8')

# 写入html头内容
f.write(HTML_HEAD.replace("../",""))

# 写入书的数量和标注的总数
f.write(INDEX_TITLE.replace("SENTENCE_SUM",str(sentence.__len__()))
                   .replace("UPDATE",time.strftime("%Y-%m-%d %H:%M", time.localtime()))
                   .replace("BOOKS_SUM",str(nameOfBooks.__len__())))

# 根据标注数量对书籍列表进行排序
book_list = []
for i in range(0,html_count):
    html_url = "books/"+file_list[i]
    html_name = file_list[i].replace(".html",'')
    book_item = [html_url,html_name,int(stceOfBookCnt[html_name])]
    book_list.append(book_item)
book_list.sort(key=lambda x: x[2], reverse=True)

# 写入书籍列表以及每本书的标注数量
for i in range(0,html_count - 1):
    url = book_list[i][0]
    name = book_list[i][1]
    num = book_list[i][2]
    f.write(ITEM_CONTENT.replace("HTML_URL",url)
                        .replace("HTML_FILE_NAME",name)
                        .replace("SENTENCE_COUNT",str(num)))
f.write(FOOTER_CONTENT)
f.close()
