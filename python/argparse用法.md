# argparse用法
官方文档[argparse Parser for command-line options, arguments and sub-commands](https://docs.python.org/3/library/argparse.html)
[Argparse Tutorial](https://docs.python.org/3/howto/argparse.html)

样例：
```
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-i', '--ignore', 
                help='regex for ignore filename', 
                default="^_|node\_modules|summary|readme")
parser.add_argument('-o', '--outfiles', 
                help='the output files such as readme.md summary.md',
                default=[],
                action='append') 
parser.parse_args([])
# Namespace(ignore='^_|node\\_modules|summary|readme', outfiles=[])
```
函数的帮助信息如下：
```
usage: [-h] [-i IGNORE] [-o OUTFILES]

optional arguments:
  -h, --help            show this help message and exit
  -i IGNORE, --ignore IGNORE
                        regex for ignore filename
  -o OUTFILES, --outfiles OUTFILES
                        the output files such as readme.md summary.md
```
## Creating a parser
```
import argparse
parser = argparse.ArgumentParser(prog='PROG')
parser.add_argument('--version', action='version', version='%(prog)s 2.0')
parser.parse_args(['--version'])
# PROG 2.0
```
## action
- store 默认行为
- store_const 与const配合使用，表示常量 
- store_true 如果出现就是true，没有出现就false
- store_false 与store_true正好相反
- append 保存一个链表，可以传入多个参数，如'--foo 1 --foo 2' 或 '--foo 1 2'
- count 计算出现的次数如 -v -vvv的用法


### append_const
与const配合使用，**应用场景比较小众**，比如"--str --int" 等同于"--types str int"，能够提高理解
```
parser = argparse.ArgumentParser()
parser.add_argument('--str', dest='types', action='append_const', const=str)
parser.add_argument('--int', dest='types', action='append_const', const=int)
parser.parse_args('--str --int'.split())
```
## nargs
样例：
```
import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('integers', metavar='N', type=int, nargs='+',
                    help='an integer for the accumulator')
parser.add_argument('--sum', dest='accumulate', action='store_const',
                    const=sum, default=max,
                    help='sum the integers (default: find the max)')
args = parser.parse_args('1 2 3 4'.split(' '))
args.accumulate(args.integers) # 默认为max 
args = parser.parse_args('1 2 3 4 --sum'.split(' '))
args.accumulate(args.integers) # 为求和 
```
### N 参数个数

### ？ 一个参数

### *  多个参数为list

### + 累加参数到list

### argparse.REMAINDER 所有剩余的参数作为list
应用在参数传递场景中
```
parser = argparse.ArgumentParser(prog='PROG')
parser.add_argument('--foo')
parser.add_argument('command')
parser.add_argument('args', nargs=argparse.REMAINDER)
print(parser.parse_args('--foo B cmd --arg1 XX ZZ'.split()))
# Namespace(args=['--arg1', 'XX', 'ZZ'], command='cmd', foo='B')
```