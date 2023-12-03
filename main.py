import argparse
import os
import re
import sys
from pathlib import Path


def get_digital(value):
    result = re.search(r'\d+', value)
    if result:
        result = int(result.group())
    else:
        result = 0
    return result


def format_two_digits(input_str, offset=0):
    value = int(input_str) + int(offset)
    result_str = f'{value:02}'
    return result_str


def get_s_name(path):
    return format_two_digits(get_digital(Path(path).name))


def get_e_name(count, offset):
    return format_two_digits(count, offset)


def format_file_name(args, count):
    result = args.format
    result = result.replace('{d_name}', args.d_name)
    result = result.replace('{d_s_name}', args.d_s_name)
    result = result.replace('{d_p_name}', args.d_p_name)
    result = result.replace('{item_num}', format_two_digits(count))
    return result


def get_new_file_name(args, file_name, count):
    suffix_index = file_name.find('.')
    suffix_index = len(file_name) if suffix_index == -1 else suffix_index
    if args.format:
        result = format_file_name(args, count)
        if args.suffix is False:
            result += file_name[suffix_index:]
    else:
        result = f'S{args.d_s_name}E{get_e_name(count, args.offset)}' + file_name[suffix_index:]
    return result


def do_rename(args, file_name_list):
    path = args.path
    count = 1
    for file_name, file_list in file_name_list:
        if args.suffix and len(file_list) > 1:
            print(file_list, file=sys.stderr)
            print('匹配到多个同名但后缀名不同的文件 无法对这些文件进行后缀重命名', file=sys.stderr)
            sys.exit(1)
        try:
            for file in file_list:
                Path(path, file).rename(Path(path, get_new_file_name(args, file, count)))
        except FileExistsError as error:
            print(error, file=sys.stderr)
            print('可尝试的解决方案: 指定offset的参数为足够大的负数执行 然后正常执行一次', file=sys.stderr)
            sys.exit(1)
        count += 1


def get_file_name_list(args):
    path = args.path
    result = {}
    for file in os.listdir(path):
        if re.search(args.pattern, file):
            if not args.directory and Path(path, file).is_dir():
                continue
            if args.exclude and re.search(args.exclude, file):
                continue
            suffix_index = file.find('.')
            file_name = file[:len(file) if suffix_index == -1 else suffix_index]
            result.setdefault(file_name, []).append(file)
    return [(file_name, result[file_name]) for file_name in sorted(result.keys())]


def rename(args):
    file_name_list = get_file_name_list(args)
    do_rename(args, file_name_list)


def init_parameter(args):
    args.d_name = Path(args.path).name
    args.d_s_name = get_s_name(args.path)
    args.d_p_name = Path(args.path).parent.name


def check_args(parser, args):
    if not hasattr(args, 'path'):
        parser.error('请输入要处理的文件夹路径')
        sys.exit(1)
    if not Path(args.path).exists() or not Path(args.path).is_dir():
        parser.error('路径不存在或路径不为文件夹')
        sys.exit(1)
    if args.suffix and not hasattr(args, 'format'):
        parser.error('处理后缀必须搭配format参数使用')
        sys.exit(1)


def parse_args():
    parser = argparse.ArgumentParser(
        description='GuGu_Rename',
        epilog='{d_name}:当前文件夹名称'
               + os.linesep +
               '{d_s_name}:从当前文件夹名称中获取数字并以两位显示'
               + os.linesep +
               '{d_p_name}:当前文件夹的父文件夹名称'
               + os.linesep +
               '{item_num}:当前文件在处理队列中的顺序(两位显示)'
    )
    parser.add_argument('path', help='要处理的文件夹目录')
    parser.add_argument('-o', '--offset', default=0, help='偏移量 默认0')
    parser.add_argument('-p', '--pattern', default='.*', help='使用正则表达式来捕获要处理的文件 默认".*"')
    parser.add_argument('-e', '--exclude', default=None, help='使用正则表达式来排除已捕获的处理文件 默认None')
    parser.add_argument(
        '-f',
        '--format',
        help='设置重命名的格式 默认为S{s_name}E{e_name} 不支持运算'
    )
    parser.add_argument('-s', '--suffix', default=False, type=bool, help='指示要处理文件后缀 默认False')
    parser.add_argument('-d', '--directory', default=False, type=bool, help='指示要处理文件夹 默认False')
    args = parser.parse_args()
    check_args(parser, args)
    init_parameter(args)
    return args


def main():
    args = parse_args()
    rename(args)


if __name__ == '__main__':
    main()
