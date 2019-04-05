from ebooklib import epub
import zipfile
import sys
import getopt
import os


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
    global source, out
    if not os.path.exists(source):
        print('错误: 文件不存在!')
        return
    print('开始解析')
    filename = os.path.split(source)[-1]
    print(os.path.split(source))
    if out == '':
        out = os.path.splitext(filename)[0] + '.epub'
    print(filename, out)


book = epub.EpubBook()


if __name__ == '__main__':
    opts, argv = getopt.getopt(sys.argv[1:], "-h-o:-s:", ['help', 'out', 'source'])
    if len(argv) == 0 and len(opts) == 0:
        print(help_str)
        sys.exit()

    source = ''
    out = ''
    for name, val in opts:
        if name == '-h':
            print(help_str)
            sys.exit()
        if name == '-s':
            source = val
        if name == '-o':
            out = val

    parse()
