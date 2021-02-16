import os
import re
import codecs
import requests
import time
import sys

img_dir = '..\\images'
blog_dir = '..\\blogs'''


def download_bar(num, sum):
    percent = num / sum
    if num != sum - 1:
        sys.stdout.write("\r{0}{1}".format("||" * (num + 1), '%.2f%%' % (percent * 100)))
        sys.stdout.flush()
    else:
        sys.stdout.write("\r{0}{1}".format("||" * (num + 1), '%.2f%%' % (100)))
        sys.stdout.flush()
        print("\n" + "下载完成")


def create_dir(path):
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        print('create folder :' + path)
    else:
        print('the folder already exists')


def get_all_md_path(path):
    md_paths = []
    list = os.listdir(blog_dir)  # 列出文件夹下所有的目录与文件
    print('共发现%d个文件\n' % len(list))
    for i in range(0, len(list)):
        path = os.path.join(blog_dir, list[i])
        # if os.path.isfile(path):
        # # 你想对文件的操作
        print('路径为  ：' + path)
        md_paths.append(path)
    return md_paths


if __name__ == '__main__':
    print("图片归类开始")
    init_time = time.strftime("%Y-%m-%d, %H:%M:%S", time.localtime())
    print('当前时间' + init_time)
    create_dir(img_dir)
    create_dir(blog_dir)

    md_paths = get_all_md_path(blog_dir)
    for path in md_paths:
        input_file = codecs.open(path, mode="r", encoding="utf-8")
        text = input_file.read()
        input_file.close()
        # 匹配标题
        # print(text)
        ex = 'blogs\\\\.*?md'
        title = re.findall(ex, path, re.DOTALL)
        print(title)
        title = title[0]
        title = title[6:title.index('.')]
        print(title)
        # 匹配网址
        ex = '\[.*?]\(http.*?[" )]'
        img_paths = re.findall(ex, text)
        print(img_paths)
        for i, l in enumerate(img_paths):
            img_paths[i] = l[l.index('(') + 1:len(l) - 1]
        print(img_paths)

        img_root_dir = img_dir + '\\' + title
        create_dir(img_root_dir)

        print('正在下载图片')
        for u, url in enumerate(img_paths):
            # print('第%d张' % u)
            download_bar(u, len(img_paths))
            img_data = requests.get(url=url).content
            with open(img_root_dir + '\\%d.png' % u, 'wb') as fp:
                fp.write(img_data)
                fp.close()
