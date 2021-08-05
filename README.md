# TsinghuaBookCrawler

## 功能

下载整本书的每一张图片，并自动合并得到 pdf 文件。

异步下载，速度较快。

无需学号和密码。

## 使用说明

### 环境

python 版本为 python3，需要安装 aiohttp、aiofiles和fpdf``pip install aiohttp aiofiles fpdf``，无需安装PIL(Pillow)

也可以使用 requirements.txt 进行一键安装：``pip install -r requirements.txt``。

### 使用

用于下载清华教参平台上的电子书pdf版本，清华教参平台：http://reserves.lib.tsinghua.edu.cn 。

找到自己需要的书籍之后，进入阅读界面将地址中的book_category和book_id复制过来即可。

阅读界面地址形如http://reserves.lib.tsinghua.edu.cn/book6/00006705/00006705002/mobile/index.html，其中'book6'的6是book_category，00006705是book_id

例子：
下载大学物理学：``python main.py 6 00006705``
下载现代操作系统：``python main.py 5 00000705``

使用 ``python main.py -h`` 可以打印帮助信息

## 说明

此脚本**仅供方便清华师生学习之用**，下载得到的电子书请务必不要进行传播（尤其是对校外的未授权者），也坚决反对任何批量下载书籍的违规行为。请大家自觉维护版权，合理使用资源，后果自负