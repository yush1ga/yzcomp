import yzcomp
import sys


def main():
    yml = sys.argv[1]
    cmd, shell = yzcomp.Parser(yml).parse()
    print(yzcomp.Generator(cmd, shell).generate())


if __name__ == '__main__':
    main()
