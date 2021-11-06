import re
import sys
import os.path
import shutil
import time

HTML_HEAD = """<!DOCTYPE html>
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
"""

INDEX_TITLE = """
	<div class="container">
		<header class="header col-md-12">
			<div class="page-header">
				<h1><small><span class="glyphicon glyphicon-book" aria-hidden="true"></span> Kindle 读书笔记 </small> <span class="badge">更新于 UPDATE </span> <span class="badge"> 共 BOOKS_SUM 本书，SENTENCE_SUM 条笔记</span></h1>
			</div>
		</header>
	<div class="col-md-12">
        <div class="list-group">
"""

BOOK_TITLE = """
	<div class="container">
		<header class="header col-md-12">
			<div class="page-header">
				<h1><small><span class="glyphicon glyphicon-book" aria-hidden="true"></span>BookName</small> <span class="badge"></span></h1>
			</div>
		</header>

        <div class="col-md-2">
			<ul class="nav nav-pills nav-stacked go-back">
				<li role="presentation" class="active text-center">
					<a href="../index.html" style="border-radius: 50%;"><span class="glyphicon glyphicon-backward" aria-hidden="true"></span></a>
				</li>
			</ul>
		</div>
"""

MARK_CONTENT = """
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
"""

ITEM_CONTENT = """          <a href="HTML_URL" class="list-group-item"><span class="glyphicon glyphicon-book" aria-hidden="true"></span>HTML_FILE_NAME<span class="glyphicon glyphicon-tag" aria-hidden="true">SENTENCE_COUNT</span></a>
"""

FOOTER_CONTENT = """
        </div>
    </div>
</body>
</html>
"""

DELIMITER = u"==========\n"
halfwidth_chars = '()\/:*?"<>|'
fullwidth_chars = "（）  ： ？“《》 "
all_books = []
all_marks = []


def replace_chars(s):
    """replace halfwidth chars to fullwidth chars"""
    return s.translate(str.maketrans(halfwidth_chars, fullwidth_chars))


def get_book_index(book_name):
    """get book's index"""
    for i in range(len(all_books)):
        if all_books[i]["name"] == book_name:
            return i
    return -1


def render_clippings(file_name):
    global all_marks
    global all_books
    with open(file_name, "r", encoding="utf-8") as f:
        content = f.read()
    content = content.replace("\n\n", "\n")
    all_marks = content.split(DELIMITER)
    for i in range(len(all_marks)):
        mark = all_marks[i].split("\n")
        if len(mark) == 4:
            book_info = re.split(r"[（）《》【】｜]\s*", replace_chars(mark[0]))
            book_name = (
                book_info[0].strip()
                if str(book_info[0].strip()) != ""
                else replace_chars(mark[0])
            )
            book_author = book_info[-2].strip() if len(book_info) > 2 else ""
            mark_info = mark[1].split("|")
            mark_time = mark_info[1].strip()
            mark_address = mark_info[0].strip("- ")
            mark_content = mark[2].strip()
            book_index = get_book_index(book_name)
            if book_index == -1:
                all_books.append(
                    {"name": book_name, "author": book_author, "nums": 0, "marks": []}
                )
            all_books[book_index]["marks"].append(
                {"time": mark_time, "address": mark_address, "content": mark_content}
            )
            all_books[book_index]["nums"] += 1
    all_books.sort(key=lambda x: x["nums"], reverse=True)


def render_index_html():
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(HTML_HEAD.replace("../", ""))
        f.write(
            INDEX_TITLE.replace("SENTENCE_SUM", str(len(all_marks)))
            .replace("UPDATE", time.strftime("%Y-%m-%d %H:%M", time.localtime()))
            .replace("BOOKS_SUM", str(len(all_books)))
        )
        for book in all_books:
            f.write(
                ITEM_CONTENT.replace("HTML_URL", "books/" + book["name"] + ".html")
                .replace("HTML_FILE_NAME", book["name"] + " [" + book["author"] + "]")
                .replace("SENTENCE_COUNT", str(book["nums"]))
            )
        f.write(FOOTER_CONTENT)


def render_books_html():
    if os.path.exists("books"):
        shutil.rmtree("books")
    os.mkdir("books")
    for i in range(len(all_books)):
        book_name = str(all_books[i]["name"][0:80])
        with open("books/" + book_name + ".html", "w", encoding="utf-8") as f:
            f.write(HTML_HEAD)
            f.write(BOOK_TITLE.replace("BookName", book_name))
            for j in range(len(all_books[i]["marks"])):
                mark = all_books[i]["marks"][j]
                f.write(
                    MARK_CONTENT.replace("SENTENCE_TXT", mark["content"])
                    .replace("SENTENCE_ADDR", mark["address"])
                    .replace("SENTENCE_TIME", mark["time"])
                )
            f.write(FOOTER_CONTENT)


if __name__ == "__main__":
    file_path = "source.txt" if len(sys.argv) == 1 else sys.argv[1]
    render_clippings(file_path)
    render_index_html()
    render_books_html()
    print("书籍总数：", len(all_books))
    print("笔记总数：", len(all_marks))
