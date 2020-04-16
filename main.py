#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import sys
import time

def main():
    try:
        f = open('result.txt', mode='w')
        if len(sys.argv) <= 1:
            print('缺少必要参数：测试组件！')
            f.write('缺少必要参数：测试组件！')
        elif sys.argv[1].upper() == 'ALL':
            print('测试全部组件！')
            f.write('测试全部组件！')
        else:
            print('测试组件: ', sys.argv[1:])
            f.write('测试组件: %s ' % str(sys.argv[1:]))
        f.close()
        for i in range(1000):
            time.sleep(1)
            print(i)
    except Exception as e:
        print(e)



if __name__ == '__main__':
    main()
