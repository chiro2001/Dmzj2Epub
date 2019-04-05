from ebooklib import epub
import zipfile
import sys
import getopt
import os
from base_logger import getLogger


help_str = '''
把动漫之家的缓存zip文件转为epub。
这些缓存zip文件可以在手机的Android文件夹内找到。

    -h --help           显示此帮助。
    -s --source :path   指定源文件/文件夹。如果是文件夹则转换文件夹下所有zip文件。
    -o --out :filename  指定输出文件名。默认为指定的文件夹名称或者源文件名称。

关于:
    https://github.com/LanceLiang2018/Dmzj2Epub
'''


def parse_dir(dirpath):
    global book
    print('解析目录', dirpath)


# 解析单文件，把图像加入book
def parse_file(filepath):
    global book
    print('解析单文件', filepath)


def parse():
    global source, out, book
    if not os.path.exists(source):
        logger.error('Error: %s 文件不存在!' % source)
        return

    logger.info('开始解析')
    filename = os.path.split(source)[-1]
    if out == '':
        out = os.path.splitext(filename)[0] + '.epub'

    # 目录管理
    toc = [(epub.Section(filename), []), ]
    # 主线
    spine = ['cover', 'nav']
    set_cover = False

    # print(filename, out)

    # 输入zip文件的情况
    if not os.path.isdir(filename):
        logger.info('输入了文件 %s' % filename)
        if os.path.splitext(filename.lower())[-1] != '.zip':
            logger.error('不是zip文件')
            sys.exit()
        zipped = zipfile.ZipFile(filename, 'r')
        filelist = list(zipped.filelist)
        # 先按文件长短，后按文件名排序
        filelist.sort(key=lambda k: (len(k.filename), k.filename))
        for file in filelist:
            data = zipped.read(file)
            logger.info("添加文件%s, 文件大小%sKB" % (file.filename, len(data) // 1000))
            img = epub.EpubItem(file_name="images/%s" % file.filename,
                                media_type="image/%s" % os.path.splitext(file.filename)[-1][1:],
                                content=data)
            if set_cover is False:
                set_cover = True
                book.set_cover('cover.jpg', data)

            page = epub.EpubHtml(title=file.filename, file_name='%s.html' % file.filename)
            page.set_content(("<img src=\"%s\">" % ("images/%s" % file.filename)).encode())
            toc[0][1].append(page)
            spine.append(page)
            # spine.append(img)
            book.add_item(page)
            book.add_item(img)

        book.toc = toc

        # add navigation files
        book.add_item(epub.EpubNcx())
        book.add_item(epub.EpubNav())

        # create spine
        book.spine = spine
        epub.write_epub(out, book)


book = epub.EpubBook()


if __name__ == '__main__':
    opts, argv = getopt.getopt(sys.argv[1:], "-h-o:-s:", ['help', 'out', 'source'])
    if len(argv) == 0 and len(opts) == 0:
        print(help_str)
        sys.exit()

    source = ''
    out = ''
    logger = getLogger(__name__)
    for name, val in opts:
        if name == '-h':
            print(help_str)
            sys.exit()
        if name == '-s':
            source = val
        if name == '-o':
            out = val

    parse()
