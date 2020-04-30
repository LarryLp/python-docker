#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import sys
from iaas import vpc, obs

def main():
    try:
        if len(sys.argv) <= 1:
            print('缺少必要参数：测试组件！')
        elif sys.argv[1].upper() == 'ALL':
            print('测试全部组件！')
        else:
            print('测试组件: ', sys.argv[1:])
            # print(sys.argv[1:])
            if 'VPC' in sys.argv[1:]:
                vpc.main()
            if 'OBS' in sys.argv[1:]:
                obs.main()
    except Exception as e:
        print(e)

if __name__ == '__main__':
    main()
