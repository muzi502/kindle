## 项目说明

这是一个使用 Python 语言编写的小工具，用于将 Kindle 标注笔记文件 `My Clippings.txt` 转换成 html 文件。fork 自 [kindleNote](https://github.com/cyang812/kindleNote)，重写生成的 html 样式为 [书伴网 Clippings Fere 工具](https://bookfere.com/tools#ClippingsFere)，使之适配移动端。预览网站 [kindle.502.li](https://kindle.502.li)

## 使用说明

- 1、从 kindle 中拷贝出标注文件 `My Clippings.txt`，重命名为 source.txt。
- 2、下载本项目源码，使用你的 source.txt 进行替换。
- 3、在 Python3 环境下执行 `python3 kindle.py` 指令，等待生成网页文件。

```shell
git clone https://github.com/muzi502/kindle
cd kindle
cat /your/path/My Clippings.txt > source.txt
python3 kindle.py
```

## 相关脚本

在 Windows 环境下可以使用 .bat 脚本来自动复制 `My Clippings.txt` 文件到相应的位置。根据自己的环境修改相应的变量即可。

```powershell
set src="G:\documents\My Clippings.txt" 
set dist=$PATH/source.txt
set pngsrc=G:\*.png
set pngdist=$PATH
copy /Y  %src% %dist%
copy /Y %pngsrc% %pngdist%
```
