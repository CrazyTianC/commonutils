"""
生成文件目录树
对generate_tree进行修改，还可以实现批量删除某个文件等操作
"""
from pathlib import Path
import argparse


class DirectionTree(object):
    """
    :param pathname: 目标目录
    :param filename: 要保存成文件的名称
    """

    def __init__(
            self,
            pathname: str,
            filename: str,
            ignore: list
    ):
        super(DirectionTree, self).__init__()
        self.pathname = Path(pathname)
        self.filename = filename
        self.ignore = ignore
        self.tree = ''

    def generate_tree(self, n=0):
        if self.pathname.is_file():
            self.tree += '    |' * n + '─' * 4 + self.pathname.name + '\n'
        elif self.pathname.is_dir():

            self.tree += '    |' * n + '─' * 4 + \
                str(self.pathname.relative_to(self.pathname.parent)) + '\\' + '\n'

            if self.pathname.name in self.ignore or self.pathname.name.startswith(('_', '.')):
                # 忽略文件
                return

            for cp in self.pathname.iterdir():
                self.pathname = Path(cp)
                self.generate_tree(n + 1)

    def save_file(self):
        with open(self.filename, 'w', encoding='utf-8') as f:
            f.write(self.tree)

    def run(self):
        self.generate_tree()
        if self.filename:
            self.save_file()
        else:
            print(self.tree)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.description = '输出路径文件目录树'
    parser.add_argument("-p", "--path", help="输入路径", default='./')
    parser.add_argument("-i", "--ignore", help="需要忽略的文件路径", nargs='+')  # nargs以列表形式接收参
    parser.add_argument("-o", "--output", help="以文件形式输出的路径", default='')
    args = parser.parse_args()

    dirtree = DirectionTree(pathname=args.path, filename=args.output, ignore=args.ignore)
    # dirtree = DirectionTree(pathname='./', filename='', ignore=['.idea', 'log_test'])

    dirtree.run()

