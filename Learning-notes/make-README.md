读取文件脚本



```python

import os


def file_name(file_dir, write_to_file):
    for root, dirs, file_name in os.walk(file_dir):
        with open(write_to_file, 'a', encoding='utf-8') as f:
            root = root.split('/')[6:] # 切片路径, 拿到需要的字段
            root = '/'.join(root) + '/' # 拼接路径
            i = 1
            for file in file_name:
                filename_list = file.split('.')
                if filename_list[1] == 'md':
                    filename = filename_list[0]
                    print(filename)
                    url = root + file
                    url.replace('\\', '/')
                    print(url)
                    result = r'[{filename}]({url})'.format(filename=filename,
                                                           url=url)
                    f.write('%s' % i + '. ' + result + '\n')
                    i += 1


def main():
    # 基本目录, 所有要读取的文件所在的目录  需要用 / 正斜杠
    BASE_PATH = r'C:/Users/Administrator/Desktop/workspace/Learning-notes/'
    # 读取的文件目录
    file_dir = BASE_PATH + r"05-Linux"
    # 写入到的文件
    write_to_file = BASE_PATH + r'README.md'
    file_name(file_dir, write_to_file)


if __name__ == '__main__':
    main()

```



