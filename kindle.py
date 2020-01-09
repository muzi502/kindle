#coding=utf-8
import re
import os,os.path
import shutil
import random
import string

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
	<script type="text/javascript" src="../style/js/jquery-1.12.2.min.js"></script>
	<script type="text/javascript" src="../style/js/bootstrap.min.js"></script>
	<script type="text/javascript" src="../style/js/custom.js"></script>
</head>
<body>
	<div class="container">
		<header class="header col-md-12">
			<div class="page-header">
				<h1><small><span class="glyphicon glyphicon-book" aria-hidden="true"></span> Kindle 读书笔记 </small> <span class="badge"></span></h1>
			</div>
		</header>
	<div class="col-md-12">
'''

FOOTER_CONTENT = '''
</div>
</html>
'''

BOOK_NAME = '''
		<header class="header col-md-12">
					<a href="../index.html"><span class="glyphicon glyphicon-chevron-left" aria-hidden="true"></span> 返回目录</a>
		</header>
		<h1><small><span class="glyphicon glyphicon-book" aria-hidden="true"></span>BookName</small> <span class="badge">1</span></h1>
'''

SENTENCE_CONTENT = '''
			<article>
				<div class="panel panel-default">
					<div class="panel-body mk88">
                        <p>SENTENCE_TXT</p>
                    </div>
					<div class="panel-footer text-right">
						<span class="label label-primary"><span class="glyphicon glyphicon-tag" aria-hidden="true"></span> 标注</span> 
						<span class="label label-default"><span class="glyphicon glyphicon-bookmark" aria-hidden="true"></span>SENTENCE_ADDR</span> 
						<span class="label label-default"><span class="glyphicon glyphicon-time" aria-hidden="true"></span>SENTENCE_TIME</span>
					</div>
				</div>
			</article>
'''

ABOUT_PAGE = '''
<div class="ui divider"></div>
    <h1 class="ui center teal aligned header">共 BOOKS_SUM 本书，SENTENCE_SUM 条笔记</h1>
'''

GRID_BEGIN = '''
    <div class="list-group">
'''

GRID_END = '''
        </div>
    </div>
'''

ITEM_CONTENT = '''
        <a href="HTML_URL" class="list-group-item">
        <span class="glyphicon glyphicon-book" aria-hidden="true"></span>HTML_FILE_NAME
        <span class="glyphicon glyphicon-tag" aria-hidden="true">SENTENCE_COUNT</span></a>
'''

# 替换不能用作文件名的字符
def changechar(s):
    return s.translate(str.maketrans(intab,outtab))

# 处理sentence列表的方法函数
def getAddr(s):  #获取标注位置
    g = s.split(" | ")[0]
    return g
def getTime(s):  #获取添加时间
    g = s.split(" | ")[1]
    return g.split("\n\n")[0]
def getMark(s):  #获取标注内容
    g = s.split(" | ")[1]
    try:
        return g.split("\n\n")[1]
    except IndexError:
        #print("list index out of range due to empty content")
        return "empty content"

# 分割函数实现利用关键词进行简单的分割成列表
# 结果为每一条单独的笔记，包含书名，时间，位置和内容
f = open("source.txt", "r", encoding='utf-8')
content = f.read()  # 读取全部内容
content = content.replace(u'\ufeff', u'') #替换书名前的空格
clips = content.split(BOUNDARY)
print("列表个数：",clips.__len__()) # 获取列表的个数
#for i in range(0,4):  #打印出4条标注
    #print(clips[i])
    #print('---------')
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
#print("both:",both)
#print("books:",books)
#print("sentence:",sentence)
print('笔记总数：',sentence.__len__())

# 去除书名列表中的重复元素
nameOfBooks = list(set(books))
nameOfBooks.sort(key=books.index)
print('书籍总数：',nameOfBooks.__len__())
#print(nameOfBooks)

# 根据不同书名建立网页文件
stceOfBookCnt = {}   # 记录每本书有几条标注的字典
#print(os.listdir())
if os.path.exists('books'):
    shutil.rmtree('books')
    print('rm books dir succ')
os.mkdir('books') #创建一个books目录，用于存放书名网页文件
# print(os.listdir())
os.chdir('books') #更改工作目录
for j in range(0,nameOfBooks.__len__()):
    '''
    # 文件名中含有特殊字符则不成创建成功，包括\/*?<>|字符
    #if (nameOfBooks[j]!='Who Moved My Cheese? (Spencer Johnson)'):
        #if (nameOfBooks[j]!='Send to Kindle | 当读书失去动力，你该如何重燃阅读的激情？ (kindle@eub-inc.com)'):
    '''
    # 网页文件的字符长度不能太长，以免无法在linux下创建
    if nameOfBooks[j].__len__() > 80:
        #print(nameOfBooks[j],"_len:",nameOfBooks[j].__len__())
        #print(nameOfBooks[j][0:90]+".html")
        nameOfBooks[j] = nameOfBooks[j][0:80]  # 截取字符串

    f = open(nameOfBooks[j]+".html",'w',encoding='utf-8') # 创建网页文件
    f.write(HTML_HEAD)   # 写入html头文件
    #s = nameOfBooks[j]
    f.write(BOOK_NAME.replace('BookName',nameOfBooks[j])) #写入书名
    f.close()
    stceOfBookCnt.__setitem__(nameOfBooks[j],0)  # 清零每本书的标注数量

# 向文件添加标注内容
stce_succ_cnt = 0  # 向html文件添加笔记成功次数
stce_fail_cnt = 0  # 向html文件添加笔记失败次数
#print("html name:",os.listdir())
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
            print("empty txt",stce_fail_cnt,filename)
        f.close()
    else:
        print("can't find filename html :",temp[0]+".html")
print("sentence add succ cnt = ",stce_succ_cnt)
print("sentence add fail cnt = ",stce_fail_cnt)
#print(stceOfBookCnt)

#向文件添加脚标
#print("html name:",os.listdir())
file_list = os.listdir(".") #获取当前目录文件名，存放于file_list
html_count = file_list.__len__()
print("file_list_count",html_count)
for i in range(0,file_list.__len__()):
    '''
    检查文件名是否过长，验证上面的修改是否成功
    '''
    #print(i,file_list[i].__len__())
    #if file_list[i].__len__() > 80:
    #    print(file_list[i],"len:",file_list[i].__len__())

    f = open(file_list[i],'a',encoding='utf-8') #打开对应的文件
    f.write(FOOTER_CONTENT)
    f.close()

# 处理index.html
os.chdir("../")
print("ls dir",os.listdir())

# 打开对应的文件
f=open("index.html",'w',encoding='utf-8')

# 写入html头内容
f.write(HTML_HEAD.replace("../",""))

# 处理数目
# f.write(ABOUT_PAGE.replace("PIC_NAME",random.randint(1,10).__str__())
#                    .replace("BOOKS_SUM",str(nameOfBooks.__len__()))
#                    .replace("SENTENCE_SUM",str(sentence.__len__())))
f.write(GRID_BEGIN)
for i in range(0,html_count):
    html_url = "books/"+file_list[i]
    html_name = file_list[i].replace(".html",'')
    f.write(ITEM_CONTENT.replace("HTML_URL",html_url)
                        .replace("HTML_FILE_NAME",html_name)
                        .replace("SENTENCE_COUNT",str(stceOfBookCnt[html_name]))) # 写入本书标注数量
f.write(GRID_END)
f.write(FOOTER_CONTENT)
f.close()
